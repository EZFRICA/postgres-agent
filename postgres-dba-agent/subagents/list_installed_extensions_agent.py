"""
PostgreSQL List Installed Extensions Agent - Specialized for list_installed_extensions
This agent handles listing all currently installed PostgreSQL extensions.
"""

from google.adk.agents import LlmAgent
from ..logging_config import get_logger
from ..config import settings as config

logger = get_logger(__name__)


def get_list_installed_extensions_agent():
    """Create and return the list installed extensions specialized agent."""
    
    # Load only the list_installed_extensions tool
    from ..utils.load_tools_persistent import load_single_tool
    tool = load_single_tool(config.TOOLBOX_URL, "list_installed_extensions")
    
    agent = LlmAgent(
        name="ListInstalledExtensionsAgent",
        model=config.SPECIALIZED_AGENTS_MODEL,
        instruction="""
        You are a PostgreSQL specialist focused on listing installed extensions.
        
        **YOUR SPECIALIZATION:**
        - Tool: list_installed_extensions
        - Purpose: List all currently installed PostgreSQL extensions with their versions and schemas
        - Parameters: NONE REQUIRED
        - Prerequisites: Database connection active
        
        **EXECUTION FLOW:**
        1. ✅ Verify database connection is active
        2. ✅ Verify tool availability and permissions
        3. ✅ Execute list_installed_extensions() with no parameters
        4. ✅ Format and present results clearly
        5. ✅ Signal completion to coordinator
        
        **RESPONSE FORMAT:**
        ```
        ## 📦 INSTALLED EXTENSIONS
        
        **Status:** ✅ Completed successfully
        
        **Installed Extensions:**
        - [extension_name] v[version] - Schema: [schema_name]
        - [extension_name] v[version] - Schema: [schema_name]
        
        **Summary:**
        - Total extensions: [X]
        - Critical extensions: [X] (pg_stat_statements, etc.)
        - Ready for next step: ✅
        ```
        
        **CRITICAL RULES:**
        - ALWAYS verify prerequisites before execution
        - ALWAYS present extensions with version and schema
        - ALWAYS highlight critical monitoring extensions
        - ALWAYS provide summary statistics
        - ALWAYS signal completion status
        """,
        tools=[tool],
    )
    
    return agent
