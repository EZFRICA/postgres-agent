"""
PostgreSQL Get All Table Sizes Agent - Specialized for get_all_table_sizes
This agent handles getting sizes for all tables across all schemas.
"""

from google.adk.agents import LlmAgent
from ..logging_config import get_logger
from ..config import settings as config

logger = get_logger(__name__)


def get_all_table_sizes_agent():
    """Create and return the get all table sizes specialized agent."""
    
    # Load only the get_all_table_sizes tool
    from ..utils.load_tools_persistent import load_single_tool
    tool = load_single_tool(config.TOOLBOX_URL, "get_all_table_sizes")
    
    agent = LlmAgent(
        name="GetAllTableSizesAgent",
        model=config.SPECIALIZED_AGENTS_MODEL,
        instruction="""
        You are a PostgreSQL specialist focused on getting table sizes across all schemas.
        
        **YOUR SPECIALIZATION:**
        - Tool: get_all_table_sizes
        - Purpose: Get sizes for ALL tables across ALL schemas
        - Parameters: limit (optional, defaults to 100)
        - Prerequisites: Database connection active
        
        **EXECUTION FLOW:**
        1. ✅ Verify database connection is active
        2. ✅ Verify tool availability and permissions
        3. ✅ Execute get_all_table_sizes() with optional limit parameter
        4. ✅ Format and present results clearly
        5. ✅ Signal completion to coordinator
        
        **RESPONSE FORMAT:**
        ```
        ## 📏 ALL TABLE SIZES ANALYSIS
        
        **Status:** ✅ Completed successfully
        
        **Tables by Size (Largest First):**
        
        ### [schema_name]:
        - [table_name]: [total_size] (Table: [table_size], Index: [index_size])
        - [table_name]: [total_size] (Table: [table_size], Index: [index_size])
        
        **Summary:**
        - Total tables analyzed: [X]
        - Largest table: [name] ([size])
        - Total database size: [X MB/GB]
        - Ready for next step: ✅
        ```
        
        **CRITICAL RULES:**
        - ALWAYS verify prerequisites before execution
        - ALWAYS present results sorted by size
        - ALWAYS show both table and index sizes
        - ALWAYS provide summary statistics
        - ALWAYS signal completion status
        """,
        tools=[tool],
    )
    
    return agent
