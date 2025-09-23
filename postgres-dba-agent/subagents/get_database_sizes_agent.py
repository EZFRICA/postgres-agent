"""
PostgreSQL Get Database Sizes Agent - Specialized for get_database_sizes
This agent handles Shows the size of all databases on the PostgreSQL server. Essential for capacity planning and monitoring disk usage..
"""

from google.adk.agents import LlmAgent
from ..logging_config import get_logger
from ..config import settings as config

logger = get_logger(__name__)


def get_database_sizes_agent():
    """Create and return the get_database_sizes specialized agent."""
    
    # Load only the get_database_sizes tool
    from ..utils.load_tools_persistent import load_single_tool
    tool = load_single_tool(config.TOOLBOX_URL, "get_database_sizes")
    
    agent = LlmAgent(
        name="GetdatabasesizesAgent",
        model=config.SPECIALIZED_AGENTS_MODEL,
        instruction="""
        You are a PostgreSQL specialist focused on Shows the size of all databases on the PostgreSQL server.
        
        **YOUR SPECIALIZATION:**
        - Tool: get_database_sizes
        - Purpose: Shows the size of all databases on the PostgreSQL server. Essential for capacity planning and monitoring disk usage.
        - Parameters: NONE REQUIRED
        - Prerequisites: Database connection active
        
        **EXECUTION FLOW:**
        1. ✅ Verify database connection is active
        2. ✅ Verify tool availability and permissions
        3. ✅ Execute get_database_sizes() with required parameters
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
