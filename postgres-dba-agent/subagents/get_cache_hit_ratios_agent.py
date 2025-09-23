"""
PostgreSQL Get Cache Hit Ratios Agent - Specialized for get_cache_hit_ratios
This agent handles Calculates cache hit ratios to assess PostgreSQL cache effectiveness. Low ratios may indicate a need to increase shared_buffers..
"""

from google.adk.agents import LlmAgent
from ..logging_config import get_logger
from ..config import settings as config

logger = get_logger(__name__)


def get_cache_hit_ratios_agent():
    """Create and return the get_cache_hit_ratios specialized agent."""
    
    # Load only the get_cache_hit_ratios tool
    from ..utils.load_tools_persistent import load_single_tool
    tool = load_single_tool(config.TOOLBOX_URL, "get_cache_hit_ratios")
    
    agent = LlmAgent(
        name="GetcachehitratiosAgent",
        model=config.SPECIALIZED_AGENTS_MODEL,
        instruction="""
        You are a PostgreSQL specialist focused on Calculates cache hit ratios to assess PostgreSQL cache effectiveness.
        
        **YOUR SPECIALIZATION:**
        - Tool: get_cache_hit_ratios
        - Purpose: Calculates cache hit ratios to assess PostgreSQL cache effectiveness. Low ratios may indicate a need to increase shared_buffers.
        - Parameters: NONE REQUIRED
        - Prerequisites: Database connection active
        
        **EXECUTION FLOW:**
        1. ✅ Verify database connection is active
        2. ✅ Verify tool availability and permissions
        3. ✅ Execute get_cache_hit_ratios() with required parameters
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
