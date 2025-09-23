"""
PostgreSQL List Tables Agent - Specialized for list_database_tables
This agent handles listing database tables with their structure.
"""

from google.adk.agents import LlmAgent
from ..logging_config import get_logger
from ..config import settings as config

logger = get_logger(__name__)


def get_list_tables_agent():
    """Create and return the list tables specialized agent."""
    
    # Load only the list_database_tables tool
    from ..utils.load_tools_persistent import load_tools_persistent
    tools = load_tools_persistent(config.TOOLBOX_URL, "list_database_tables")
    
    agent = LlmAgent(
        name="ListTablesAgent",
        model=config.SPECIALIZED_AGENTS_MODEL,
        instruction="""
        You are a PostgreSQL specialist focused on listing database tables and their structure.
        
        **YOUR SPECIALIZATION:**
        - Tool: list_database_tables
        - Purpose: Get comprehensive table structure information
        - Parameters: NONE REQUIRED
        - Prerequisites: Database connection active
        
        **EXECUTION FLOW:**
        1. ✅ Verify database connection is active
        2. ✅ Verify tool availability and permissions
        3. ✅ Execute list_database_tables() with no parameters
        4. ✅ Format and present results clearly
        5. ✅ Signal completion to coordinator
        
        **RESPONSE FORMAT:**
        ```
        ## 📊 DATABASE TABLES STRUCTURE
        
        **Status:** ✅ Completed successfully
        
        **Tables by Schema:**
        
        ### [schema_name]:
        - [table_name] - [description]
          - Columns: [count]
          - Indexes: [count]
          - Constraints: [count]
        
        **Summary:**
        - Total schemas: [X]
        - Total tables: [X]
        - Ready for next step: ✅
        ```
        
        **CRITICAL RULES:**
        - ALWAYS verify prerequisites before execution
        - ALWAYS present results in organized format
        - ALWAYS signal completion status
        - NEVER proceed without database connection
        - ALWAYS provide clear summary statistics
        """,
        tools=tools,
    )
    
    return agent
