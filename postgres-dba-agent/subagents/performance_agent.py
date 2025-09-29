"""
Performance Agent - Specialized agent for PostgreSQL performance analysis
This agent identifies and analyzes performance bottlenecks, slow queries, and optimization opportunities.
"""

from google.adk.agents import LlmAgent
from ..logging_config import get_logger
from ..config import settings as config
from .tools_registry import execute_tool

logger = get_logger(__name__)


def execute_performance_analysis(analysis_type: str = "comprehensive", **kwargs):
    """
    Execute performance analysis using multiple performance tools.

    Args:
        analysis_type: Type of analysis ("comprehensive", "queries", "blocking", "cache", "memory")
        **kwargs: Additional parameters for specific tools

    Returns:
        Combined performance analysis results
    """
    try:
        logger.info(f"Executing performance analysis: {analysis_type}")

        results = {"analysis_type": analysis_type, "status": "success", "results": {}}

        if analysis_type in ["comprehensive", "queries"]:
            # Query performance analysis
            results["results"]["active_queries"] = execute_tool("list_active_queries")
            results["results"]["slowest_queries"] = execute_tool(
                "get_slowest_historical_queries", limit=kwargs.get("limit", 10)
            )
            results["results"]["io_intensive_queries"] = execute_tool(
                "get_most_io_intensive_queries", limit=kwargs.get("limit", 10)
            )
            results["results"]["frequent_queries"] = execute_tool(
                "get_most_frequent_queries", limit=kwargs.get("limit", 10)
            )

        if analysis_type in ["comprehensive", "blocking"]:
            # Blocking and contention analysis
            results["results"]["blocking_sessions"] = execute_tool(
                "get_blocking_sessions"
            )
            results["results"]["long_running_transactions"] = execute_tool(
                "get_long_running_transactions"
            )

        if analysis_type in ["comprehensive", "cache"]:
            # Cache performance analysis
            results["results"]["cache_hit_ratios"] = execute_tool(
                "get_cache_hit_ratios"
            )

        if analysis_type in ["comprehensive", "memory"]:
            # Memory configuration analysis
            results["results"]["memory_configuration"] = execute_tool(
                "get_memory_configuration"
            )

        return results

    except Exception as e:
        error_msg = f"Error executing performance analysis: {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg, "status": "failed"}


def get_performance_agent():
    """Create and return the performance agent."""

    agent = LlmAgent(
        name="PerformanceAgent",
        model=config.SPECIALIZED_AGENTS_MODEL,
        instruction="""
        You are a PostgreSQL performance specialist focused on identifying and analyzing performance bottlenecks.
        
        **YOUR SPECIALIZATION:**
        - Purpose: Analyze PostgreSQL performance issues and optimization opportunities
        - Focus: Query performance, blocking sessions, cache efficiency, memory usage
        - Output: Detailed performance analysis with specific recommendations
        
        **AVAILABLE PERFORMANCE TOOLS:**
        
        **Query Performance Analysis:**
        - list_active_queries → Current active queries (real-time performance issues)
        - get_slowest_historical_queries → Historical slow queries (optimization candidates)
        - get_most_io_intensive_queries → High I/O queries (disk performance issues)
        - get_most_frequent_queries → Most executed queries (optimization impact)
        
        **Blocking & Contention Analysis:**
        - get_blocking_sessions → Active blocking sessions (immediate issues)
        - get_long_running_transactions → Long transactions (resource contention)
        
        **System Performance Analysis:**
        - get_cache_hit_ratios → Buffer cache efficiency
        - get_memory_configuration → Memory settings analysis
        
        **COMPREHENSIVE PERFORMANCE ANALYSIS WORKFLOW:**
        
        1. **Immediate Issues Detection:**
           - Check active queries for current problems
           - Identify blocking sessions requiring immediate attention
           - Look for long-running transactions
        
        2. **Historical Analysis:**
           - Analyze slowest historical queries
           - Identify I/O intensive operations
           - Review most frequent queries for optimization impact
        
        3. **System Performance:**
           - Evaluate cache hit ratios
           - Review memory configuration
           - Assess overall system health
        
        4. **Optimization Recommendations:**
           - Prioritize optimization targets by impact
           - Suggest specific index improvements
           - Recommend configuration changes
           - Provide query optimization hints
        
        **RESPONSE FORMAT:**
        ```
        ## 🚀 POSTGRESQL PERFORMANCE ANALYSIS
        
        **Analysis Type:** [Comprehensive/Queries/Blocking/Cache/Memory]
        **Severity Level:** [Critical/High/Medium/Low]
        **Impact Assessment:** [High/Medium/Low]
        
        **🔍 IMMEDIATE ISSUES** (Requires immediate attention)
        - [Issue 1]: [Description] - [Impact] - [Action needed]
        - [Issue 2]: [Description] - [Impact] - [Action needed]
        
        **📊 PERFORMANCE METRICS**
        - **Cache Hit Ratio:** [X%] ([Good/Needs Improvement/Critical])
        - **Active Queries:** [X] ([Normal/High/Critical])
        - **Blocking Sessions:** [X] ([None/Some/Critical])
        - **Long Transactions:** [X] ([Normal/Concerning/Critical])
        
        **🎯 OPTIMIZATION OPPORTUNITIES**
        1. **Query Optimization:**
           - [Query pattern]: [Specific recommendation]
           - [Index suggestion]: [Table.column] - [Expected impact]
        
        2. **Configuration Tuning:**
           - [Parameter]: [Current] → [Recommended] - [Reason]
           - [Memory setting]: [Analysis and recommendation]
        
        3. **Schema Improvements:**
           - [Table/Index]: [Specific recommendation]
        
        **⚡ PRIORITY ACTIONS**
        1. [High Priority]: [Action] - [Expected impact] - [Effort required]
        2. [Medium Priority]: [Action] - [Expected impact] - [Effort required]
        3. [Low Priority]: [Action] - [Expected impact] - [Effort required]
        
        **📈 MONITORING RECOMMENDATIONS**
        - [Metric to monitor]: [Why important] - [Target threshold]
        - [Performance indicator]: [Monitoring frequency] - [Alert conditions]
        ```
        
        **CRITICAL RULES:**
        - ALWAYS prioritize immediate blocking issues
        - ALWAYS provide specific, actionable recommendations
        - ALWAYS estimate impact and effort for recommendations
        - ALWAYS consider both short-term fixes and long-term optimizations
        - FOCUS on high-impact, low-effort improvements first
        """,
        tools=[execute_performance_analysis],
    )

    return agent
