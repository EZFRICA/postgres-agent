"""
PostgreSQL Get Slowest Historical Queries Agent - Specialized for get_slowest_historical_queries
This agent handles Identifies the most expensive queries by total execution time from pg_stat_statements. Critical for historical performance analysis and identifying queries that need optimization priority..
"""

from google.adk.agents import LlmAgent
from ..logging_config import get_logger
from ..config import settings as config

logger = get_logger(__name__)


def get_slowest_historical_queries_agent():
    """Create and return the get_slowest_historical_queries specialized agent."""

    # Load only the get_slowest_historical_queries tool
    from ..utils.load_tools_persistent import load_single_tool

    tool = load_single_tool(config.TOOLBOX_URL, "get_slowest_historical_queries")

    agent = LlmAgent(
        name="GetslowesthistoricalqueriesAgent",
        model=config.SPECIALIZED_AGENTS_MODEL,
        instruction="""
        You are a PostgreSQL specialist focused on Identifies the most expensive queries by total execution time from pg_stat_statements.
        
        **YOUR SPECIALIZATION:**
        - Tool: get_slowest_historical_queries
        - Purpose: Identifies the most expensive queries by total execution time from pg_stat_statements. Critical for historical performance analysis and identifying queries that need optimization priority.
        - Parameters: limit (integer)
        - Prerequisites: Database connection active
        
        **EXECUTION FLOW:**
        1. ✅ Verify database connection is active
        2. ✅ Verify tool availability and permissions
        3. ✅ Execute get_slowest_historical_queries(limit) with required parameters
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
