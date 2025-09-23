"""
PostgreSQL Get Current Connections Summary Agent - Specialized for get_current_connections_summary
This agent handles Shows a summary of active connections grouped by user and application. Complements the native list-active-queries tool with an aggregated view..
"""

from google.adk.agents import LlmAgent
from ..logging_config import get_logger
from ..config import settings as config

logger = get_logger(__name__)


def get_current_connections_summary_agent():
    """Create and return the get_current_connections_summary specialized agent."""
    
    # Load only the get_current_connections_summary tool
    from ..utils.load_tools_persistent import load_single_tool
    tool = load_single_tool(config.TOOLBOX_URL, "get_current_connections_summary")
    
    agent = LlmAgent(
        name="GetcurrentconnectionssummaryAgent",
        model=config.SPECIALIZED_AGENTS_MODEL,
        instruction="""
        You are a PostgreSQL specialist focused on Shows a summary of active connections grouped by user and application.
        
        **YOUR SPECIALIZATION:**
        - Tool: get_current_connections_summary
        - Purpose: Shows a summary of active connections grouped by user and application. Complements the native list-active-queries tool with an aggregated view.
        - Parameters: NONE REQUIRED
        - Prerequisites: Database connection active
        
        **EXECUTION FLOW:**
        1. ✅ Verify database connection is active
        2. ✅ Verify tool availability and permissions
        3. ✅ Execute get_current_connections_summary() with required parameters
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
