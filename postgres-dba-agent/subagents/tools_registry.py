"""
PostgreSQL DBA Tools Registry - Central registry for all PostgreSQL tools
This module provides a centralized way to access and manage PostgreSQL tools.
"""

from typing import Dict, List
from ..logging_config import get_logger
from ..config import settings as config
from ..utils.load_tools_persistent import load_single_tool

logger = get_logger(__name__)

# Tools registry with their metadata
TOOLS_REGISTRY = {
    # Schema & Structure Tools
    "list_database_tables": {
        "category": "schema",
        "description": "List all database tables with schema information",
        "parameters": [],
        "required_params": [],
        "optional_params": ["schema_name", "table_name"],
    },
    "find_invalid_indexes": {
        "category": "schema",
        "description": "Find invalid or broken indexes in the database",
        "parameters": [],
        "required_params": [],
        "optional_params": [],
    },
    "get_unused_indexes": {
        "category": "schema",
        "description": "Identify indexes that are not being used",
        "parameters": ["min_size_mb"],
        "required_params": [],
        "optional_params": ["min_size_mb"],
        "defaults": {"min_size_mb": 1},
    },
    "get_table_maintenance_stats": {
        "category": "schema",
        "description": "Get maintenance statistics for database tables",
        "parameters": ["table_name"],
        "required_params": [],
        "optional_params": ["table_name"],
    },
    # Security & Users Tools
    "get_database_users_and_roles": {
        "category": "security",
        "description": "List all database users and their roles",
        "parameters": [],
        "required_params": [],
        "optional_params": [],
    },
    "get_user_table_permissions": {
        "category": "security",
        "description": "Get table permissions for a specific user",
        "parameters": ["table_name", "username"],
        "required_params": ["username"],
        "optional_params": ["table_name"],
    },
    "get_user_role_memberships": {
        "category": "security",
        "description": "Get role memberships for a specific user",
        "parameters": ["username"],
        "required_params": ["username"],
        "optional_params": [],
    },
    "get_current_connections_summary": {
        "category": "security",
        "description": "Get summary of current database connections",
        "parameters": [],
        "required_params": [],
        "optional_params": [],
    },
    # Performance & Monitoring Tools
    "list_active_queries": {
        "category": "performance",
        "description": "List currently active queries in the database",
        "parameters": [],
        "required_params": [],
        "optional_params": ["min_duration_ms", "exclude_apps"],
    },
    "get_slowest_historical_queries": {
        "category": "performance",
        "description": "Get the slowest queries from query history",
        "parameters": ["limit"],
        "required_params": [],
        "optional_params": ["limit"],
        "defaults": {"limit": 10},
    },
    "get_most_io_intensive_queries": {
        "category": "performance",
        "description": "Get the most I/O intensive queries",
        "parameters": ["limit"],
        "required_params": [],
        "optional_params": ["limit"],
        "defaults": {"limit": 10},
    },
    "get_most_frequent_queries": {
        "category": "performance",
        "description": "Get the most frequently executed queries",
        "parameters": ["limit"],
        "required_params": [],
        "optional_params": ["limit"],
        "defaults": {"limit": 10},
    },
    "get_blocking_sessions": {
        "category": "performance",
        "description": "Find sessions that are blocking other queries",
        "parameters": [],
        "required_params": [],
        "optional_params": [],
    },
    "get_long_running_transactions": {
        "category": "performance",
        "description": "Find long-running transactions",
        "parameters": [],
        "required_params": [],
        "optional_params": [],
    },
    "get_cache_hit_ratios": {
        "category": "performance",
        "description": "Get database cache hit ratios",
        "parameters": [],
        "required_params": [],
        "optional_params": [],
    },
    # System & Maintenance Tools
    "get_database_sizes": {
        "category": "system",
        "description": "Get sizes of all databases",
        "parameters": [],
        "required_params": [],
        "optional_params": [],
    },
    "get_memory_configuration": {
        "category": "system",
        "description": "Get PostgreSQL memory configuration",
        "parameters": [],
        "required_params": [],
        "optional_params": [],
    },
    "get_postgresql_version_info": {
        "category": "system",
        "description": "Get PostgreSQL version and build information",
        "parameters": [],
        "required_params": [],
        "optional_params": [],
    },
    "get_replication_status": {
        "category": "system",
        "description": "Get PostgreSQL replication status",
        "parameters": [],
        "required_params": [],
        "optional_params": [],
    },
    "list_installed_extensions": {
        "category": "system",
        "description": "List all installed PostgreSQL extensions",
        "parameters": [],
        "required_params": [],
        "optional_params": [],
    },
    "list_available_extensions": {
        "category": "system",
        "description": "List all available PostgreSQL extensions",
        "parameters": [],
        "required_params": [],
        "optional_params": [],
    },
}

# Tool categories for organization
TOOL_CATEGORIES = {
    "schema": "Schema & Structure",
    "security": "Security & Users",
    "performance": "Performance & Monitoring",
    "system": "System & Maintenance",
}


def execute_tool(tool_name: str, **kwargs) -> Dict:
    """
    Execute a PostgreSQL tool directly.

    Args:
        tool_name: Name of the PostgreSQL tool to execute
        **kwargs: Parameters to pass to the tool

    Returns:
        Result from the PostgreSQL tool
    """
    try:
        logger.info(f"Executing PostgreSQL tool: {tool_name}")

        # Validate tool exists
        if tool_name not in TOOLS_REGISTRY:
            available_tools = list(TOOLS_REGISTRY.keys())
            error_msg = (
                f"Tool '{tool_name}' not found. Available tools: {available_tools}"
            )
            logger.error(error_msg)
            return {"error": error_msg, "status": "failed"}

        # Load and execute the tool
        tool = load_single_tool(config.TOOLBOX_URL, tool_name)

        # Execute the tool with provided parameters
        if kwargs:
            result = tool(**kwargs)
        else:
            result = tool()

        logger.info(f"Successfully executed tool: {tool_name}")
        return {"status": "success", "tool_name": tool_name, "result": result}

    except Exception as e:
        error_msg = f"Error executing tool '{tool_name}': {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg, "status": "failed"}


def get_tool_info(tool_name: str) -> Dict:
    """
    Get information about a specific tool.

    Args:
        tool_name: Name of the tool

    Returns:
        Dictionary with tool information
    """
    if tool_name not in TOOLS_REGISTRY:
        return {"error": f"Tool '{tool_name}' not found"}

    tool_info = TOOLS_REGISTRY[tool_name].copy()
    tool_info["name"] = tool_name
    tool_info["available"] = True

    return tool_info


def list_available_tools() -> List[str]:
    """
    List all available PostgreSQL tools.

    Returns:
        List of tool names
    """
    return list(TOOLS_REGISTRY.keys())


def get_tools_by_category(category: str) -> List[str]:
    """
    Get all tools in a specific category.

    Args:
        category: Tool category (schema, security, performance, system)

    Returns:
        List of tool names in the category
    """
    return [
        tool_name
        for tool_name, info in TOOLS_REGISTRY.items()
        if info.get("category") == category
    ]


def get_all_categories() -> Dict[str, str]:
    """
    Get all available tool categories.

    Returns:
        Dictionary mapping category keys to display names
    """
    return TOOL_CATEGORIES.copy()


def validate_tool_parameters(tool_name: str, **kwargs) -> Dict:
    """
    Validate parameters for a tool before execution.

    Args:
        tool_name: Name of the tool
        **kwargs: Parameters to validate

    Returns:
        Validation result with status and messages
    """
    if tool_name not in TOOLS_REGISTRY:
        return {
            "valid": False,
            "error": f"Tool '{tool_name}' not found",
            "available_tools": list(TOOLS_REGISTRY.keys()),
        }

    tool_info = TOOLS_REGISTRY[tool_name]
    required_params = tool_info.get("required_params", [])
    all_params = tool_info.get("parameters", [])

    # Check required parameters
    missing_params = [
        param
        for param in required_params
        if param not in kwargs or kwargs[param] is None
    ]
    if missing_params:
        return {
            "valid": False,
            "error": f"Missing required parameters: {missing_params}",
            "required_params": required_params,
            "provided_params": list(kwargs.keys()),
        }

    # Check for unknown parameters
    unknown_params = [param for param in kwargs.keys() if param not in all_params]
    if unknown_params:
        return {
            "valid": False,
            "warning": f"Unknown parameters will be ignored: {unknown_params}",
            "valid_params": all_params,
        }

    return {"valid": True, "message": "All parameters are valid"}


def get_tools_summary() -> Dict:
    """
    Get a comprehensive summary of all available tools.

    Returns:
        Summary with tools organized by category
    """
    summary = {
        "total_tools": len(TOOLS_REGISTRY),
        "categories": {},
        "tools_by_category": {},
    }

    # Organize tools by category
    for category_key, category_name in TOOL_CATEGORIES.items():
        tools_in_category = get_tools_by_category(category_key)
        summary["categories"][category_key] = {
            "name": category_name,
            "count": len(tools_in_category),
        }
        summary["tools_by_category"][category_key] = tools_in_category

    return summary
