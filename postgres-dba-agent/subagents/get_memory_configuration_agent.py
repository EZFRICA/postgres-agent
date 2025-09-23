"""
PostgreSQL Get Memory Configuration Agent - Specialized for get_memory_configuration
This agent handles Shows critical PostgreSQL memory configuration parameters. Essential for diagnosing performance issues related to memory allocation..
"""

from google.adk.agents import LlmAgent
from ..logging_config import get_logger
from ..config import settings as config

logger = get_logger(__name__)


def get_memory_configuration_agent():
    """Create and return the get_memory_configuration specialized agent."""
    
    # Load only the get_memory_configuration tool
    from ..utils.load_tools_persistent import load_single_tool
    tool = load_single_tool(config.TOOLBOX_URL, "get_memory_configuration")
    
    agent = LlmAgent(
        name="GetmemoryconfigurationAgent",
        model=config.SPECIALIZED_AGENTS_MODEL,
        instruction="""
        You are a PostgreSQL specialist focused on Shows critical PostgreSQL memory configuration parameters.
        
        **YOUR SPECIALIZATION:**
        - Tool: get_memory_configuration
        - Purpose: Shows critical PostgreSQL memory configuration parameters. Essential for diagnosing performance issues related to memory allocation.
        - Parameters: NONE REQUIRED
        - Prerequisites: Database connection active
        
        **EXECUTION FLOW:**
        1. ✅ Verify database connection is active
        2. ✅ Verify tool availability and permissions
        3. ✅ Execute get_memory_configuration() with required parameters
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
