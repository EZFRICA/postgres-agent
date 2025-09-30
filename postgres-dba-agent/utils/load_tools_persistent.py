# utils.py
from toolbox_core import ToolboxSyncClient
from typing import List, Callable
import logging
import inspect

logger = logging.getLogger(__name__)

# Global reusable client
_toolbox_client = None

# Default values for tools with optional parameters
TOOL_DEFAULTS = {
    "get_most_frequent_queries": {"limit": 10},
    "get_slowest_historical_queries": {"limit": 10},
    "get_most_io_intensive_queries": {"limit": 10},
    "get_unused_indexes": {"min_size_mb": 1},
    "get_table_maintenance_stats": {"table_name": None},
    "get_user_role_memberships": {"username": None},
    "get_user_table_permissions": {"table_name": None, "username": None},
    "list_active_queries": {"min_duration_ms": None, "exclude_apps": None},
    "list_database_tables": {"schema_name": None, "table_name": None},
}

# Tools that have no parameters
NO_PARAM_TOOLS = {
    "get_database_sizes",
    "get_blocking_sessions",
    "get_long_running_transactions",
    "get_postgresql_version_info",
    "get_replication_status",
    "get_memory_configuration",
    "get_cache_hit_ratios",
    "find_invalid_indexes",
    "get_database_users_and_roles",
    "get_current_connections_summary",
    "list_installed_extensions",
    "list_available_extensions",
}


class ToolWrapper:
    """Wrapper to handle tools with optional parameters and ADK compatibility"""

    def __init__(self, tool_function: Callable, tool_name: str):
        self.tool = tool_function
        self.tool_name = tool_name
        self.defaults = TOOL_DEFAULTS.get(tool_name, {})

        # Add necessary attributes for function compatibility
        self.__name__ = tool_name
        self.__doc__ = getattr(tool_function, "__doc__", f"Tool: {tool_name}")
        self.__module__ = getattr(
            tool_function, "__module__", "postgres_dba_agent.utils"
        )

        # Simplify signature for ADK
        self._simplify_signature()

    def _simplify_signature(self):
        """Simplify function signature to avoid ADK parsing issues"""
        try:
            # Get original signature
            sig = inspect.signature(self.tool)

            # Create simplified signature
            new_params = []
            for param_name, param in sig.parameters.items():
                # Simplify type annotation
                if param.annotation != inspect.Parameter.empty:
                    # Replace complex annotations with simple types
                    if "Annotated" in str(param.annotation):
                        new_annotation = (
                            str(param.annotation)
                            .split(",")[0]
                            .replace("Annotated[", "")
                            .replace("]", "")
                        )
                        if "int" in new_annotation.lower():
                            new_annotation = int
                        elif "str" in new_annotation.lower():
                            new_annotation = str
                        elif "float" in new_annotation.lower():
                            new_annotation = float
                        elif "bool" in new_annotation.lower():
                            new_annotation = bool
                        else:
                            new_annotation = str
                    else:
                        new_annotation = param.annotation
                else:
                    new_annotation = str

                # Make all parameters optional with default values
                if param_name in self.defaults:
                    default_value = self.defaults[param_name]
                else:
                    default_value = None

                new_param = inspect.Parameter(
                    param_name,
                    inspect.Parameter.KEYWORD_ONLY,
                    default=default_value,
                    annotation=new_annotation,
                )
                new_params.append(new_param)

            # Create new signature
            new_sig = inspect.Signature(new_params)

            # Apply new signature
            self.tool.__signature__ = new_sig

        except Exception as e:
            logger.warning(f"Could not simplify signature for {self.tool_name}: {e}")

    def __call__(self, **kwargs):
        """Execute tool with parameter management"""
        try:
            # Merge with default values
            params = {**self.defaults, **kwargs}

            # Filter None parameters
            params = {k: v for k, v in params.items() if v is not None}

            # Special handling for tools that require parameters
            if self.tool_name in [
                "get_user_table_permissions",
                "get_user_role_memberships",
            ]:
                if not params or "username" not in params or params["username"] is None:
                    # Return a helpful error message instead of raising an exception
                    return {
                        "error": f"❌ MISSING REQUIRED PARAMETER: {self.tool_name} requires a 'username' parameter.",
                        "message": "🔧 SOLUTION: First call 'get_database_users_and_roles' to get the list of users, then call this tool with a specific username from that list.",
                        "workflow": f"📋 CORRECT SEQUENCE:\n1. get_database_users_and_roles() - Get all users\n2. {self.tool_name}(username='specific_user') - Analyze specific user",
                        "status": "blocked",
                    }

                # Handle usernames with special characters by quoting them
                username = params.get("username")
                if username and isinstance(username, str):
                    # Quote the username to handle special characters
                    params["username"] = f'"{username}"'

            # If no parameters, call without arguments
            if not params:
                return self.tool()

            return self.tool(**params)

        except Exception as e:
            logger.error(f"Error executing tool {self.tool_name}: {e}")
            # Try without parameters if error comes from parsing
            if (
                "Failed to parse the parameter" in str(e)
                or "parameter" in str(e).lower()
            ):
                logger.warning(
                    f"Parameter parsing failed for {self.tool_name}, trying without parameters"
                )
                try:
                    return self.tool()
                except Exception as e2:
                    logger.error(
                        f"Tool {self.tool_name} failed even without parameters: {e2}"
                    )
                    raise e2
            raise


def get_toolbox_client(toolbox_url: str):
    """Obtient ou crée un client Toolbox réutilisable"""
    global _toolbox_client
    if _toolbox_client is None:
        _toolbox_client = ToolboxSyncClient(toolbox_url)
    return _toolbox_client


def load_single_tool(toolbox_url: str, tool_name: str) -> Callable:
    """
    Load a single tool from MCP Toolbox.

    Args:
        toolbox_url: URL of the MCP Toolbox server
        tool_name: Name of the tool to load

    Returns:
        Wrapped tool function
    """
    global _toolbox_client

    try:
        # Get or create toolbox client
        if _toolbox_client is None:
            _toolbox_client = ToolboxSyncClient(toolbox_url)

        # Load single tool
        raw_tool = _toolbox_client.load_tool(tool_name)

        # Wrap the tool for ADK compatibility
        wrapped_tool = ToolWrapper(raw_tool, tool_name)

        logger.info(f"Successfully loaded single tool: {tool_name}")
        return wrapped_tool

    except Exception as e:
        logger.error(f"Error loading single tool {tool_name}: {e}")
        raise


def load_tools_persistent(toolbox_url: str, toolset_name: str) -> List:
    """
    Load tools from MCP Toolbox persistently for Google ADK.
    Transform tools to avoid metadata parsing issues.

    Args:
        toolbox_url: MCP Toolbox server URL
        toolset_name: Toolset name to load (or 'all' for all tools)

    Returns:
        List of tools compatible with Google ADK
    """
    try:
        # Use persistent client
        client = get_toolbox_client(toolbox_url)

        # Define tools by toolset (correspondence with tools.yaml)
        toolsets = {
            "postgres-dba-emergency": [
                "list_active_queries",
                "get_blocking_sessions",
                "get_long_running_transactions",
                "get_current_connections_summary",
            ],
            "postgres-dba-performance": [
                "list_active_queries",
                "get_slowest_historical_queries",
                "get_most_io_intensive_queries",
                "get_most_frequent_queries",
                "get_blocking_sessions",
                "get_long_running_transactions",
                "get_cache_hit_ratios",
            ],
            "postgres-dba-schema": [
                "list_database_tables",
                "find_invalid_indexes",
                "get_unused_indexes",
                "get_table_maintenance_stats",
            ],
            "postgres-dba-security": [
                "get_database_users_and_roles",
                "get_user_table_permissions",
                "get_current_connections_summary",
                "get_user_role_memberships",
                "list_database_tables",
                "get_postgresql_version_info",
                "list_installed_extensions",
            ],
            "postgres-dba-maintenance": [
                "get_database_sizes",
                "get_memory_configuration",
                "get_postgresql_version_info",
                "get_replication_status",
                "list_installed_extensions",
                "list_available_extensions",
            ],
            "postgres-dba-complete": [
                "list_active_queries",
                "list_database_tables",
                "list_installed_extensions",
                "list_available_extensions",
                "get_slowest_historical_queries",
                "get_most_io_intensive_queries",
                "get_most_frequent_queries",
                "get_blocking_sessions",
                "get_long_running_transactions",
                "find_invalid_indexes",
                "get_unused_indexes",
                "get_database_users_and_roles",
                "get_user_table_permissions",
                "get_current_connections_summary",
                "get_user_role_memberships",
                "get_database_sizes",
                "get_table_maintenance_stats",
                "get_memory_configuration",
                "get_postgresql_version_info",
                "get_replication_status",
                "get_cache_hit_ratios",
            ],
        }

        # Get tool list for this toolset
        tool_names = toolsets.get(toolset_name, toolsets["postgres-dba-complete"])

        # Load tools individually
        raw_tools = []
        for tool_name in tool_names:
            try:
                tool = client.load_tool(tool_name)
                raw_tools.append(tool)
            except Exception as e:
                logger.warning(f"Could not load tool {tool_name}: {e}")
                # Continue with other tools even if one fails

        if not raw_tools:
            logger.error(f"No tools could be loaded for toolset '{toolset_name}'")
            return []

        logger.info(
            f"Successfully loaded {len(raw_tools)} tools from toolset '{toolset_name}'"
        )

        # Transform tools for ADK compatibility
        transformed_tools = []
        for tool in raw_tools:
            tool_name = getattr(tool, "__name__", str(tool))

            # Wrap tool to handle parameters and simplify signatures
            wrapped_tool = ToolWrapper(tool, tool_name)
            transformed_tools.append(wrapped_tool)

            logger.debug(f"Transformed tool: {tool_name}")

        logger.info(
            f"Successfully transformed {len(transformed_tools)} tools for ADK compatibility"
        )
        return transformed_tools

    except Exception as e:
        logger.error(f"Error loading tools from toolset '{toolset_name}': {e}")
        # Clean up resources in case of error
        try:
            cleanup_toolbox_client()
        except Exception:
            pass
        # Return empty list in case of error to not block the agent
        return []


# Note: safe_tool_execution is now in tool_error_handler.py


def cleanup_toolbox_client():
    """Clean up Toolbox client (to be called at end of application)"""
    global _toolbox_client
    if _toolbox_client is not None:
        try:
            _toolbox_client.close()
        except Exception as e:
            logger.warning(f"Error closing toolbox client: {e}")
        finally:
            _toolbox_client = None


def cleanup_toolbox_connections():
    """Alias pour la compatibilité - nettoie les connexions Toolbox"""
    cleanup_toolbox_client()
