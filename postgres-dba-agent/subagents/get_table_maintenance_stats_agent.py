"""
PostgreSQL Get Table Maintenance Stats Agent - Specialized for get_table_maintenance_stats
This agent handles Shows maintenance statistics (VACUUM/ANALYZE) for all tables or a specific table. Critical for diagnosing performance issues related to bloat and stale statistics..
"""

from google.adk.agents import LlmAgent
from ..logging_config import get_logger
from ..config import settings as config

logger = get_logger(__name__)


def get_table_maintenance_stats_agent():
    """Create and return the get_table_maintenance_stats specialized agent."""
    
    # Load only the get_table_maintenance_stats tool
    from ..utils.load_tools_persistent import load_single_tool
    tool = load_single_tool(config.TOOLBOX_URL, "get_table_maintenance_stats")
    
    agent = LlmAgent(
        name="GettablemaintenancestatsAgent",
        model=config.SPECIALIZED_AGENTS_MODEL,
        instruction="""
        You are a PostgreSQL specialist focused on Shows maintenance statistics (VACUUM/ANALYZE) for all tables or a specific table.
        
        **YOUR SPECIALIZATION:**
        - Tool: get_table_maintenance_stats
        - Purpose: Shows maintenance statistics (VACUUM/ANALYZE) for all tables or a specific table. Critical for diagnosing performance issues related to bloat and stale statistics.
        - Parameters: table_name (string)
        - Prerequisites: Database connection active
        
        **EXECUTION FLOW:**
        1. ✅ Verify database connection is active
        2. ✅ Verify tool availability and permissions
        3. ✅ Execute get_table_maintenance_stats(table_name) with required parameters
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
