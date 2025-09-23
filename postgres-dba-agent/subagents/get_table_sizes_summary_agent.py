"""
PostgreSQL Get Table Sizes Summary Agent - Specialized for get_table_sizes_summary
This agent handles Provides a summary of table sizes sorted by descending size with data/index separation. Complements the native list-tables tool by focusing on capacity aspects..
"""

from google.adk.agents import LlmAgent
from ..logging_config import get_logger
from ..config import settings as config

logger = get_logger(__name__)


def get_table_sizes_summary_agent():
    """Create and return the get_table_sizes_summary specialized agent."""
    
    # Load only the get_table_sizes_summary tool
    from ..utils.load_tools_persistent import load_single_tool
    tool = load_single_tool(config.TOOLBOX_URL, "get_table_sizes_summary")
    
    agent = LlmAgent(
        name="GettablesizessummaryAgent",
        model=config.SPECIALIZED_AGENTS_MODEL,
        instruction="""
        You are a PostgreSQL specialist focused on Provides a summary of table sizes sorted by descending size with data/index separation.
        
        **YOUR SPECIALIZATION:**
        - Tool: get_table_sizes_summary
        - Purpose: Provides a summary of table sizes sorted by descending size with data/index separation. Complements the native list-tables tool by focusing on capacity aspects.
        - Parameters: schema_name (string), limit (integer)
        - Prerequisites: Database connection active
        
        **EXECUTION FLOW:**
        1. ✅ Verify database connection is active
        2. ✅ Verify tool availability and permissions
        3. ✅ Execute get_table_sizes_summary(schema_name, limit) with required parameters
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
