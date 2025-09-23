"""
PostgreSQL Get Most Frequent Queries Agent - Specialized for get_most_frequent_queries
This agent handles Identifies the most frequently executed queries. Useful for understanding usage patterns and identifying queries that are candidates for optimization or caching..
"""

from google.adk.agents import LlmAgent
from ..logging_config import get_logger
from ..config import settings as config

logger = get_logger(__name__)


def get_most_frequent_queries_agent():
    """Create and return the get_most_frequent_queries specialized agent."""
    
    # Load only the get_most_frequent_queries tool
    from ..utils.load_tools_persistent import load_single_tool
    tool = load_single_tool(config.TOOLBOX_URL, "get_most_frequent_queries")
    
    agent = LlmAgent(
        name="GetmostfrequentqueriesAgent",
        model=config.SPECIALIZED_AGENTS_MODEL,
        instruction="""
        You are a PostgreSQL specialist focused on Identifies the most frequently executed queries.
        
        **YOUR SPECIALIZATION:**
        - Tool: get_most_frequent_queries
        - Purpose: Identifies the most frequently executed queries. Useful for understanding usage patterns and identifying queries that are candidates for optimization or caching.
        - Parameters: limit (integer)
        - Prerequisites: Database connection active
        
        **EXECUTION FLOW:**
        1. ✅ Verify database connection is active
        2. ✅ Verify tool availability and permissions
        3. ✅ Execute get_most_frequent_queries(limit) with required parameters
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
