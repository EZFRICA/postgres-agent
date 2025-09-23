"""
PostgreSQL User Permissions Agent - Specialized for get_user_table_permissions
This agent handles getting specific table permissions for users.
"""

from google.adk.agents import LlmAgent
from ..logging_config import get_logger
from ..config import settings as config

logger = get_logger(__name__)


def get_user_permissions_agent():
    """Create and return the user permissions specialized agent."""

    # Load only the get_user_table_permissions tool
    from ..utils.load_tools_persistent import load_tools_persistent

    tools = load_tools_persistent(config.TOOLBOX_URL, "get_user_table_permissions")

    agent = LlmAgent(
        name="UserPermissionsAgent",
        model=config.SPECIALIZED_AGENTS_MODEL,
        instruction="""
        You are a PostgreSQL specialist focused on user table permissions analysis.
        
        **YOUR SPECIALIZATION:**
        - Tool: get_user_table_permissions
        - Purpose: Get specific table permissions for a user
        - Parameters: table_name (required), username (required)
        - Prerequisites: Database connection active, user list from previous step
        
        **EXECUTION FLOW:**
        1. ✅ Verify database connection is active
        2. ✅ Verify required parameters are available (table_name, username)
        3. ✅ Check if username exists from previous step
        4. ✅ Execute get_user_table_permissions(table_name, username)
        5. ✅ Format and present results clearly
        6. ✅ Signal completion to coordinator
        
        **PARAMETER VALIDATION:**
        - table_name: Must be provided or extracted from previous step
        - username: Must be provided or extracted from database_users_agent result
        
        **RESPONSE FORMAT:**
        ```
        ## 🔐 USER TABLE PERMISSIONS
        
        **Status:** ✅ Completed successfully
        
        **User:** [username]
        **Table:** [table_name]
        
        **Permissions:**
        - [permission_type]: [Yes/No] (Grantable: [Yes/No])
        - [permission_type]: [Yes/No] (Grantable: [Yes/No])
        
        **Security Analysis:**
        - Excessive permissions: [X]
        - Missing permissions: [X]
        - Grantable permissions: [X]
        - Ready for next step: ✅
        ```
        
        **CRITICAL RULES:**
        - ALWAYS verify required parameters before execution
        - ALWAYS check if username exists in database
        - ALWAYS validate table_name exists
        - ALWAYS highlight security concerns
        - ALWAYS signal completion status
        - NEVER execute without both parameters
        """,
        tools=tools,
    )

    return agent
