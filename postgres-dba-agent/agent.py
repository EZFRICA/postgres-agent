#!/usr/bin/env python3
"""
Main entry point for PostgreSQL DBA Multi-Agent with Google ADK.
Uses a coordinator agent that orchestrates specialized database administration agents.
"""

from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
import signal
import atexit

# Import centralized logging and configuration
from .logging_config import initialize_logging
from .config import settings as config

# Import the coordinator agent and multi-agent system
from .subagents import coordinator_agent

# Import cleanup function for proper session management
from .utils import cleanup_toolbox_connections

# Initialize logging
logger = initialize_logging()


# Define shutdown function first
def shutdown_agent():
    """
    Properly shutdown the agent and clean up all resources.
    This function should be called when the application is shutting down
    to avoid "Unclosed client session" warnings.
    """
    logger.info("Shutting down PostgreSQL DBA Multi-Agent...")
    cleanup_toolbox_connections()
    logger.info("Agent shutdown complete")


# Register cleanup function for graceful shutdown
def signal_handler(signum, frame):
    logger.info(f"Received signal {signum}, shutting down gracefully...")
    try:
        shutdown_agent()
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")
    finally:
        # Force exit after cleanup
        import os

        os._exit(0)


# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# Register cleanup on exit
atexit.register(shutdown_agent)

session_service = InMemorySessionService()

# Create the coordinator agent instance
coordinator_agent = coordinator_agent.get_coordinator_agent()

# ADK expects a root_agent variable - alias to our coordinator
root_agent = coordinator_agent


# Environment configuration
def setup_environment():
    """Configure environment variables for ADK."""
    logger.info("🔧 Environment configured for PostgreSQL DBA Multi-Agent")


# Initialize on module load
setup_environment()


async def run_agent_with_session(
    message: str, user_id: str = config.DEFAULT_USER_ID, session_id: str = None
):
    """
    Execute the coordinator agent with native session management and user interaction.

    Args:
        message: User's message
        user_id: User ID
        session_id: Session ID (None for new session)

    Returns:
        Coordinator agent's response with orchestrated sub-agents
    """
    try:
        # Create or retrieve session
        if session_id is None:
            session = await session_service.create_session(
                app_name=config.APP_NAME, user_id=user_id
            )
            session_id = session.id
        else:
            session = await session_service.get_session(
                app_name=config.APP_NAME, user_id=user_id, session_id=session_id
            )

        # Create runner with coordinator agent and services
        runner = Runner(
            app_name=config.APP_NAME,
            agent=coordinator_agent,
            session_service=session_service,
        )

        # Execute coordinator agent that will orchestrate specialized agents
        content = types.Content(role="user", parts=[types.Part(text=message)])
        events = runner.run(session_id=session_id, user_id=user_id, new_message=content)

        # Collect responses from coordinator and sub-agents
        responses = [
            part.text
            for event in events
            for part in event.content.parts
            if part.text is not None
        ]

        return "\n".join(responses) if responses else "No response generated."

    except Exception as e:
        logger.error(f"Error during coordinator agent execution: {e}")
        return f"Error: {str(e)}"


async def get_session_info(user_id: str = config.DEFAULT_USER_ID):
    """Retrieve session information for a user."""
    try:
        sessions_response = await session_service.list_sessions(
            app_name=config.APP_NAME, user_id=user_id
        )

        # Convert response to list
        sessions = []
        async for session in sessions_response:
            sessions.append(session)

        return {
            "user_id": user_id,
            "sessions_count": len(sessions),
            "sessions": [
                {
                    "id": session.id,
                    "last_update": session.last_update_time,
                    "events_count": len(session.events),
                    "state_keys": list(session.state.keys()),
                }
                for session in sessions
            ],
        }
    except Exception as e:
        logger.error(f"Error retrieving sessions: {e}")
        return {"error": str(e)}


async def clear_user_sessions(user_id: str = config.DEFAULT_USER_ID):
    """Clear all sessions for a user."""
    try:
        sessions_response = await session_service.list_sessions(
            app_name=config.APP_NAME, user_id=user_id
        )

        deleted_count = 0
        async for session in sessions_response:
            await session_service.delete_session(
                app_name=config.APP_NAME, user_id=user_id, session_id=session.id
            )
            deleted_count += 1

        return {"message": f"{deleted_count} sessions cleared for user {user_id}"}
    except Exception as e:
        logger.error(f"Error clearing sessions: {e}")
        return {"error": str(e)}


async def ask_question(message: str, user_id: str = config.DEFAULT_USER_ID):
    """
    Simplified function to ask a question to the coordinator agent.
    The coordinator agent automatically handles routing to specialized agents and pedagogical questions.

    Args:
        message: User's question
        user_id: User ID (optional)

    Returns:
        Coordinator agent's response with orchestrated sub-agents
    """
    return await run_agent_with_session(message, user_id)


async def start_new_conversation(user_id: str = config.DEFAULT_USER_ID):
    """
    Start a new interactive conversation.

    Args:
        user_id: User ID

    Returns:
        Welcome message
    """
    welcome_message = """
    Welcome to the PostgreSQL DBA Multi-Agent Expert System! 🚀
    
    I'm a sophisticated database administration assistant powered by specialized AI agents, each expert in different aspects of PostgreSQL management. I can perform comprehensive database analysis, optimization, and provide actionable recommendations.
    
    **🏗️ Multi-Agent Architecture:**
    - **🎯 Coordinator Agent**: Orchestrates analysis workflow and validates each step with you
    - **⚡ Performance Agent**: Deep performance analysis using pg_stat_statements, query plans, and blocking analysis
    - **🔒 Security Agent**: Comprehensive security audits, role analysis, and privilege reviews
    - **📊 Schema Agent**: Advanced schema analysis, indexing strategies, and table optimization
    - **🔧 Maintenance Agent**: System health monitoring, VACUUM analysis, and configuration optimization
    - **🌟 Generalist Agent**: Complex cross-domain issues requiring multi-faceted analysis
    - **📚 Pedagogical Agent**: In-depth explanations of PostgreSQL concepts and best practices
    
    **🔬 Advanced Diagnostic Capabilities:**
    
    **Performance Deep Dive:**
    - "Analyze query performance bottlenecks and identify the top 10 slowest operations with execution plans"
    - "Investigate blocking sessions and deadlock patterns over the last 24 hours"
    - "Evaluate buffer cache hit ratios and recommend memory configuration optimizations"
    - "Identify queries causing high I/O wait times and suggest index optimizations"
    
    **Security & Compliance:**
    - "Conduct a comprehensive security audit of user privileges and role hierarchies"
    - "Analyze authentication methods and identify potential security vulnerabilities"
    - "Review table-level permissions and detect privilege escalation risks"
    - "Generate compliance report for database access controls"
    
    **Schema Optimization:**
    - "Perform advanced indexing analysis with usage statistics and redundancy detection"
    - "Analyze table bloat, fragmentation, and recommend maintenance strategies"
    - "Evaluate foreign key relationships and constraint validation performance"
    - "Assess partitioning strategies for large tables based on access patterns"
    
    **System Health & Maintenance:**
    - "Comprehensive database health check with performance baselines and trend analysis"
    - "Analyze VACUUM and ANALYZE statistics with recommendations for automation"
    - "Review PostgreSQL configuration parameters against workload requirements"
    - "Evaluate replication lag and standby server performance"
    
    **📈 Interactive Workflow:**
    Each analysis follows a structured process:
    1. **Initial Assessment** → I analyze your request and route to appropriate specialists
    2. **Deep Analysis** → Specialized agents perform detailed investigation using real database metrics
    3. **Findings Validation** → I present findings and ask for your confirmation before proceeding
    4. **Synthesis & Recommendations** → Final actionable recommendations with implementation priorities
    
    **💡 Example Professional Queries:**
    - "Our e-commerce platform experiences performance degradation during peak hours. Analyze query patterns, identify bottlenecks, and recommend optimization strategies."
    - "Conduct a security assessment of our multi-tenant database architecture and verify proper row-level security implementation."
    - "Our 500GB orders table is experiencing slow queries. Analyze the current indexing strategy and recommend partitioning approaches."
    
    Ready to begin your PostgreSQL analysis? Please describe your specific database challenge or diagnostic requirement.
    """

    return await run_agent_with_session(welcome_message, user_id)


logger.info(
    "PostgreSQL DBA Multi-Agent initialized with coordinator agent orchestrating specialized agents and MCP tools hosted on Cloud Run"
)
