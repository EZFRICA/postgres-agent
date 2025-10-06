"""
PostgreSQL DBA Tools Registry - Central registry for all PostgreSQL tools
This module provides a centralized way to access and manage PostgreSQL tools.
"""

from typing import Dict, List, Optional
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
    "get_table_sizes_summary": {
        "category": "system",
        "description": "Get comprehensive table sizes with row counts and types",
        "parameters": ["schema_name", "limit"],
        "required_params": [],
        "optional_params": ["schema_name", "limit"],
        "defaults": {"schema_name": "public", "limit": 50},
    },
    "list_all_schemas": {
        "category": "system",
        "description": "List all schemas in the database with their properties",
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

        # Ensure result is always a dictionary
        if isinstance(result, dict):
            # If it's already a dict, check if it has the expected structure
            if "status" in result:
                return result
            else:
                return {"status": "success", "tool_name": tool_name, "result": result}
        else:
            # If it's not a dict (e.g., string), wrap it
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


# =============================================================================
# ANALYSIS FUNCTIONS - Centralized logic for all analysis operations
# =============================================================================

def execute_performance_analysis(analysis_type: str = "comprehensive", limit: Optional[int] = None, min_duration: Optional[str] = None, limit_active: Optional[int] = None):
    """
    Execute performance analysis using multiple performance tools.

    Args:
        analysis_type: Type of analysis ("comprehensive", "queries", "blocking", "cache", "memory")
        limit: Number of queries to analyze (required for comprehensive and queries analysis)
        min_duration: Optional minimum duration for active queries (e.g., "5 minutes")
        limit_active: Optional limit for active queries

    Returns:
        Combined performance analysis results
    """
    try:
        logger.info(f"Executing performance analysis: {analysis_type}")

        results = {"analysis_type": analysis_type, "status": "success", "results": {}}

        if analysis_type in ["comprehensive", "queries"]:
            # Query performance analysis - use native tool with optional parameters
            if min_duration or limit_active:
                params = {}
                if min_duration:
                    params["min_duration"] = min_duration
                if limit_active:
                    params["limit"] = limit_active
                results["results"]["active_queries"] = execute_tool("list_active_queries", **params)
            else:
                results["results"]["active_queries"] = execute_tool("list_active_queries")
            
            # Require limit parameter for historical queries
            if limit is None:
                return {
                    "error": "Parameter 'limit' is required for query analysis tools. Please specify how many queries to analyze.",
                    "status": "failed",
                    "required_parameter": "limit",
                    "suggestion": "Example: limit=10 for top 10 queries"
                }
            
            results["results"]["slowest_queries"] = execute_tool(
                "get_slowest_historical_queries", limit=limit
            )
            results["results"]["io_intensive_queries"] = execute_tool(
                "get_most_io_intensive_queries", limit=limit
            )
            results["results"]["frequent_queries"] = execute_tool(
                "get_most_frequent_queries", limit=limit
            )

        if analysis_type in ["comprehensive", "blocking"]:
            # Blocking and contention analysis
            results["results"]["blocking_sessions"] = execute_tool(
                "get_blocking_sessions"
            )
            results["results"]["long_running_transactions"] = execute_tool(
                "get_long_running_transactions"
            )

        if analysis_type in ["comprehensive", "cache"]:
            # Cache performance analysis
            results["results"]["cache_hit_ratios"] = execute_tool(
                "get_cache_hit_ratios"
            )

        if analysis_type in ["comprehensive", "memory"]:
            # Memory configuration analysis
            results["results"]["memory_configuration"] = execute_tool(
                "get_memory_configuration"
            )

        return results

    except Exception as e:
        error_msg = f"Error executing performance analysis: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg, "status": "failed"}


def execute_schema_analysis(analysis_type: str = "comprehensive", schema_name: Optional[str] = None, limit: Optional[int] = None, min_size_mb: Optional[int] = None):
    """
    Execute schema analysis using multiple schema tools.

    Args:
        analysis_type: Type of analysis ("comprehensive", "tables", "indexes", "maintenance")
        schema_name: Schema name to analyze (required for most analysis types)
        limit: Number of results to return
        min_size_mb: Minimum size in MB for filtering

    Returns:
        Combined schema analysis results
    """
    try:
        logger.info(f"Executing schema analysis: {analysis_type}")

        results = {"analysis_type": analysis_type, "status": "success", "results": {}}

        if analysis_type in ["comprehensive", "tables"]:
            # Table analysis
            if schema_name is None:
                return {
                    "error": "Parameter 'schema_name' is required for table analysis. Please specify which schema to analyze.",
                    "status": "failed",
                    "required_parameter": "schema_name",
                    "suggestion": "Example: schema_name='public' or schema_name='ecommerce_schema'"
                }

            
            params = {"schema_name": schema_name}
            if limit:
                params["limit"] = limit
            
            results["results"]["table_sizes"] = execute_tool("get_table_sizes_summary", **params)

            # List tables in schema
            results["results"]["tables"] = execute_tool("list_database_tables")

        if analysis_type in ["comprehensive", "indexes"]:
            # Index analysis
            results["results"]["invalid_indexes"] = execute_tool("find_invalid_indexes")
            
            # Unused indexes
            params = {}
            if min_size_mb:
                params["min_size_mb"] = min_size_mb
            results["results"]["unused_indexes"] = execute_tool("get_unused_indexes", **params)

        if analysis_type in ["comprehensive", "maintenance"]:
            # Maintenance analysis
            if schema_name is None:
                return {
                    "error": "Parameter 'schema_name' is required for maintenance analysis. Please specify which schema to analyze.",
                    "status": "failed",
                    "required_parameter": "schema_name",
                    "suggestion": "Example: schema_name='public' or schema_name='ecommerce_schema'"
                }

            # Get all tables in schema for maintenance stats
            table_sizes_result = execute_tool("get_table_sizes_summary", schema_name=schema_name, limit=100)
            if table_sizes_result.get("status") == "success" and "result" in table_sizes_result:
                tables = table_sizes_result["result"]
                maintenance_stats = {}
                
                # Ensure tables is a list, not a string
                if isinstance(tables, list):
                    for table in tables[:limit or 10]:  # Limit to prevent too many calls
                        if isinstance(table, dict):
                            table_name = table.get("table_name")
                            if table_name:
                                maintenance_result = execute_tool("get_table_maintenance_stats", 
                                                               schema_name=schema_name, table_name=table_name)
                                maintenance_stats[table_name] = maintenance_result
                else:
                    logger.warning(f"Expected list of tables, got {type(tables)}: {tables}")
                
                results["results"]["maintenance_stats"] = maintenance_stats

        return results

    except Exception as e:
        error_msg = f"Error executing schema analysis: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg, "status": "failed"}


def execute_schema_design_review(schema_name: str, focus_areas: Optional[List[str]] = None):
    """
    Execute comprehensive schema design review.

    Args:
        schema_name: Schema name to review (required)
        focus_areas: Optional list of focus areas (normalization, indexing, constraints, performance)

    Returns:
        Schema design review results
    """
    try:
        logger.info(f"Executing schema design review for schema: {schema_name}")

        if focus_areas is None:
            focus_areas = ["normalization", "indexing", "constraints", "performance"]

        results = {"schema_name": schema_name, "focus_areas": focus_areas, "status": "success", "results": {}}

        # Table structure analysis
        results["results"]["table_structure"] = execute_tool("get_table_sizes_summary", schema_name=schema_name, limit=50)
        results["results"]["tables"] = execute_tool("list_database_tables")

        # Index analysis
        if "indexing" in focus_areas:
            results["results"]["invalid_indexes"] = execute_tool("find_invalid_indexes")
            results["results"]["unused_indexes"] = execute_tool("get_unused_indexes")

        # Maintenance analysis
        if "performance" in focus_areas:
            table_sizes_result = execute_tool("get_table_sizes_summary", schema_name=schema_name, limit=20)
            if table_sizes_result.get("status") == "success" and "result" in table_sizes_result:
                tables = table_sizes_result["result"]
                maintenance_stats = {}
                
                # Ensure tables is a list, not a string
                if isinstance(tables, list):
                    for table in tables:
                        if isinstance(table, dict):
                            table_name = table.get("table_name")
                            if table_name:
                                maintenance_result = execute_tool("get_table_maintenance_stats", 
                                                               schema_name=schema_name, table_name=table_name)
                                maintenance_stats[table_name] = maintenance_result
                else:
                    logger.warning(f"Expected list of tables, got {type(tables)}: {tables}")
                
                results["results"]["maintenance_stats"] = maintenance_stats

        return results

    except Exception as e:
        error_msg = f"Error executing schema design review: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg, "status": "failed"}


def execute_maintenance_analysis(analysis_type: str = "comprehensive", schema_name: Optional[str] = None, limit: Optional[int] = None):
    """
    Execute maintenance analysis using multiple maintenance tools.

    Args:
        analysis_type: Type of analysis ("comprehensive", "stats", "sizes", "extensions")
        schema_name: Schema name to analyze (required for stats analysis)
        limit: Number of results to return

    Returns:
        Combined maintenance analysis results
    """
    try:
        logger.info(f"Executing maintenance analysis: {analysis_type}")

        results = {"analysis_type": analysis_type, "status": "success", "results": {}}

        if analysis_type in ["comprehensive", "stats"]:
            # Maintenance statistics
            if schema_name is None:
                return {
                    "error": "Parameter 'schema_name' is required for maintenance stats analysis. Please specify which schema to analyze.",
                    "status": "failed",
                    "required_parameter": "schema_name",
                    "suggestion": "Example: schema_name='public' or schema_name='ecommerce_schema'"
                }

            # Get table sizes first to identify tables for maintenance stats
            table_sizes_result = execute_tool("get_table_sizes_summary", schema_name=schema_name, limit=limit or 20)
            results["results"]["table_sizes"] = table_sizes_result

            if table_sizes_result.get("status") == "success" and "result" in table_sizes_result:
                tables = table_sizes_result["result"]
                logger.info(f"Table sizes result type: {type(table_sizes_result)}, result type: {type(tables)}")
                maintenance_stats = {}
                
                # Ensure tables is a list, not a string
                if isinstance(tables, list):
                    for table in tables:
                        if isinstance(table, dict):
                            table_name = table.get("table_name")
                            if table_name:
                                maintenance_result = execute_tool("get_table_maintenance_stats", 
                                                               schema_name=schema_name, table_name=table_name)
                                maintenance_stats[table_name] = maintenance_result
                else:
                    logger.warning(f"Expected list of tables, got {type(tables)}: {tables}")
                
                results["results"]["maintenance_stats"] = maintenance_stats

        if analysis_type in ["comprehensive", "sizes"]:
            # Database and table sizes
            results["results"]["database_sizes"] = execute_tool("get_database_sizes")
            
            if schema_name:
                results["results"]["schema_table_sizes"] = execute_tool("get_table_sizes_summary", 
                                                                      schema_name=schema_name, limit=limit)

        if analysis_type in ["comprehensive", "extensions"]:
            # Extension analysis
            results["results"]["installed_extensions"] = execute_tool("list_installed_extensions")
            results["results"]["available_extensions"] = execute_tool("list_available_extensions")

        return results

    except Exception as e:
        error_msg = f"Error executing maintenance analysis: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg, "status": "failed"}


def execute_security_audit(analysis_type: str = "comprehensive", username: Optional[str] = None, schema_name: Optional[str] = None, table_name: Optional[str] = None):
    """
    Execute security audit using multiple security tools.

    Args:
        analysis_type: Type of analysis ("comprehensive", "users", "permissions", "connections")
        username: Username to analyze (required for user-specific analysis)
        schema_name: Schema name for table-specific analysis
        table_name: Table name for specific table analysis

    Returns:
        Combined security audit results
    """
    try:
        logger.info(f"Executing security audit: {analysis_type}")

        results = {"analysis_type": analysis_type, "status": "success", "results": {}}

        if analysis_type in ["comprehensive", "users"]:
            # User and role analysis
            results["results"]["users_and_roles"] = execute_tool("get_database_users_and_roles")

            if username:
                results["results"]["user_role_memberships"] = execute_tool("get_user_role_memberships", username=username)

        if analysis_type in ["comprehensive", "permissions"]:
            # Permission analysis
            if username and schema_name and table_name:
                results["results"]["user_table_permissions"] = execute_tool(
                    "get_user_table_permissions", 
                    schema_name=schema_name, 
                    table_name=table_name, 
                    username=username
                )
            elif username:
                # Get user role memberships to understand their permissions
                results["results"]["user_role_memberships"] = execute_tool("get_user_role_memberships", username=username)

        if analysis_type in ["comprehensive", "connections"]:
            # Connection analysis
            results["results"]["current_connections"] = execute_tool("get_current_connections_summary")

        return results

    except Exception as e:
        error_msg = f"Error executing security audit: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg, "status": "failed"}


def execute_user_permissions_analysis(username: str, schema_name: Optional[str] = None, table_name: Optional[str] = None):
    """
    Execute comprehensive user permissions analysis.

    Args:
        username: Username to analyze (required)
        schema_name: Optional schema name for table-specific analysis
        table_name: Optional table name for specific table analysis

    Returns:
        User permissions analysis results
    """
    try:
        logger.info(f"Executing user permissions analysis for user: {username}")

        results = {"username": username, "status": "success", "results": {}}

        # Get user role memberships
        results["results"]["role_memberships"] = execute_tool("get_user_role_memberships", username=username)

        # Get table permissions if schema and table are specified
        if schema_name and table_name:
            results["results"]["table_permissions"] = execute_tool(
                "get_user_table_permissions", 
                schema_name=schema_name, 
                table_name=table_name, 
                username=username
            )

        return results

    except Exception as e:
        error_msg = f"Error executing user permissions analysis: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg, "status": "failed"}
