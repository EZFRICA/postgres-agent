"""
Multi-agent system for PostgreSQL DBA assistant.
This package contains specialized agents for different aspects of database administration.
"""

# New intelligent coordinator
from .coordinator_agent import get_coordinator_agent

# Specialized agents
from .pedagogical_agent import get_pedagogical_agent
from .synthesis_agent import get_synthesis_agent
from .performance_agent import get_performance_agent
from .security_agent import get_security_agent
from .maintenance_agent import get_maintenance_agent
from .schema_agent import get_schema_agent

# Tools registry for centralized tool management
from .tools_registry import (
    execute_tool,
    get_tool_info,
    list_available_tools,
    get_tools_by_category,
    get_all_categories,
    validate_tool_parameters,
    get_tools_summary,
)


__all__ = [
    # Main coordinator
    "get_coordinator_agent",
    # Specialized agents
    "get_pedagogical_agent",
    "get_synthesis_agent",
    "get_performance_agent",
    "get_security_agent",
    "get_maintenance_agent",
    "get_schema_agent",
    # Tools registry functions
    "execute_tool",
    "get_tool_info",
    "list_available_tools",
    "get_tools_by_category",
    "get_all_categories",
    "validate_tool_parameters",
    "get_tools_summary",
]
