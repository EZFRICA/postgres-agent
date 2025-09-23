"""
PostgreSQL Get User Table Permissions Agent - Specialized for get_user_table_permissions
This agent handles Shows specific permissions for a user on a given table. Useful for diagnosing access issues and verifying permissions..
"""

from google.adk.agents import LlmAgent
from ..logging_config import get_logger
from ..config import settings as config

logger = get_logger(__name__)


def get_user_table_permissions_agent():
    """Create and return the get_user_table_permissions specialized agent."""

    # Load only the get_user_table_permissions tool
    from ..utils.load_tools_persistent import load_single_tool

    tool = load_single_tool(config.TOOLBOX_URL, "get_user_table_permissions")

    agent = LlmAgent(
        name="GetusertablepermissionsAgent",
        model=config.SPECIALIZED_AGENTS_MODEL,
        instruction="""
        You are a PostgreSQL specialist focused on Shows specific permissions for a user on a given table.
        
        **YOUR SPECIALIZATION:**
        - Tool: get_user_table_permissions
        - Purpose: Shows specific permissions for a user on a given table. Useful for diagnosing access issues and verifying permissions.
        - Parameters: table_name (string), username (string)
        - Prerequisites: Database connection active
        
        **EXECUTION FLOW:**
        1. ✅ Verify database connection is active
        2. ✅ Verify tool availability and permissions
        3. ✅ Execute get_user_table_permissions(table_name, username) with required parameters
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
