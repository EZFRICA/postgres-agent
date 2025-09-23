"""
PostgreSQL Get Unused Indexes Agent - Specialized for get_unused_indexes
This agent handles Identifies indexes that are rarely or never used which could be candidates for removal. Based on index usage statistics..
"""

from google.adk.agents import LlmAgent
from ..logging_config import get_logger
from ..config import settings as config

logger = get_logger(__name__)


def get_unused_indexes_agent():
    """Create and return the get_unused_indexes specialized agent."""
    
    # Load only the get_unused_indexes tool
    from ..utils.load_tools_persistent import load_single_tool
    tool = load_single_tool(config.TOOLBOX_URL, "get_unused_indexes")
    
    agent = LlmAgent(
        name="GetunusedindexesAgent",
        model=config.SPECIALIZED_AGENTS_MODEL,
        instruction="""
        You are a PostgreSQL specialist focused on Identifies indexes that are rarely or never used which could be candidates for removal.
        
        **YOUR SPECIALIZATION:**
        - Tool: get_unused_indexes
        - Purpose: Identifies indexes that are rarely or never used which could be candidates for removal. Based on index usage statistics.
        - Parameters: min_size_mb (integer)
        - Prerequisites: Database connection active
        
        **EXECUTION FLOW:**
        1. ✅ Verify database connection is active
        2. ✅ Verify tool availability and permissions
        3. ✅ Execute get_unused_indexes(min_size_mb) with required parameters
        4. ✅ Format and present results clearly
        5. ✅ Signal completion to coordinator
        
        **RESPONSE FORMAT:**
        ```
        ## 📊 SCHEMA ANALYSIS
        
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
