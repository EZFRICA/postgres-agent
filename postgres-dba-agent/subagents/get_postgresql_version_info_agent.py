"""
PostgreSQL Get Postgresql Version Info Agent - Specialized for get_postgresql_version_info
This agent handles Returns the complete PostgreSQL version with compilation details. Useful for verifying version and identifying available features..
"""

from google.adk.agents import LlmAgent
from ..logging_config import get_logger
from ..config import settings as config

logger = get_logger(__name__)


def get_postgresql_version_info_agent():
    """Create and return the get_postgresql_version_info specialized agent."""

    # Load only the get_postgresql_version_info tool
    from ..utils.load_tools_persistent import load_single_tool

    tool = load_single_tool(config.TOOLBOX_URL, "get_postgresql_version_info")

    agent = LlmAgent(
        name="GetpostgresqlversioninfoAgent",
        model=config.SPECIALIZED_AGENTS_MODEL,
        instruction="""
        You are a PostgreSQL specialist focused on Returns the complete PostgreSQL version with compilation details.
        
        **YOUR SPECIALIZATION:**
        - Tool: get_postgresql_version_info
        - Purpose: Returns the complete PostgreSQL version with compilation details. Useful for verifying version and identifying available features.
        - Parameters: NONE REQUIRED
        - Prerequisites: Database connection active
        
        **EXECUTION FLOW:**
        1. ✅ Verify database connection is active
        2. ✅ Verify tool availability and permissions
        3. ✅ Execute get_postgresql_version_info() with required parameters
        4. ✅ Format and present results clearly
        5. ✅ Signal completion to coordinator
        
        **RESPONSE FORMAT:**
        ```
        ## 📈 ANALYSIS
        
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
