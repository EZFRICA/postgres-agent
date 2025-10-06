# utils.py
from toolbox_core import ToolboxSyncClient
from typing import List, Callable
import logging
import inspect

logger = logging.getLogger(__name__)

# Global reusable client
_toolbox_client = None

# No default values needed - let MCP Toolbox handle parameters directly

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
    "list_all_schemas",
}


class ToolWrapper:
    """Wrapper to handle tools with optional parameters and ADK compatibility"""

    def __init__(self, tool_function: Callable, tool_name: str):
        self.tool = tool_function
        self.tool_name = tool_name

        # Add necessary attributes for function compatibility
        self.__name__ = tool_name
        self.__doc__ = getattr(tool_function, "__doc__", f"Tool: {tool_name}")
        self.__module__ = getattr(
            tool_function, "__module__", "postgres_dba_agent.utils"
        )

        # Get tool signature to understand required parameters
        try:
            self.signature = inspect.signature(tool_function)
        except Exception:
            self.signature = None

    def __call__(self, **kwargs):
        """Execute tool with parameter validation"""
        try:
            # Let MCP Toolbox handle all parameters directly
            return self.tool(**kwargs)
        except TypeError as e:
            error_msg = str(e)
            # Check if it's a missing required argument error
            if "missing a required argument" in error_msg or "required positional argument" in error_msg:
                # Extract parameter name from error message
                import re
                match = re.search(r"'(\w+)'", error_msg)
                param_name = match.group(1) if match else "unknown"
                
                # Return a user-friendly error message
                friendly_msg = (
                    f"❌ Tool '{self.tool_name}' requires the parameter '{param_name}' but it was not provided.\n\n"
                    f"Please provide the required parameter. For example:\n"
                    f"- For query analysis tools: specify 'limit' (e.g., limit=10)\n"
                    f"- For schema tools: specify 'schema_name' (e.g., schema_name='public')\n"
                    f"- For size analysis: specify both 'schema_name' and 'limit'\n\n"
                    f"Ask me again with the required parameter included."
                )
                logger.error(f"Missing required parameter for {self.tool_name}: {param_name}")
                return {"error": friendly_msg, "tool": self.tool_name, "missing_parameter": param_name}
            else:
                logger.error(f"Type error executing tool {self.tool_name}: {e}")
                raise
        except Exception as e:
            logger.error(f"Error executing tool {self.tool_name}: {e}")
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
                "list_all_schemas",
                "get_table_sizes_summary",
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
                "list_all_schemas",
                "get_slowest_historical_queries",
                "get_most_io_intensive_queries",
                "get_most_frequent_queries",
                "get_blocking_sessions",
                "get_long_running_transactions",
                "get_table_sizes_summary",
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
