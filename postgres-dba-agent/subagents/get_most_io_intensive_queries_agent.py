"""
PostgreSQL Get Most Io Intensive Queries Agent - Specialized for get_most_io_intensive_queries
This agent handles Identifies queries that consume the most disk I/O by analyzing block reads. Critical for diagnosing disk performance issues and identifying queries needing index optimization..
"""

from google.adk.agents import LlmAgent
from ..logging_config import get_logger
from ..config import settings as config

logger = get_logger(__name__)


def get_most_io_intensive_queries_agent():
    """Create and return the get_most_io_intensive_queries specialized agent."""
    
    # Load only the get_most_io_intensive_queries tool
    from ..utils.load_tools_persistent import load_single_tool
    tool = load_single_tool(config.TOOLBOX_URL, "get_most_io_intensive_queries")
    
    agent = LlmAgent(
        name="GetmostiointensivequeriesAgent",
        model=config.SPECIALIZED_AGENTS_MODEL,
        instruction="""
        You are a PostgreSQL specialist focused on Identifies queries that consume the most disk I/O by analyzing block reads.
        
        **YOUR SPECIALIZATION:**
        - Tool: get_most_io_intensive_queries
        - Purpose: Identifies queries that consume the most disk I/O by analyzing block reads. Critical for diagnosing disk performance issues and identifying queries needing index optimization.
        - Parameters: limit (integer)
        - Prerequisites: Database connection active
        
        **EXECUTION FLOW:**
        1. ✅ Verify database connection is active
        2. ✅ Verify tool availability and permissions
        3. ✅ Execute get_most_io_intensive_queries(limit) with required parameters
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
