"""
PostgreSQL Get Database Users And Roles Agent - Specialized for get_database_users_and_roles
This agent handles Lists all database roles/users with their attributes and privileges. Essential for security auditing and access management..
"""

from google.adk.agents import LlmAgent
from ..logging_config import get_logger
from ..config import settings as config

logger = get_logger(__name__)


def get_database_users_and_roles_agent():
    """Create and return the get_database_users_and_roles specialized agent."""

    # Load only the get_database_users_and_roles tool
    from ..utils.load_tools_persistent import load_single_tool

    tool = load_single_tool(config.TOOLBOX_URL, "get_database_users_and_roles")

    agent = LlmAgent(
        name="GetdatabaseusersandrolesAgent",
        model=config.SPECIALIZED_AGENTS_MODEL,
        instruction="""
        You are a PostgreSQL specialist focused on Lists all database roles/users with their attributes and privileges.
        
        **YOUR SPECIALIZATION:**
        - Tool: get_database_users_and_roles
        - Purpose: Lists all database roles/users with their attributes and privileges. Essential for security auditing and access management.
        - Parameters: NONE REQUIRED
        - Prerequisites: Database connection active
        
        **EXECUTION FLOW:**
        1. ✅ Verify database connection is active
        2. ✅ Verify tool availability and permissions
        3. ✅ Execute get_database_users_and_roles() with required parameters
        4. ✅ Format and present results clearly
        5. ✅ Signal completion to coordinator
        
        **RESPONSE FORMAT:**
        ```
        ## 🔒 SECURITY ANALYSIS
        
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
