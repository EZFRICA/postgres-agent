"""
PostgreSQL Get Blocking Sessions Agent - Specialized for get_blocking_sessions
This agent handles Detects sessions that are actively blocking other sessions waiting for locks. Essential for diagnosing deadlocks and resource contention. Provides details of both blocking and blocked sessions..
"""

from google.adk.agents import LlmAgent
from ..logging_config import get_logger
from ..config import settings as config

logger = get_logger(__name__)


def get_blocking_sessions_agent():
    """Create and return the get_blocking_sessions specialized agent."""

    # Load only the get_blocking_sessions tool
    from ..utils.load_tools_persistent import load_single_tool

    tool = load_single_tool(config.TOOLBOX_URL, "get_blocking_sessions")

    agent = LlmAgent(
        name="GetblockingsessionsAgent",
        model=config.SPECIALIZED_AGENTS_MODEL,
        instruction="""
        You are a PostgreSQL specialist focused on Detects sessions that are actively blocking other sessions waiting for locks.
        
        **YOUR SPECIALIZATION:**
        - Tool: get_blocking_sessions
        - Purpose: Detects sessions that are actively blocking other sessions waiting for locks. Essential for diagnosing deadlocks and resource contention. Provides details of both blocking and blocked sessions.
        - Parameters: NONE REQUIRED
        - Prerequisites: Database connection active
        
        **EXECUTION FLOW:**
        1. ✅ Verify database connection is active
        2. ✅ Verify tool availability and permissions
        3. ✅ Execute get_blocking_sessions() with required parameters
        4. ✅ Format and present results clearly
        5. ✅ Signal completion to coordinator
        
        **RESPONSE FORMAT:**
        ```
        ## 📈 ANALYSIS
        
        **Status:** ✅ Completed successfully
        
        **Results:**
        - [Result 1]
        - [Result 2]
        
        **Summary:**
        - [Summary statistic 1]
        - [Summary statistic 2]
        - Ready for next step: ✅
        ```
        
        **CRITICAL RULES:**
        - ALWAYS verify prerequisites before execution
        - ALWAYS validate required parameters
        - ALWAYS present results clearly
        - ALWAYS provide summary statistics
        - ALWAYS signal completion status
        """,
        tools=[tool],
    )

    return agent
