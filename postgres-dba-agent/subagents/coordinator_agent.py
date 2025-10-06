"""
PostgreSQL DBA Coordinator Agent - Intelligent Planning and Orchestration
This agent analyzes user requests and creates execution plans for specialized agents.
"""

from typing import Optional
from google.adk.agents import LlmAgent
from ..logging_config import get_logger
from ..config import settings as config
from ..utils.load_tools_persistent import load_single_tool, load_tools_persistent
from .pedagogical_agent import get_pedagogical_agent
from .synthesis_agent import get_synthesis_agent
from .performance_agent import get_performance_agent
from .security_agent import get_security_agent
from .maintenance_agent import get_maintenance_agent
from .schema_agent import get_schema_agent

logger = get_logger(__name__)


# Pre-loaded tools cache
_tools_cache = {}


def _initialize_tools():
    """Pre-load all tools at module initialization using load_tools_persistent."""
    try:
        # Load all tools using the complete toolset
        tools = load_tools_persistent(config.TOOLBOX_URL, "postgres-dba-complete")

        # Index tools by name
        for tool in tools:
            tool_name = getattr(tool, "__name__", str(tool))
            _tools_cache[tool_name] = tool
            logger.info(f"Pre-loaded tool: {tool_name}")

        logger.info(f"Successfully pre-loaded {len(_tools_cache)} tools")

    except Exception as e:
        logger.error(f"Failed to pre-load tools via load_tools_persistent: {e}")
        raise


def _get_tool(tool_name: str):
    """Get a tool from pre-loaded cache."""
    if tool_name not in _tools_cache:
        logger.error(f"Tool {tool_name} not found in cache")
        raise KeyError(f"Tool {tool_name} not found")
    return _tools_cache[tool_name]


# Initialize tools at module load
_initialize_tools()


# Tool discovery functions
def list_available_tools():
    """List all available PostgreSQL tools."""
    try:
        # Return list from tools.yaml categories
        tools = [
            "list_database_tables",
            "list_all_schemas",
            "get_slowest_historical_queries",
            "get_most_io_intensive_queries",
            "get_most_frequent_queries",
            "get_blocking_sessions",
            "get_long_running_transactions",
            "get_database_users_and_roles",
            "get_cache_hit_ratios",
            "find_invalid_indexes",
            "list_active_queries",
            "list_installed_extensions",
            "list_available_extensions",
            "get_unused_indexes",
            "get_user_table_permissions",
            "get_current_connections_summary",
            "get_user_role_memberships",
            "get_database_sizes",
            "get_table_sizes_summary",
            "get_table_maintenance_stats",
            "get_memory_configuration",
            "get_postgresql_version_info",
            "get_replication_status",
        ]
        return {"tools": tools, "count": len(tools)}
    except Exception as e:
        logger.error(f"Error listing tools: {e}")
        return {"error": str(e)}


def get_tool_info(tool_name: str):
    """Get detailed information about a specific tool."""
    try:
        tool = _get_tool(tool_name)
        return {
            "name": tool_name,
            "description": getattr(tool, "__doc__", f"Tool: {tool_name}"),
            "status": "available",
        }
    except Exception as e:
        logger.error(f"Error getting tool info for {tool_name}: {e}")
        return {"error": str(e)}


def load_precise_tool(tool_name: str):
    """Load a specific tool using load_single_tool when needed."""
    try:
        logger.info(f"Loading precise tool: {tool_name}")
        tool = load_single_tool(config.TOOLBOX_URL, tool_name)
        logger.info(f"✅ Successfully loaded {tool_name}")
        return tool
    except Exception as e:
        logger.error(f"Failed to load precise tool {tool_name}: {e}")
        return None


def execute_slowest_queries(limit: int):
    """
    Execute get_slowest_historical_queries tool with a limit parameter.
    
    Args:
        limit: Number of queries to return (e.g., 5, 10, 20)
    
    Returns:
        The slowest historical queries
    
    Example:
        execute_slowest_queries(limit=10)
    """
    try:
        logger.info(f"Executing get_slowest_historical_queries with limit={limit}")
        tool = _get_tool("get_slowest_historical_queries")
        result = tool(limit=limit)
        logger.info(f"Successfully executed get_slowest_historical_queries")
        return {"status": "success", "tool": "get_slowest_historical_queries", "result": result}
    except Exception as e:
        error_msg = f"Error executing get_slowest_historical_queries: {str(e)}"
        logger.error(error_msg)
        return {"status": "failed", "tool": "get_slowest_historical_queries", "error": error_msg}


def execute_io_intensive_queries(limit: int):
    """
    Execute get_most_io_intensive_queries tool with a limit parameter.
    
    Args:
        limit: Number of queries to return (e.g., 5, 10, 20)
    
    Returns:
        The most I/O intensive queries
    """
    try:
        logger.info(f"Executing get_most_io_intensive_queries with limit={limit}")
        tool = _get_tool("get_most_io_intensive_queries")
        result = tool(limit=limit)
        return {"status": "success", "tool": "get_most_io_intensive_queries", "result": result}
    except Exception as e:
        return {"status": "failed", "tool": "get_most_io_intensive_queries", "error": str(e)}


def execute_frequent_queries(limit: int):
    """
    Execute get_most_frequent_queries tool with a limit parameter.
    
    Args:
        limit: Number of queries to return (e.g., 5, 10, 20)
    
    Returns:
        The most frequently executed queries
    """
    try:
        logger.info(f"Executing get_most_frequent_queries with limit={limit}")
        tool = _get_tool("get_most_frequent_queries")
        result = tool(limit=limit)
        return {"status": "success", "tool": "get_most_frequent_queries", "result": result}
    except Exception as e:
        return {"status": "failed", "tool": "get_most_frequent_queries", "error": str(e)}


def execute_table_sizes(schema_name: str, limit: int):
    """
    Execute get_table_sizes_summary tool with schema_name and limit parameters.
    
    Args:
        schema_name: Schema to analyze (e.g., "public", "ecommerce")
        limit: Number of tables to return (e.g., 10, 20, 50)
    
    Returns:
        Table sizes summary for the specified schema
    """
    try:
        logger.info(f"Executing get_table_sizes_summary with schema_name={schema_name}, limit={limit}")
        tool = _get_tool("get_table_sizes_summary")
        result = tool(schema_name=schema_name, limit=limit)
        return {"status": "success", "tool": "get_table_sizes_summary", "result": result}
    except Exception as e:
        return {"status": "failed", "tool": "get_table_sizes_summary", "error": str(e)}


def execute_unused_indexes(min_size_mb: int):
    """
    Execute get_unused_indexes tool with min_size_mb parameter.
    
    Args:
        min_size_mb: Minimum size in MB to consider (e.g., 1, 5, 10)
    
    Returns:
        Unused indexes above the specified size
    """
    try:
        logger.info(f"Executing get_unused_indexes with min_size_mb={min_size_mb}")
        tool = _get_tool("get_unused_indexes")
        result = tool(min_size_mb=min_size_mb)
        return {"status": "success", "tool": "get_unused_indexes", "result": result}
    except Exception as e:
        return {"status": "failed", "tool": "get_unused_indexes", "error": str(e)}


def execute_database_tables(table_names: Optional[str] = None, output_format: Optional[str] = None):
    """
    Execute list_database_tables native tool to list database tables.
    
    Args:
        table_names: Optional comma-separated list of table names (e.g., "orders,users,products")
                     If not provided, lists all tables
        output_format: Optional output format - "simple" for names only, "detailed" for full info
                       Default is "detailed" if not specified
    
    Returns:
        List of database tables with their structure
    """
    try:
        logger.info(f"Executing list_database_tables with table_names={table_names}, output_format={output_format}")
        tool = _get_tool("list_database_tables")
        
        # Build parameters dict - only include non-None values
        params = {}
        if table_names is not None:
            params["table_names"] = table_names
        if output_format is not None:
            params["output_format"] = output_format
        
        # Call tool with or without parameters
        if params:
            result = tool(**params)
        else:
            result = tool()
            
        return {"status": "success", "tool": "list_database_tables", "result": result}
    except Exception as e:
        return {"status": "failed", "tool": "list_database_tables", "error": str(e)}


def execute_table_maintenance_stats(schema_name: str, table_name: str):
    """
    Execute get_table_maintenance_stats tool with schema_name and table_name parameters.
    
    Args:
        schema_name: Schema name (e.g., "public", "ecommerce_schema")
        table_name: Table name to check maintenance stats (e.g., "users", "orders")
    
    Returns:
        Maintenance statistics for the specified table
    """
    try:
        logger.info(f"Executing get_table_maintenance_stats with schema_name={schema_name}, table_name={table_name}")
        tool = _get_tool("get_table_maintenance_stats")
        result = tool(schema_name=schema_name, table_name=table_name)
        return {"status": "success", "tool": "get_table_maintenance_stats", "result": result}
    except Exception as e:
        return {"status": "failed", "tool": "get_table_maintenance_stats", "error": str(e)}


def execute_user_table_permissions(schema_name: str, table_name: str, username: str):
    """
    Execute get_user_table_permissions tool with schema_name, table_name and username.
    
    Args:
        schema_name: Schema name (e.g., "public", "ecommerce_schema")
        table_name: Table name to check (e.g., "orders", "users")
        username: Username to check permissions for (e.g., "postgres", "app_user")
    
    Returns:
        Table permissions for the specified user on the specified table
    """
    try:
        logger.info(f"Executing get_user_table_permissions with schema_name={schema_name}, table_name={table_name}, username={username}")
        tool = _get_tool("get_user_table_permissions")
        result = tool(schema_name=schema_name, table_name=table_name, username=username)
        return {"status": "success", "tool": "get_user_table_permissions", "result": result}
    except Exception as e:
        return {"status": "failed", "tool": "get_user_table_permissions", "error": str(e)}


def execute_user_role_memberships(username: str):
    """
    Execute get_user_role_memberships tool with username parameter.
    
    Args:
        username: Username to check role memberships (e.g., "postgres", "app_user")
    
    Returns:
        Role memberships for the specified user
    """
    try:
        logger.info(f"Executing get_user_role_memberships with username={username}")
        tool = _get_tool("get_user_role_memberships")
        result = tool(username=username)
        return {"status": "success", "tool": "get_user_role_memberships", "result": result}
    except Exception as e:
        return {"status": "failed", "tool": "get_user_role_memberships", "error": str(e)}


def execute_active_queries(min_duration: Optional[str] = None, exclude_application_names: Optional[str] = None, limit: Optional[int] = None):
    """
    Execute list_active_queries native tool to get currently active queries.
    
    Args:
        min_duration: Optional minimum query duration (e.g., "1 minute", "30 seconds", "5 minutes")
                      Default is "1 minute" if not specified
        exclude_application_names: Optional comma-separated list of application names to exclude
                                   (e.g., "psql,pgAdmin,DBeaver")
        limit: Optional maximum number of results (default: 50)
    
    Returns:
        List of currently active queries matching the filters
    """
    try:
        logger.info(f"Executing list_active_queries with min_duration={min_duration}, exclude_application_names={exclude_application_names}, limit={limit}")
        tool = _get_tool("list_active_queries")
        
        # Build parameters dict - only include non-None values
        params = {}
        if min_duration is not None:
            params["min_duration"] = min_duration
        if exclude_application_names is not None:
            params["exclude_application_names"] = exclude_application_names
        if limit is not None:
            params["limit"] = limit
        
        # Call tool with or without parameters
        if params:
            result = tool(**params)
        else:
            result = tool()
            
        return {"status": "success", "tool": "list_active_queries", "result": result}
    except Exception as e:
        return {"status": "failed", "tool": "list_active_queries", "error": str(e)}


def get_coordinator_agent():
    """Create and return the intelligent coordinator agent."""

    # Load tools using load_tools_persistent
    try:
        tools_list = load_tools_persistent(config.TOOLBOX_URL, "postgres-dba-complete")
        logger.info(f"Loaded {len(tools_list)} tools for coordinator")
        
        # Debug: Check if critical tools are loaded
        tool_names = [getattr(tool, '__name__', str(tool)) for tool in tools_list]
        logger.info(f"Loaded tools: {tool_names}")
        
        # Ensure critical tools are loaded using load_single_tool if needed
        critical_tools = ["list_all_schemas", "get_table_sizes_summary"]
        for tool_name in critical_tools:
            if tool_name not in tool_names:
                logger.warning(f"{tool_name} tool not found in loaded tools, loading individually")
                try:
                    single_tool = load_single_tool(config.TOOLBOX_URL, tool_name)
                    tools_list.append(single_tool)
                    logger.info(f"✅ Successfully loaded {tool_name} using load_single_tool")
                except Exception as e:
                    logger.error(f"Failed to load {tool_name} individually: {e}")
            
    except Exception as e:
        logger.error(f"Failed to load tools: {e}")
        logger.error("Falling back to empty tools list")
        tools_list = []

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
        
        **AVAILABLE TOOLS & AGENTS:**
        
        **Direct PostgreSQL Tools (loaded via load_tools_persistent):**
        
        **Schema & Structure:**
        - list_all_schemas (no parameters) - List all schemas in the database
        - list_database_tables (REQUIRED: schema_name, optional: table_name)
        - get_table_sizes_summary (REQUIRED: schema_name, REQUIRED: limit) - COMPREHENSIVE table sizes with row counts
        - find_invalid_indexes (no parameters)
        - get_unused_indexes (REQUIRED: min_size_mb)
        - get_table_maintenance_stats (REQUIRED: table_name)
        
        **Security & Users:**
        - get_database_users_and_roles (no parameters)
        - get_user_table_permissions (REQUIRED: username, optional: table_name)
        - get_user_role_memberships (REQUIRED: username)
        - get_current_connections_summary (no parameters)
        
        **Performance & Monitoring:**
        - list_active_queries (optional: min_duration_ms, exclude_apps)
        - get_slowest_historical_queries (REQUIRED: limit) - Number of queries to return
        - get_most_io_intensive_queries (REQUIRED: limit) - Number of queries to return
        - get_most_frequent_queries (REQUIRED: limit) - Number of queries to return
        - get_blocking_sessions (no parameters)
        - get_long_running_transactions (no parameters)
        - get_cache_hit_ratios (no parameters)
        
        **System & Maintenance:**
        - get_database_sizes (no parameters)
        - get_memory_configuration (no parameters)
        - get_postgresql_version_info (no parameters)
        - get_replication_status (no parameters)
        - list_installed_extensions (no parameters)
        - list_available_extensions (no parameters)
        
        **Available Sub-Agents (Managed automatically by Google ADK):**
        - PerformanceAgent → Comprehensive performance analysis and optimization
        - SecurityAgent → Security auditing and vulnerability assessment  
        - MaintenanceAgent → Database health and maintenance analysis
        - SchemaAgent → Schema design analysis and optimization
        - PedagogicalAgent → PostgreSQL concept explanations and education
        - SynthesisAgent → Multi-source result synthesis and analysis
        
        **Direct Agent Communication:**
        The coordinator can communicate directly with sub-agents by referring to them by name.
        Google ADK automatically handles the delegation and routing.
        
        **Tools Registry Functions:**
        - list_available_tools() → Get list of all available PostgreSQL tools
        - get_tool_info(tool_name) → Get detailed information about a specific tool and its parameters
        - load_precise_tool(tool_name) → Load a specific tool using load_single_tool when needed
        
        **Specialized Execution Functions (USE THESE FOR TOOLS WITH PARAMETERS):**
        
        **Performance Tools:**
        - execute_slowest_queries(limit) → Get slowest historical queries with specified limit
        - execute_io_intensive_queries(limit) → Get most I/O intensive queries with specified limit
        - execute_frequent_queries(limit) → Get most frequent queries with specified limit
        - execute_active_queries(min_duration, exclude_application_names, limit) → Get active queries (all params optional)
          * min_duration: e.g., "1 minute", "30 seconds" (default: "1 minute")
          * exclude_application_names: CSV list (e.g., "psql,pgAdmin")
          * limit: max results (default: 50)
        
        **Schema Tools:**
        - execute_database_tables(table_names, output_format) → List database tables (both params optional)
          * table_names: comma-separated list (e.g., "orders,users") or empty for all tables
          * output_format: "simple" for names only, "detailed" for full structure (default: detailed)
        - execute_table_sizes(schema_name, limit) → Get table sizes for schema with specified limit
        - execute_unused_indexes(min_size_mb) → Get unused indexes above specified size
        - execute_table_maintenance_stats(schema_name, table_name) → Get maintenance stats for specific table
        
        **Security Tools:**
        - execute_user_table_permissions(schema_name, table_name, username) → Get user permissions on specific table
        - execute_user_role_memberships(username) → Get role memberships for user
        
        **TOOL SELECTION GUIDELINES:**
        
        **For Table Size Requests:**
        - Use get_table_sizes_summary() for comprehensive table size analysis
        - Includes: table names, types, row counts, total/table/index sizes, formatted sizes
        - Parameters: schema_name (REQUIRED), limit (REQUIRED)
        - ALWAYS use get_table_sizes_summary() for ANY table size analysis request
        - Preferred over list_database_tables() + get_table_maintenance_stats() combination
        
        **For Schema Analysis:**
        - Use list_database_tables() without parameters to get ALL tables across ALL schemas
        - Use list_database_tables(schema_name=required) for specific schema table structure and metadata
        - Use get_table_sizes_summary(schema_name=required) for storage and capacity analysis
        - Combine both for complete schema overview
        
        **For Index Analysis:**
        - Use get_unused_indexes(min_size_mb=REQUIRED) for unused index identification
        - Use find_invalid_indexes() for broken index detection
        
        **For Maintenance Analysis:**
        - Use get_table_maintenance_stats(table_name=REQUIRED) for specific table maintenance stats
        
        **For Performance Analysis:**
        - Use get_slowest_historical_queries(limit=REQUIRED) for slowest queries analysis
        - Use get_most_io_intensive_queries(limit=REQUIRED) for I/O intensive queries
        - Use get_most_frequent_queries(limit=REQUIRED) for most frequent queries
        
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
        
        **Request: "List all schemas in the database"**
        Plan:
        - Step 1: Use list_all_schemas() to get all schemas
        - Step 2: Present organized schema list grouped by type (user/system)
          → Format: Group schemas by type, show count, and present in organized sections
          
        **Request: "List all tables in the database"**
        Plan:
        - Step 1: Use list_database_tables() without parameters to get ALL tables across ALL schemas
          → Present: "Found X tables across Y schemas. Continue with analysis? ✅ Yes / ❌ No"
        - Step 2: Present organized results grouped by schema
          → Present final comprehensive table listing
          
        **Request: "List all tables and their sizes"**
        Plan:
        - Step 1: Ask user for schema_name (REQUIRED parameter)
          → Present: "Please specify the schema name to analyze (e.g., 'public', 'ecommerce_schema')"
        - Step 2: Ask user for limit (REQUIRED parameter)
          → Present: "How many tables should I analyze? (limit parameter)"
        - Step 3: get_table_sizes_summary(schema_name=user_provided, limit=user_provided) → Get comprehensive table sizes with row counts
          → Present: "Found X tables in [schema] with sizes and row counts. Continue with analysis? ✅ Yes / ❌ No"
        - Step 4: Ask SynthesisAgent to analyze storage patterns if needed
          → "SynthesisAgent, please analyze the table size patterns and provide recommendations"
          → Present final comprehensive report with storage analysis
        
        **Request: "Security audit"**
        Plan:
        - Step 1: get_database_users_and_roles() → Get all users and roles
          → Present results and ask for validation
        - Step 2: get_user_table_permissions(username=user) → Get permissions (needs usernames from Step 1)
          → Present results and ask for validation
        - Step 3: get_user_role_memberships(username=user) → Get role memberships
          → Present results and ask for validation
        - Step 4: Ask SynthesisAgent to analyze security vulnerabilities
          → "SynthesisAgent, please analyze the security audit results and identify vulnerabilities"
          → Present final security report
        
        **Request: "Performance analysis"**
        Plan:
        - Step 1: list_active_queries() → Get current active queries
          → Present results and ask for validation
        - Step 2: Ask user for limit parameter (REQUIRED)
          → Present: "How many slowest historical queries should I analyze? (limit parameter)"
        - Step 3: get_slowest_historical_queries(limit=user_provided) → Get historical slow queries
          → Present results and ask for validation
        - Step 4: get_blocking_sessions() → Check for blocking sessions
          → Present results and ask for validation
        - Step 5: get_cache_hit_ratios() → Check cache performance
          → Present results and ask for validation
        - Step 6: Ask SynthesisAgent to analyze and combine all results
          → "SynthesisAgent, please analyze and synthesize the performance results"
          → Present final comprehensive performance report
          
        **Request: "What is VACUUM in PostgreSQL?"**
        Plan:
        - Step 1: Ask PedagogicalAgent to explain VACUUM concept
          → "PedagogicalAgent, please explain what VACUUM is in PostgreSQL"
          → Agent will provide detailed educational content about VACUUM concept, usage, and best practices
          
        **Request: "Performance analysis of my database"**
        Plan:
        - Step 1: Ask PerformanceAgent to analyze database performance
          → "PerformanceAgent, please analyze the database performance and identify bottlenecks"
          → Agent will use its tools to provide comprehensive performance analysis
          
        **Request: "Security audit"**
        Plan:
        - Step 1: Ask SecurityAgent to conduct security audit
          → "SecurityAgent, please perform a comprehensive security audit"
          → Agent will assess vulnerabilities, user privileges, and provide remediation plan
          
        **Request: "Check database maintenance needs"**
        Plan:
        - Step 1: Ask MaintenanceAgent to assess maintenance needs
          → "MaintenanceAgent, please check database maintenance requirements"
          → Agent will assess maintenance status and provide action recommendations
          
        **Request: "Show me table sizes in [schema]"**
        Plan:
        - Step 1: Use get_table_sizes_summary(schema_name=schema) directly
          → Get comprehensive table information with sizes, row counts, and storage breakdown
          → Present detailed table analysis with storage recommendations
          
        **Request: "Analyze storage usage"**
        Plan:
        - Step 1: Ask user for schema_name (REQUIRED parameter)
          → Present: "Please specify the schema name to analyze for storage usage"
        - Step 2: Use get_table_sizes_summary(schema_name=user_provided) 
          → Get comprehensive storage analysis with table sizes, row counts, and index sizes
          → Present detailed storage breakdown and recommendations
          
        **Request: "Check table sizes and row counts"**
        Plan:
        - Step 1: Ask user for schema_name (REQUIRED parameter)
          → Present: "Please specify the schema name to analyze"
        - Step 2: Use get_table_sizes_summary(schema_name=user_provided)
          → Get comprehensive table information with sizes, row counts, and storage breakdown
          → Present detailed analysis with storage recommendations
          
        **Request: "Analyze my database schema design"**
        Plan:
        - Step 1: Ask SchemaAgent to analyze schema design
          → "SchemaAgent, please analyze the database schema design and suggest improvements"
          → Agent will analyze structure and provide optimization recommendations
          
        **Request: "Complete database health check"**
        Plan:
        - Step 1: Ask PerformanceAgent for performance assessment
        - Step 2: Ask SecurityAgent for security assessment  
        - Step 3: Ask MaintenanceAgent for maintenance assessment
        - Step 4: Ask SchemaAgent for schema assessment
        - Step 5: Ask SynthesisAgent to combine all assessments
          → "SynthesisAgent, please synthesize all the assessment results"
          → Comprehensive multi-agent analysis with expert synthesis
        
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
        
        **TABLE ANALYSIS WORKFLOW:**
        1. Ask user for schema_name (REQUIRED parameter for all table analysis)
        2. Use get_table_sizes_summary(schema_name=required) for comprehensive analysis
        3. Use list_database_tables(schema_name=required) for table structure if needed
        4. Ask SynthesisAgent to combine results if multiple analyses performed
        5. Always ask for user validation between major steps
        
        **STORAGE ANALYSIS WORKFLOW:**
        1. Ask user for schema_name (REQUIRED parameter)
        2. Use get_table_sizes_summary(schema_name=required) for storage analysis
        3. Present comprehensive storage breakdown with recommendations
        4. Ask SynthesisAgent for storage optimization recommendations if needed
        
        **EXECUTION CAPABILITIES:**
        
        You have access to the following capabilities:
        
        **Direct Tool Execution:**
        - Most common tools available directly: list_database_tables(schema_name=required), get_table_sizes_summary(schema_name=required, limit=required), get_slowest_historical_queries(limit=required), etc.
        - All tools loaded via load_tools_persistent → Direct access to PostgreSQL tools
        - ALWAYS provide required parameters (schema_name, table_name, min_size_mb, limit, etc.)
        - NEVER call tools without required parameters - always ask user for missing parameters first
        
        **Sub-Agent Communication:**
        The coordinator communicates directly with sub-agents through natural language:
        - "PerformanceAgent, [request]" → Performance analysis and optimization
        - "SecurityAgent, [request]" → Security auditing and vulnerability assessment
        - "MaintenanceAgent, [request]" → Database health and maintenance analysis
        - "SchemaAgent, [request]" → Schema design analysis and optimization
        
        Google ADK automatically routes these requests to the appropriate sub-agents.
        
        **Tools Registry Functions:**
        - list_available_tools() → Get list of all available PostgreSQL tools
        - get_tool_info(tool_name) → Get detailed information about a specific tool and its parameters
        
        **EXECUTION PROCESS:**
        
        1. **ANALYZE** user request and create execution plan
        2. **EXECUTE** one tool/agent at a time with user validation
        3. **COORDINATE** sub-agents for specialized analysis
        4. **SYNTHESIZE** results for comprehensive analysis
        
        **Key Rules:**
        - Always present plan before execution
        - Ask for validation between steps
        - Use sub-agents for domain expertise
        - Combine results with SynthesisAgent
        
        **DISPLAY FORMATTING GUIDELINES:**
        
        **For Schema Lists:**
        - Group schemas by type (User Schemas vs System Schemas)
        - Show count for each group
        - Use clear section headers
        - Format: "📊 USER SCHEMAS (X schemas):" and "🔧 SYSTEM SCHEMAS (X schemas):"
        
        **For Table Lists:**
        - Group by schema
        - Show table count per schema
        - Use organized sections with clear headers
        
        **General Formatting:**
        - Use emojis for visual clarity (📊, 🔧, 📋, ✅, ❌)
        - Group related information together
        - Provide counts and summaries
        - Use clear section dividers
        
        **CRITICAL RULES:**
        - Execute ONE tool/agent at a time with user validation
        - Use sub-agents for specialized analysis (PerformanceAgent, SecurityAgent, etc.)
        - Use SynthesisAgent to combine multiple results
        - Handle user "No" responses gracefully
        
        **TOOL CALLING WITH PARAMETERS:**
        When the user provides a parameter value (e.g., "limit 5", "limit=10", "schema public"):
        1. Extract the parameter value from user input (e.g., "limit 5" → 5)
        2. Use the specialized execution function with the parameter
        3. Example: If user says "limit 5" for slowest queries, call execute_slowest_queries(limit=5)
        4. Example: If user says "schema public and limit 20" for table sizes, call execute_table_sizes(schema_name="public", limit=20)
        5. Example: For active queries, call execute_active_queries() (no parameters needed)
        6. ALWAYS use the specialized execution functions (execute_slowest_queries, execute_active_queries, etc.)
        7. When user provides "limit X", extract X as an integer and pass it to the function
        8. NEVER call the base tools (get_slowest_historical_queries, list_active_queries, etc.) directly - use the execute_* functions
        
        **RESPONSE FORMAT:**
        ```
        ## 📋 ANALYSIS PLAN
        
        **Request:** [User request]
        
        **Recommended Approach:**
        1. Ask [AgentName] to handle specialized analysis → [Purpose]
        2. Use direct tool calls (e.g., list_database_tables(), get_cache_hit_ratios()) → [Purpose]
        3. Ask SynthesisAgent to combine results → Comprehensive analysis
        
        **Available Agents:** [List of relevant agents]
        **Required Parameters:** [List of needed parameters]
        **Estimated Time:** [X minutes]
        **Complexity:** [Low/Medium/High]
        
        **Next Steps:** [Guidance on how to proceed]
        ```
        """,
        tools=tools_list + [
            # Tool discovery functions
            list_available_tools,
            get_tool_info,
            load_precise_tool,
            # Specialized execution functions with explicit parameters
            # Performance tools
            execute_slowest_queries,
            execute_io_intensive_queries,
            execute_frequent_queries,
            execute_active_queries,
            # Schema tools
            execute_database_tables,
            execute_table_sizes,
            execute_unused_indexes,
            execute_table_maintenance_stats,
            # Security tools
            execute_user_table_permissions,
            execute_user_role_memberships,
        ],
        sub_agents=[
            get_performance_agent(),
            get_security_agent(),
            get_maintenance_agent(),
            get_schema_agent(),
            get_pedagogical_agent(),
            get_synthesis_agent(),
        ],
    )

    return coordinator
