"""
PostgreSQL Get Long Running Transactions Agent - Specialized for get_long_running_transactions
This agent handles Identifies transactions that have been open for a long time which can cause bloat, replication, and performance issues. Transactions in 'idle in transaction' state are particularly problematic..
"""

from google.adk.agents import LlmAgent
from ..logging_config import get_logger
from ..config import settings as config

logger = get_logger(__name__)


def get_long_running_transactions_agent():
    """Create and return the get_long_running_transactions specialized agent."""

    # Load only the get_long_running_transactions tool
    from ..utils.load_tools_persistent import load_single_tool

    tool = load_single_tool(config.TOOLBOX_URL, "get_long_running_transactions")

    agent = LlmAgent(
        name="GetlongrunningtransactionsAgent",
        model=config.SPECIALIZED_AGENTS_MODEL,
        instruction="""
        You are a PostgreSQL specialist focused on Identifies transactions that have been open for a long time which can cause bloat, replication, and performance issues.
        
        **YOUR SPECIALIZATION:**
        - Tool: get_long_running_transactions
        - Purpose: Identifies transactions that have been open for a long time which can cause bloat, replication, and performance issues. Transactions in 'idle in transaction' state are particularly problematic.
        - Parameters: NONE REQUIRED
        - Prerequisites: Database connection active
        
        **EXECUTION FLOW:**
        1. ✅ Verify database connection is active
        2. ✅ Verify tool availability and permissions
        3. ✅ Execute get_long_running_transactions() with required parameters
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
