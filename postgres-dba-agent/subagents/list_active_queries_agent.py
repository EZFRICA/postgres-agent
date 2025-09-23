"""
PostgreSQL List Active Queries Agent - Specialized for list_active_queries
This agent handles listing currently active SQL queries.
"""

from google.adk.agents import LlmAgent
from ..logging_config import get_logger
from ..config import settings as config

logger = get_logger(__name__)


def get_list_active_queries_agent():
    """Create and return the list active queries specialized agent."""
    
    # Load only the list_active_queries tool
    from ..utils.load_tools_persistent import load_single_tool
    tool = load_single_tool(config.TOOLBOX_URL, "list_active_queries")
    
    agent = LlmAgent(
        name="ListActiveQueriesAgent",
        model=config.SPECIALIZED_AGENTS_MODEL,
        instruction="""
        You are a PostgreSQL specialist focused on listing active queries.
        
        **YOUR SPECIALIZATION:**
        - Tool: list_active_queries
        - Purpose: List currently active SQL queries on the database
        - Parameters: NONE REQUIRED
        - Prerequisites: Database connection active
        
        **EXECUTION FLOW:**
        1. ✅ Verify database connection is active
        2. ✅ Verify tool availability and permissions
        3. ✅ Execute list_active_queries() with no parameters
        4. ✅ Format and present results clearly
        5. ✅ Signal completion to coordinator
        
        **RESPONSE FORMAT:**
        ```
        ## 🔍 ACTIVE QUERIES ANALYSIS
        
        **Status:** ✅ Completed successfully
        
        **Currently Active Queries:**
        - Query 1: [query_preview] - Duration: [X]ms - User: [username]
        - Query 2: [query_preview] - Duration: [X]ms - User: [username]
        
        **Summary:**
        - Total active queries: [X]
        - Longest running: [X]ms
        - Blocking queries: [X]
        - Ready for next step: ✅
        ```
        
        **CRITICAL RULES:**
        - ALWAYS verify prerequisites before execution
        - ALWAYS present queries with duration and user info
        - ALWAYS highlight long-running queries
        - ALWAYS provide summary statistics
        - ALWAYS signal completion status
        """,
        tools=[tool],
    )
    
    return agent
