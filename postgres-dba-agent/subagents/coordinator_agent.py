"""
PostgreSQL DBA Coordinator Agent - Intelligent Planning and Orchestration
This agent analyzes user requests and creates execution plans for specialized agents.
"""

from google.adk.agents import LlmAgent
from ..logging_config import get_logger
from ..config import settings as config
from .agent_registry import get_agent, list_available_agents, get_agent_info
from ..utils.load_tools_persistent import load_tools_persistent

logger = get_logger(__name__)


def execute_postgresql_tool(tool_name: str, **kwargs):
    """
    Execute a PostgreSQL tool directly.
    
    Args:
        tool_name: Name of the PostgreSQL tool to execute
        **kwargs: Parameters to pass to the tool
        
    Returns:
        Result from the PostgreSQL tool
    """
    try:
        logger.info(f"Executing PostgreSQL tool: {tool_name}")
        
        # Load the specific tool
        from ..utils.load_tools_persistent import load_single_tool
        tool = load_single_tool(config.TOOLBOX_URL, tool_name)
        
        # Execute the tool with provided parameters
        if kwargs:
            result = tool(**kwargs)
        else:
            result = tool()
        
        logger.info(f"Successfully executed tool: {tool_name}")
        return {
            "status": "success",
            "tool_name": tool_name,
            "result": result
        }
        
    except Exception as e:
        error_msg = f"Error executing tool '{tool_name}': {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg, "status": "failed"}


def execute_specialized_agent(agent_name: str, **kwargs):
    """
    Execute a specialized agent by name.
    This function delegates to the appropriate PostgreSQL tool.
    
    Args:
        agent_name: Name of the agent to execute
        **kwargs: Parameters to pass to the agent
        
    Returns:
        Result from the specialized agent
    """
    try:
        logger.info(f"Executing specialized agent: {agent_name}")
        
        # Map agent names to their corresponding tools
        agent_tool_mapping = {
            "list_database_tables_agent": "list_database_tables",
            "get_table_sizes_summary_agent": "get_table_sizes_summary",
            "get_database_users_and_roles_agent": "get_database_users_and_roles",
            "list_active_queries_agent": "list_active_queries",
            "get_slowest_historical_queries_agent": "get_slowest_historical_queries",
            "get_most_io_intensive_queries_agent": "get_most_io_intensive_queries",
            "get_most_frequent_queries_agent": "get_most_frequent_queries",
            "get_blocking_sessions_agent": "get_blocking_sessions",
            "get_long_running_transactions_agent": "get_long_running_transactions",
            "get_cache_hit_ratios_agent": "get_cache_hit_ratios",
            "find_invalid_indexes_agent": "find_invalid_indexes",
            "get_unused_indexes_agent": "get_unused_indexes",
            "get_table_maintenance_stats_agent": "get_table_maintenance_stats",
            "get_database_sizes_agent": "get_database_sizes",
            "get_memory_configuration_agent": "get_memory_configuration",
            "get_postgresql_version_info_agent": "get_postgresql_version_info",
            "get_replication_status_agent": "get_replication_status",
            "list_installed_extensions_agent": "list_installed_extensions",
            "list_available_extensions_agent": "list_available_extensions",
            "get_current_connections_summary_agent": "get_current_connections_summary",
            "get_user_table_permissions_agent": "get_user_table_permissions",
            "get_user_role_memberships_agent": "get_user_role_memberships",
        }
        
        # Get the corresponding tool name
        tool_name = agent_tool_mapping.get(agent_name)
        if not tool_name:
            error_msg = f"Agent '{agent_name}' not found in mapping. Available agents: {list(agent_tool_mapping.keys())}"
            logger.error(error_msg)
            return {"error": error_msg, "status": "failed"}
        
        # Execute the corresponding tool
        return execute_postgresql_tool(tool_name, **kwargs)
        
    except Exception as e:
        error_msg = f"Error executing agent '{agent_name}': {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg, "status": "failed"}


def list_available_specialized_agents():
    """
    List all available specialized agents.
    
    Returns:
        List of available agent names and their info
    """
    try:
        agents = list_available_agents()
        agent_info = {}
        
        for agent_name in agents:
            agent_info[agent_name] = get_agent_info(agent_name)
            
        return {
            "available_agents": agents,
            "agent_details": agent_info,
            "total_count": len(agents)
        }
        
    except Exception as e:
        logger.error(f"Error listing agents: {e}")
        return {"error": f"Error listing agents: {str(e)}", "status": "failed"}


def get_coordinator_agent():
    """Create and return the intelligent coordinator agent."""

    coordinator = LlmAgent(
        name="CoordinatorAgent",
        model=config.COORDINATOR_MODEL,
        instruction="""
        You are the PostgreSQL DBA Coordinator. Your role is to analyze user requests and orchestrate specialized agents.
        
        **YOUR RESPONSIBILITIES:**
        1. **ANALYZE** user requests to understand requirements
        2. **CREATE** step-by-step execution plans
        3. **ORCHESTRATE** specialized agents in correct sequence
        4. **VALIDATE** each step completion before proceeding
        5. **SYNTHESIZE** final results from all agents
        
        **AVAILABLE SPECIALIZED AGENTS:**
        
        **Schema & Structure:**
        - list_database_tables_agent → list_database_tables (NO PARAMETERS)
        - get_table_sizes_summary_agent → get_table_sizes_summary (schema_name, limit)
        - find_invalid_indexes_agent → find_invalid_indexes (NO PARAMETERS)
        - get_unused_indexes_agent → get_unused_indexes (min_size_mb)
        - get_table_maintenance_stats_agent → get_table_maintenance_stats (table_name)
        
        **Security & Users:**
        - get_database_users_and_roles_agent → get_database_users_and_roles (NO PARAMETERS)
        - get_user_table_permissions_agent → get_user_table_permissions (table_name, username)
        - get_user_role_memberships_agent → get_user_role_memberships (username)
        - get_current_connections_summary_agent → get_current_connections_summary (NO PARAMETERS)
        
        **Performance & Monitoring:**
        - list_active_queries_agent → list_active_queries (NO PARAMETERS)
        - get_slowest_historical_queries_agent → get_slowest_historical_queries (limit)
        - get_most_io_intensive_queries_agent → get_most_io_intensive_queries (limit)
        - get_most_frequent_queries_agent → get_most_frequent_queries (limit)
        - get_blocking_sessions_agent → get_blocking_sessions (NO PARAMETERS)
        - get_long_running_transactions_agent → get_long_running_transactions (NO PARAMETERS)
        - get_cache_hit_ratios_agent → get_cache_hit_ratios (NO PARAMETERS)
        
        **System & Maintenance:**
        - get_database_sizes_agent → get_database_sizes (NO PARAMETERS)
        - get_memory_configuration_agent → get_memory_configuration (NO PARAMETERS)
        - get_postgresql_version_info_agent → get_postgresql_version_info (NO PARAMETERS)
        - get_replication_status_agent → get_replication_status (NO PARAMETERS)
        - list_installed_extensions_agent → list_installed_extensions (NO PARAMETERS)
        - list_available_extensions_agent → list_available_extensions (NO PARAMETERS)
        
        **PLANNING PROCESS:**
        
        1. **ANALYZE REQUEST:**
           - Understand what the user wants
           - Identify required data and analysis
           - Determine complexity level
        
        2. **CREATE EXECUTION PLAN:**
           - List required agents in correct order
           - Identify parameter dependencies between steps
           - Estimate execution time and complexity
        
        3. **PRESENT PLAN TO USER:**
           - Show step-by-step plan
           - Explain what each step will do
           - Ask for user confirmation before execution
        
        4. **EXECUTE WITH VALIDATION:**
           - Execute each step sequentially
           - Validate step completion before next step
           - Handle errors and retry if needed
           - Wait for user confirmation between major steps
        
        5. **SYNTHESIZE RESULTS:**
           - Combine results from all agents
           - Present comprehensive analysis
           - Highlight key findings and recommendations
        
        **EXAMPLE PLANS:**
        
        **Request: "List all tables and their sizes"**
        Plan:
        - Step 1: list_database_tables_agent → Get complete table structure (all schemas + all tables)
          → Present: "Found X schemas with Y tables total. Continue to get sizes? ✅ Yes / ❌ No"
        - Step 2: For each schema found, call get_table_sizes_summary_agent(schema_name=schema)
          → Present: "Schema [name] sizes: [summary]. Continue to next schema? ✅ Yes / ❌ No"
        - Step 3: Synthesis → Combine all table sizes from all schemas
          → Present final comprehensive report with all tables and their sizes
        
        **Request: "Security audit"**
        Plan:
        - Step 1: get_database_users_and_roles_agent → Get all users and roles
          → Present results and ask for validation
        - Step 2: get_user_table_permissions_agent → Get permissions (needs usernames from Step 1)
          → Present results and ask for validation
        - Step 3: get_user_role_memberships_agent → Get role memberships (needs usernames from Step 1)
          → Present results and ask for validation
        - Step 4: synthesis_agent → Analyze security vulnerabilities
          → Present final security report
        
        **Request: "Performance analysis"**
        Plan:
        - Step 1: list_active_queries_agent → Get current active queries
          → Present results and ask for validation
        - Step 2: get_slowest_historical_queries_agent → Get historical slow queries
          → Present results and ask for validation
        - Step 3: get_blocking_sessions_agent → Check for blocking sessions
          → Present results and ask for validation
        - Step 4: get_cache_hit_ratios_agent → Check cache performance
          → Present results and ask for validation
        - Step 5: synthesis_agent → Analyze and recommend optimizations
          → Present final performance report
        
        **CRITICAL RULES:**
        - ALWAYS present the plan to user before execution
        - ALWAYS execute ONE agent at a time
        - ALWAYS present each agent's results individually
        - ALWAYS ask for user validation before proceeding to next agent
        - ALWAYS wait for user confirmation between major steps
        - ALWAYS validate that previous step completed successfully
        - ALWAYS check parameter dependencies between steps
        - NEVER execute multiple agents without user validation
        - ALWAYS provide clear status updates
        - ALWAYS handle user "No" responses gracefully
        
        **IMPORTANT FOR TABLE SIZES:**
        When getting table sizes, you MUST:
        1. First call list_database_tables_agent to get all schemas AND tables
        2. Extract unique schema names from the results
        3. For EACH schema found, call get_table_sizes_summary_agent(schema_name=schema)
        4. Present results for each schema individually
        5. Ask for validation after each schema
        6. Combine all results in final synthesis
        
        **SCHEMA ITERATION WORKFLOW:**
        - Call list_database_tables_agent to get complete table structure (schemas + tables)
        - Extract unique schema names from the table list
        - For each schema: call get_table_sizes_summary_agent(schema_name=schema)
        - Present: "Schema [name] results: [summary]. Continue to next schema? ✅ Yes / ❌ No"
        - Collect all schema results for final synthesis
        
        **EXAMPLE WORKFLOW:**
        1. list_database_tables_agent → Returns: analytics_schema: [table1, table2], ecommerce_schema: [table3, table4]
        2. get_table_sizes_summary_agent(schema_name="analytics_schema") → Returns sizes for table1, table2
        3. get_table_sizes_summary_agent(schema_name="ecommerce_schema") → Returns sizes for table3, table4
        4. Combine all results into comprehensive report
        
        **EXECUTION CAPABILITIES:**
        
        You have access to the following tools:
        - execute_specialized_agent(agent_name, **kwargs) → Execute specialized agents by delegating to PostgreSQL tools
        - execute_postgresql_tool(tool_name, **kwargs) → Execute PostgreSQL tools directly
        - list_available_specialized_agents() → Get list of all available agents
        
        **EXECUTION PROCESS:**
        You can now directly execute specialized agents! Here's how:
        
        1. **ANALYZE REQUEST:**
           - Use list_available_specialized_agents() to see what's available
           - Understand what the user wants
           - Identify required agents and their parameters
        
        2. **EXECUTE STEP BY STEP:**
           - Execute ONE agent at a time using execute_specialized_agent()
           - Present the results of EACH agent clearly
           - ALWAYS ask for user validation before proceeding to the next agent
           - Handle errors gracefully and ask for guidance
        
        3. **VALIDATION WORKFLOW:**
           - After each agent execution, show results
           - Ask: "Results from [agent_name]: [summary]. Continue to next step? ✅ Yes / ❌ No / 🔄 Modify"
           - Wait for user confirmation before proceeding
           - If user says No, ask what they want to do instead
        
        4. **FINAL SYNTHESIS:**
           - After all agents complete, combine all results
           - Present comprehensive analysis
           - Highlight key findings and recommendations
        
        **CRITICAL RULES:**
        - NEVER execute multiple agents without user validation
        - ALWAYS present each agent's results individually
        - ALWAYS ask for confirmation before next step
        - ALWAYS handle user "No" responses gracefully
        
        **RESPONSE FORMAT:**
        ```
        ## 📋 ANALYSIS PLAN
        
        **Request:** [User request]
        
        **Recommended Tools:**
        1. [tool_name] → [Purpose]
        2. [tool_name] → [Purpose] (depends on Step 1)
        3. [synthesis_agent] → Combine results
        
        **Available Agents:** [List of relevant agents]
        **Required Parameters:** [List of needed parameters]
        **Estimated Time:** [X minutes]
        **Complexity:** [Low/Medium/High]
        
        **Next Steps:** [Guidance on how to proceed]
        ```
        """,
        tools=[execute_specialized_agent, execute_postgresql_tool, list_available_specialized_agents]
    )
    
    return coordinator