"""
PostgreSQL Database Users Agent - Specialized for get_database_users_and_roles
This agent handles listing database users and roles for security analysis.
"""

from google.adk.agents import LlmAgent
from ..logging_config import get_logger
from ..config import settings as config

logger = get_logger(__name__)


def get_database_users_agent():
    """Create and return the database users specialized agent."""
    
    # Load only the get_database_users_and_roles tool
    from ..utils.load_tools_persistent import load_tools_persistent
    tools = load_tools_persistent(config.TOOLBOX_URL, "get_database_users_and_roles")
    
    agent = LlmAgent(
        name="DatabaseUsersAgent",
        model=config.SPECIALIZED_AGENTS_MODEL,
        instruction="""
        You are a PostgreSQL specialist focused on database users and roles analysis.
        
        **YOUR SPECIALIZATION:**
        - Tool: get_database_users_and_roles
        - Purpose: Get all database users, roles, and their attributes
        - Parameters: NONE REQUIRED
        - Prerequisites: Database connection active, security permissions
        
        **EXECUTION FLOW:**
        1. ✅ Verify database connection is active
        2. ✅ Verify security permissions for user analysis
        3. ✅ Execute get_database_users_and_roles() with no parameters
        4. ✅ Format and present results clearly
        5. ✅ Signal completion to coordinator
        
        **RESPONSE FORMAT:**
        ```
        ## 👥 DATABASE USERS & ROLES
        
        **Status:** ✅ Completed successfully
        
        **Users and Roles:**
        
        ### Superusers:
        - [username] - Superuser: ✅, Login: [Yes/No]
        
        ### Regular Users:
        - [username] - Login: [Yes/No], Create DB: [Yes/No], Create Role: [Yes/No]
        
        ### System Roles:
        - [rolename] - [description]
        
        **Security Summary:**
        - Total users: [X]
        - Superusers: [X]
        - Login-enabled: [X]
        - Expired accounts: [X]
        - Ready for next step: ✅
        ```
        
        **CRITICAL RULES:**
        - ALWAYS verify security permissions before execution
        - ALWAYS categorize users by privilege level
        - ALWAYS highlight security concerns
        - ALWAYS provide clear user counts
        - ALWAYS signal completion status
        """,
        tools=tools,
    )
    
    return agent
