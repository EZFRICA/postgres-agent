"""
Gestionnaire d'erreurs pour les appels d'outils MCP Toolbox avec Google ADK.
Ce module fournit des fonctions utilitaires pour gérer les erreurs de parsing
et d'exécution des outils.
"""

import logging
from typing import Dict, Any, Optional, Callable
from functools import wraps

logger = logging.getLogger(__name__)

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


def safe_tool_execution(
    tool_name: str, tool_function: Callable, params: Optional[Dict[str, Any]] = None
):
    """
    Execute a tool with error handling and parameter management.

    Args:
        tool_name: Tool name
        tool_function: Tool function to execute
        params: Parameters to pass to the tool

    Returns:
        Tool execution result

    Raises:
        Exception: If tool fails even after recovery attempts
    """
    try:
        # If tool has no parameters
        if tool_name in NO_PARAM_TOOLS:
            logger.debug(f"Executing no-parameter tool: {tool_name}")
            return tool_function()

        # For other tools, use default values if necessary
        if tool_name in TOOL_DEFAULTS and not params:
            params = TOOL_DEFAULTS[tool_name]
            logger.debug(f"Using default parameters for {tool_name}: {params}")

        # Filter None parameters
        if params:
            params = {k: v for k, v in params.items() if v is not None}

        # If no parameters after filtering, call without arguments
        if not params:
            logger.debug(f"Executing tool {tool_name} without parameters")
            return tool_function()

        logger.debug(f"Executing tool {tool_name} with parameters: {params}")
        return tool_function(**params)

    except ValueError as e:
        if "Failed to parse the parameter" in str(e) or "parameter" in str(e).lower():
            # Try without parameters
            logger.warning(
                f"Parameter parsing failed for {tool_name}, trying without parameters"
            )
            try:
                return tool_function()
            except Exception as e2:
                logger.error(f"Tool {tool_name} failed even without parameters: {e2}")
                raise e2
        raise
    except Exception as e:
        logger.error(f"Error executing tool {tool_name}: {e}")
        # Try without parameters if error seems related to parameters
        if "parameter" in str(e).lower() or "argument" in str(e).lower():
            logger.warning(
                f"Parameter-related error for {tool_name}, trying without parameters"
            )
            try:
                return tool_function()
            except Exception as e2:
                logger.error(f"Tool {tool_name} failed even without parameters: {e2}")
                raise e2
        raise


def tool_error_handler(tool_name: str):
    """
    Décorateur pour gérer les erreurs d'exécution des outils.

    Args:
        tool_name: Nom de l'outil pour le logging

    Returns:
        Décorateur qui gère les erreurs
    """

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error in tool {tool_name}: {e}")

                # Try to recover by calling without parameters
                if args or kwargs:
                    logger.warning(
                        f"Trying to recover by calling {tool_name} without parameters"
                    )
                    try:
                        return func()
                    except Exception as e2:
                        logger.error(f"Recovery failed for {tool_name}: {e2}")
                        raise e2
                raise

        return wrapper

    return decorator


def validate_tool_parameters(tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and clean tool parameters.

    Args:
        tool_name: Tool name
        params: Parameters to validate

    Returns:
        Validated and cleaned parameters
    """
    validated_params = {}

    # Apply default values
    if tool_name in TOOL_DEFAULTS:
        validated_params.update(TOOL_DEFAULTS[tool_name])

    # Update with provided parameters
    if params:
        validated_params.update(params)

    # Filter None values
    validated_params = {k: v for k, v in validated_params.items() if v is not None}

    logger.debug(f"Validated parameters for {tool_name}: {validated_params}")
    return validated_params


def get_tool_usage_info(tool_name: str) -> Dict[str, Any]:
    """
    Retourne les informations d'utilisation d'un outil.

    Args:
        tool_name: Nom de l'outil

    Returns:
        Dictionnaire avec les informations d'utilisation
    """
    info = {
        "name": tool_name,
        "has_parameters": tool_name not in NO_PARAM_TOOLS,
        "defaults": TOOL_DEFAULTS.get(tool_name, {}),
        "required_params": [],
        "optional_params": [],
    }

    if tool_name in TOOL_DEFAULTS:
        info["optional_params"] = list(TOOL_DEFAULTS[tool_name].keys())

    return info


def log_tool_execution(
    tool_name: str,
    params: Optional[Dict[str, Any]] = None,
    success: bool = True,
    error: Optional[Exception] = None,
):
    """
    Log l'exécution d'un outil pour le debugging.

    Args:
        tool_name: Nom de l'outil
        params: Paramètres utilisés
        success: Si l'exécution a réussi
        error: Exception si l'exécution a échoué
    """
    if success:
        logger.info(f"Tool {tool_name} executed successfully with params: {params}")
    else:
        logger.error(f"Tool {tool_name} failed with params: {params}, error: {error}")


# Utility function to test tool connectivity
def test_tool_connectivity(tools: list) -> Dict[str, bool]:
    """
    Teste la connectivité de base des outils.

    Args:
        tools: Liste des outils à tester

    Returns:
        Dictionnaire avec le statut de chaque outil
    """
    results = {}

    for tool in tools:
        tool_name = getattr(tool, "__name__", str(tool))
        try:
            # For tools without parameters, try to call them
            if tool_name in NO_PARAM_TOOLS:
                tool()
                results[tool_name] = True
            else:
                # For other tools, just check they are callable
                results[tool_name] = callable(tool)
        except Exception as e:
            logger.warning(f"Tool {tool_name} connectivity test failed: {e}")
            results[tool_name] = False

    return results
