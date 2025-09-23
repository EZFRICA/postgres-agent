"""
PostgreSQL DBA Agent Registry - Central registry for all specialized agents
This module provides a centralized way to access all specialized agents.
"""

# Import all specialized agents
from .list_active_queries_agent import get_list_active_queries_agent
from .list_database_tables_agent import get_list_database_tables_agent
from .list_installed_extensions_agent import get_list_installed_extensions_agent
from .list_available_extensions_agent import get_list_available_extensions_agent
from .get_slowest_historical_queries_agent import get_slowest_historical_queries_agent
from .get_most_io_intensive_queries_agent import get_most_io_intensive_queries_agent
from .get_most_frequent_queries_agent import get_most_frequent_queries_agent
from .get_blocking_sessions_agent import get_blocking_sessions_agent
from .get_long_running_transactions_agent import get_long_running_transactions_agent
from .get_table_sizes_summary_agent import get_table_sizes_summary_agent
from .get_all_table_sizes_agent import get_all_table_sizes_agent
from .find_invalid_indexes_agent import get_find_invalid_indexes_agent
from .get_unused_indexes_agent import get_unused_indexes_agent
from .get_database_users_and_roles_agent import get_database_users_and_roles_agent
from .get_user_table_permissions_agent import get_user_table_permissions_agent
from .get_current_connections_summary_agent import get_current_connections_summary_agent
from .get_user_role_memberships_agent import get_user_role_memberships_agent
from .get_database_sizes_agent import get_database_sizes_agent
from .get_table_maintenance_stats_agent import get_table_maintenance_stats_agent
from .get_memory_configuration_agent import get_memory_configuration_agent
from .get_postgresql_version_info_agent import get_postgresql_version_info_agent
from .get_replication_status_agent import get_replication_status_agent
from .get_cache_hit_ratios_agent import get_cache_hit_ratios_agent
from .synthesis_agent import get_synthesis_agent

# Registry of all available specialized agents
AGENT_REGISTRY = {
    # Native tools
    "list_active_queries_agent": get_list_active_queries_agent,
    "list_database_tables_agent": get_list_database_tables_agent,
    "list_installed_extensions_agent": get_list_installed_extensions_agent,
    "list_available_extensions_agent": get_list_available_extensions_agent,
    # Performance tools
    "get_slowest_historical_queries_agent": get_slowest_historical_queries_agent,
    "get_most_io_intensive_queries_agent": get_most_io_intensive_queries_agent,
    "get_most_frequent_queries_agent": get_most_frequent_queries_agent,
    "get_blocking_sessions_agent": get_blocking_sessions_agent,
    "get_long_running_transactions_agent": get_long_running_transactions_agent,
    "get_cache_hit_ratios_agent": get_cache_hit_ratios_agent,
    # Schema tools
    "get_table_sizes_summary_agent": get_table_sizes_summary_agent,
    "get_all_table_sizes_agent": get_all_table_sizes_agent,
    "find_invalid_indexes_agent": get_find_invalid_indexes_agent,
    "get_unused_indexes_agent": get_unused_indexes_agent,
    "get_table_maintenance_stats_agent": get_table_maintenance_stats_agent,
    # Security tools
    "get_database_users_and_roles_agent": get_database_users_and_roles_agent,
    "get_user_table_permissions_agent": get_user_table_permissions_agent,
    "get_user_role_memberships_agent": get_user_role_memberships_agent,
    "get_current_connections_summary_agent": get_current_connections_summary_agent,
    # System tools
    "get_database_sizes_agent": get_database_sizes_agent,
    "get_memory_configuration_agent": get_memory_configuration_agent,
    "get_postgresql_version_info_agent": get_postgresql_version_info_agent,
    "get_replication_status_agent": get_replication_status_agent,
    # Synthesis
    "synthesis_agent": get_synthesis_agent,
}


def get_agent(agent_name: str):
    """
    Get a specialized agent by name.

    Args:
        agent_name: Name of the agent to retrieve

    Returns:
        Agent instance

    Raises:
        KeyError: If agent name is not found
    """
    if agent_name not in AGENT_REGISTRY:
        available_agents = list(AGENT_REGISTRY.keys())
        raise KeyError(
            f"Agent '{agent_name}' not found. Available agents: {available_agents}"
        )

    return AGENT_REGISTRY[agent_name]()


def list_available_agents():
    """
    List all available specialized agents.

    Returns:
        List of agent names
    """
    return list(AGENT_REGISTRY.keys())


def get_agent_info(agent_name: str):
    """
    Get information about a specific agent.

    Args:
        agent_name: Name of the agent

    Returns:
        Dictionary with agent information
    """
    if agent_name not in AGENT_REGISTRY:
        return {"error": f"Agent '{agent_name}' not found"}

    # Basic agent information
    agent_info = {
        "name": agent_name,
        "available": True,
        "description": f"Specialized agent for {agent_name.replace('_', ' ')}",
    }

    # Add specific tool information based on agent type
    if "tables" in agent_name:
        agent_info["tool"] = "list_database_tables"
        agent_info["parameters"] = "NONE"
    elif "sizes" in agent_name:
        agent_info["tool"] = "get_table_sizes_summary"
        agent_info["parameters"] = "schema_name, limit"
    elif "users" in agent_name:
        agent_info["tool"] = "get_database_users_and_roles"
        agent_info["parameters"] = "NONE"
    elif "permissions" in agent_name:
        agent_info["tool"] = "get_user_table_permissions"
        agent_info["parameters"] = "table_name, username"
    elif "synthesis" in agent_name:
        agent_info["tool"] = "NONE"
        agent_info["parameters"] = "NONE"
        agent_info["description"] = "Combines results from multiple agents"

    return agent_info
