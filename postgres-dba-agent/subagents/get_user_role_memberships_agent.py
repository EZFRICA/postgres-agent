"""
PostgreSQL Get User Role Memberships Agent - Specialized for get_user_role_memberships
This agent handles Lists all roles that a specific user is a member of, directly or through inheritance. Important for understanding effective permissions..
"""

from google.adk.agents import LlmAgent
from ..logging_config import get_logger
from ..config import settings as config

logger = get_logger(__name__)


def get_user_role_memberships_agent():
    """Create and return the get_user_role_memberships specialized agent."""

    # Load only the get_user_role_memberships tool
    from ..utils.load_tools_persistent import load_single_tool

    tool = load_single_tool(config.TOOLBOX_URL, "get_user_role_memberships")

    agent = LlmAgent(
        name="GetuserrolemembershipsAgent",
        model=config.SPECIALIZED_AGENTS_MODEL,
        instruction="""
        You are a PostgreSQL specialist focused on Lists all roles that a specific user is a member of, directly or through inheritance.
        
        **YOUR SPECIALIZATION:**
        - Tool: get_user_role_memberships
        - Purpose: Lists all roles that a specific user is a member of, directly or through inheritance. Important for understanding effective permissions.
        - Parameters: username (string)
        - Prerequisites: Database connection active
        
        **EXECUTION FLOW:**
        1. ✅ Verify database connection is active
        2. ✅ Verify tool availability and permissions
        3. ✅ Execute get_user_role_memberships(username) with required parameters
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
