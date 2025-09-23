"""
PostgreSQL DBA Multi-Agent System

A comprehensive multi-agent system for PostgreSQL database administration
using Google ADK and MCP Toolbox hosted on Cloud Run.
"""

__version__ = "1.0.0"
__author__ = "PostgreSQL DBA Agent Team"

# Export main components
from .agent import (
    coordinator_agent,
    root_agent,
    run_agent_with_session,
    ask_question,
    start_new_conversation,
    shutdown_agent,
)
from .config import settings
from .logging_config import initialize_logging, get_logger

__all__ = [
    "coordinator_agent",
    "root_agent",
    "run_agent_with_session",
    "ask_question",
    "start_new_conversation",
    "shutdown_agent",
    "settings",
    "initialize_logging",
    "get_logger",
]
