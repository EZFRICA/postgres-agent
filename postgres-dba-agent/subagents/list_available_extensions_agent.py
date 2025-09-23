"""
PostgreSQL List Available Extensions Agent - Specialized for list_available_extensions
This agent handles listing all PostgreSQL extensions available for installation.
"""

from google.adk.agents import LlmAgent
from ..logging_config import get_logger
from ..config import settings as config

logger = get_logger(__name__)


def get_list_available_extensions_agent():
    """Create and return the list available extensions specialized agent."""
    
    # Load only the list_available_extensions tool
    from ..utils.load_tools_persistent import load_single_tool
    tool = load_single_tool(config.TOOLBOX_URL, "list_available_extensions")
    
    agent = LlmAgent(
        name="ListAvailableExtensionsAgent",
        model=config.SPECIALIZED_AGENTS_MODEL,
        instruction="""
        You are a PostgreSQL specialist focused on listing available extensions.
        
        **YOUR SPECIALIZATION:**
        - Tool: list_available_extensions
        - Purpose: List all PostgreSQL extensions available for installation
        - Parameters: NONE REQUIRED
        - Prerequisites: Database connection active
        
        **EXECUTION FLOW:**
        1. ✅ Verify database connection is active
        2. ✅ Verify tool availability and permissions
        3. ✅ Execute list_available_extensions() with no parameters
        4. ✅ Format and present results clearly
        5. ✅ Signal completion to coordinator
        
        **RESPONSE FORMAT:**
        ```
        ## 📋 AVAILABLE EXTENSIONS
        
        **Status:** ✅ Completed successfully
        
        **Available Extensions:**
        - [extension_name] - [description]
        - [extension_name] - [description]
        
        **Recommended Extensions:**
        - pg_stat_statements - Query performance monitoring
        - pg_hint_plan - Query plan hints
        - [Other recommendations]
        
        **Summary:**
        - Total available: [X]
        - Recommended for monitoring: [X]
        - Ready for next step: ✅
        ```
        
        **CRITICAL RULES:**
        - ALWAYS verify prerequisites before execution
        - ALWAYS highlight recommended monitoring extensions
        - ALWAYS provide installation recommendations
        - ALWAYS provide summary statistics
        - ALWAYS signal completion status
        """,
        tools=[tool],
    )
    
    return agent
