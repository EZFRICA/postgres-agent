"""
PostgreSQL Get Replication Status Agent - Specialized for get_replication_status
This agent handles Shows PostgreSQL replication status (if configured). Essential for monitoring replica health and diagnosing replication lag..
"""

from google.adk.agents import LlmAgent
from ..logging_config import get_logger
from ..config import settings as config

logger = get_logger(__name__)


def get_replication_status_agent():
    """Create and return the get_replication_status specialized agent."""

    # Load only the get_replication_status tool
    from ..utils.load_tools_persistent import load_single_tool

    tool = load_single_tool(config.TOOLBOX_URL, "get_replication_status")

    agent = LlmAgent(
        name="GetreplicationstatusAgent",
        model=config.SPECIALIZED_AGENTS_MODEL,
        instruction="""
        You are a PostgreSQL specialist focused on Shows PostgreSQL replication status (if configured).
        
        **YOUR SPECIALIZATION:**
        - Tool: get_replication_status
        - Purpose: Shows PostgreSQL replication status (if configured). Essential for monitoring replica health and diagnosing replication lag.
        - Parameters: NONE REQUIRED
        - Prerequisites: Database connection active
        
        **EXECUTION FLOW:**
        1. ✅ Verify database connection is active
        2. ✅ Verify tool availability and permissions
        3. ✅ Execute get_replication_status() with required parameters
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
