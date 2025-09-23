"""
Multi-agent system for PostgreSQL DBA assistant.
This package contains specialized agents for different aspects of database administration.
"""

# New intelligent coordinator
from .coordinator_agent import get_coordinator_agent

# All specialized single-tool agents
from .list_tables_agent import get_list_tables_agent
from .database_users_agent import get_database_users_agent
from .user_permissions_agent import get_user_permissions_agent
from .synthesis_agent import get_synthesis_agent

# Schema and structure agents
from .list_database_tables_agent import get_list_database_tables_agent
from .get_table_sizes_summary_agent import get_table_sizes_summary_agent
from .get_all_table_sizes_agent import get_all_table_sizes_agent
from .find_invalid_indexes_agent import get_find_invalid_indexes_agent
from .get_unused_indexes_agent import get_unused_indexes_agent
from .get_table_maintenance_stats_agent import get_table_maintenance_stats_agent

# Security and user management agents
from .get_database_users_and_roles_agent import get_database_users_and_roles_agent
from .get_user_table_permissions_agent import get_user_table_permissions_agent
from .get_user_role_memberships_agent import get_user_role_memberships_agent
from .get_current_connections_summary_agent import get_current_connections_summary_agent

# Performance and monitoring agents
from .list_active_queries_agent import get_list_active_queries_agent
from .get_slowest_historical_queries_agent import get_slowest_historical_queries_agent
from .get_most_io_intensive_queries_agent import get_most_io_intensive_queries_agent
from .get_most_frequent_queries_agent import get_most_frequent_queries_agent
from .get_blocking_sessions_agent import get_blocking_sessions_agent
from .get_long_running_transactions_agent import get_long_running_transactions_agent
from .get_cache_hit_ratios_agent import get_cache_hit_ratios_agent

# System and maintenance agents
from .get_database_sizes_agent import get_database_sizes_agent
from .get_memory_configuration_agent import get_memory_configuration_agent
from .get_postgresql_version_info_agent import get_postgresql_version_info_agent
from .get_replication_status_agent import get_replication_status_agent
from .list_installed_extensions_agent import get_list_installed_extensions_agent
from .list_available_extensions_agent import get_list_available_extensions_agent

# Pedagogical agent
from .pedagogical_agent import get_pedagogical_agent

# Agent registry for centralized management
from .agent_registry import get_agent, list_available_agents, get_agent_info


__all__ = [
    # New intelligent coordinator
    "get_coordinator_agent",
    # Specialized single-tool agents
    "get_list_tables_agent",
    "get_database_users_agent",
    "get_user_permissions_agent",
    "get_synthesis_agent",
    # Schema and structure agents
    "get_list_database_tables_agent",
    "get_table_sizes_summary_agent",
    "get_all_table_sizes_agent",
    "get_find_invalid_indexes_agent",
    "get_unused_indexes_agent",
    "get_table_maintenance_stats_agent",
    # Security and user management agents
    "get_database_users_and_roles_agent",
    "get_user_table_permissions_agent",
    "get_user_role_memberships_agent",
    "get_current_connections_summary_agent",
    # Performance and monitoring agents
    "get_list_active_queries_agent",
    "get_slowest_historical_queries_agent",
    "get_most_io_intensive_queries_agent",
    "get_most_frequent_queries_agent",
    "get_blocking_sessions_agent",
    "get_long_running_transactions_agent",
    "get_cache_hit_ratios_agent",
    # System and maintenance agents
    "get_database_sizes_agent",
    "get_memory_configuration_agent",
    "get_postgresql_version_info_agent",
    "get_replication_status_agent",
    "get_list_installed_extensions_agent",
    "get_list_available_extensions_agent",
    # Pedagogical agent
    "get_pedagogical_agent",
    # Agent registry
    "get_agent",
    "list_available_agents",
    "get_agent_info",
]
