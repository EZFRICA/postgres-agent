"""
PostgreSQL Find Invalid Indexes Agent - Specialized for find_invalid_indexes
This agent handles Detects invalid indexes in the database. Invalid indexes can result from errors during concurrent index creation and should be dropped and recreated..
"""

from google.adk.agents import LlmAgent
from ..logging_config import get_logger
from ..config import settings as config

logger = get_logger(__name__)


def get_find_invalid_indexes_agent():
    """Create and return the find_invalid_indexes specialized agent."""
    
    # Load only the find_invalid_indexes tool
    from ..utils.load_tools_persistent import load_single_tool
    tool = load_single_tool(config.TOOLBOX_URL, "find_invalid_indexes")
    
    agent = LlmAgent(
        name="FindinvalidindexesAgent",
        model=config.SPECIALIZED_AGENTS_MODEL,
        instruction="""
        You are a PostgreSQL specialist focused on Detects invalid indexes in the database.
        
        **YOUR SPECIALIZATION:**
        - Tool: find_invalid_indexes
        - Purpose: Detects invalid indexes in the database. Invalid indexes can result from errors during concurrent index creation and should be dropped and recreated.
        - Parameters: NONE REQUIRED
        - Prerequisites: Database connection active
        
        **EXECUTION FLOW:**
        1. ✅ Verify database connection is active
        2. ✅ Verify tool availability and permissions
        3. ✅ Execute find_invalid_indexes() with required parameters
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
