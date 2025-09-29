"""
PostgreSQL DBA Coordinator Agent - Intelligent Planning and Orchestration
This agent analyzes user requests and creates execution plans for specialized agents.
"""

from google.adk.agents import LlmAgent
from ..logging_config import get_logger
from ..config import settings as config
from ..utils.load_tools_persistent import load_single_tool
from .pedagogical_agent import get_pedagogical_agent
from .synthesis_agent import get_synthesis_agent
from .performance_agent import get_performance_agent
from .security_agent import get_security_agent
from .maintenance_agent import get_maintenance_agent
from .schema_agent import get_schema_agent

logger = get_logger(__name__)


# Lazy-loaded tools cache
_tools_cache = {}


def _get_tool(tool_name: str):
    """Get a tool from cache or load it from MCP toolbox."""
    if tool_name not in _tools_cache:
        try:
            _tools_cache[tool_name] = load_single_tool(config.TOOLBOX_URL, tool_name)
            logger.info(f"Loaded tool: {tool_name}")
        except Exception as e:
            logger.error(f"Failed to load tool {tool_name}: {e}")
            raise
    return _tools_cache[tool_name]


# Tool wrapper functions using load_tools_persistent
def list_database_tables(**kwargs):
    """List all database tables with optional schema and table filtering."""
    tool = _get_tool("list_database_tables")
    return tool(**kwargs)


def get_table_sizes_summary(**kwargs):
    """Get comprehensive table size information for a schema."""
    tool = _get_tool("get_table_sizes_summary")
    return tool(**kwargs)


def get_slowest_historical_queries(**kwargs):
    """Get the slowest queries from query history."""
    tool = _get_tool("get_slowest_historical_queries")
    return tool(**kwargs)


def get_most_io_intensive_queries(**kwargs):
    """Get the most I/O intensive queries."""
    tool = _get_tool("get_most_io_intensive_queries")
    return tool(**kwargs)


def get_most_frequent_queries(**kwargs):
    """Get the most frequently executed queries."""
    tool = _get_tool("get_most_frequent_queries")
    return tool(**kwargs)


def get_blocking_sessions(**kwargs):
    """Find sessions that are blocking other queries."""
    tool = _get_tool("get_blocking_sessions")
    return tool(**kwargs)


def get_long_running_transactions(**kwargs):
    """Find long-running transactions."""
    tool = _get_tool("get_long_running_transactions")
    return tool(**kwargs)


def get_database_users_and_roles(**kwargs):
    """List all database users and their roles."""
    tool = _get_tool("get_database_users_and_roles")
    return tool(**kwargs)


def get_cache_hit_ratios(**kwargs):
    """Get database cache hit ratios."""
    tool = _get_tool("get_cache_hit_ratios")
    return tool(**kwargs)


def find_invalid_indexes(**kwargs):
    """Find invalid or broken indexes."""
    tool = _get_tool("find_invalid_indexes")
    return tool(**kwargs)


def list_active_queries(**kwargs):
    """List currently active SQL queries on the database."""
    tool = _get_tool("list_active_queries")
    return tool(**kwargs)


def list_installed_extensions(**kwargs):
    """List all currently installed PostgreSQL extensions."""
    tool = _get_tool("list_installed_extensions")
    return tool(**kwargs)


def list_available_extensions(**kwargs):
    """List all PostgreSQL extensions available for installation."""
    tool = _get_tool("list_available_extensions")
    return tool(**kwargs)


def get_unused_indexes(**kwargs):
    """Identify indexes that are not being used."""
    tool = _get_tool("get_unused_indexes")
    return tool(**kwargs)


def get_user_table_permissions(**kwargs):
    """Get table permissions for a specific user."""
    tool = _get_tool("get_user_table_permissions")
    return tool(**kwargs)


def get_current_connections_summary(**kwargs):
    """Get summary of current database connections."""
    tool = _get_tool("get_current_connections_summary")
    return tool(**kwargs)


def get_user_role_memberships(**kwargs):
    """Get role memberships for a specific user."""
    tool = _get_tool("get_user_role_memberships")
    return tool(**kwargs)


def get_database_sizes(**kwargs):
    """Get sizes of all databases."""
    tool = _get_tool("get_database_sizes")
    return tool(**kwargs)


def get_table_maintenance_stats(**kwargs):
    """Get maintenance statistics (VACUUM/ANALYZE) for tables."""
    tool = _get_tool("get_table_maintenance_stats")
    return tool(**kwargs)


def get_memory_configuration(**kwargs):
    """Get PostgreSQL memory configuration parameters."""
    tool = _get_tool("get_memory_configuration")
    return tool(**kwargs)


def get_postgresql_version_info(**kwargs):
    """Get PostgreSQL version and build information."""
    tool = _get_tool("get_postgresql_version_info")
    return tool(**kwargs)


def get_replication_status(**kwargs):
    """Get PostgreSQL replication status."""
    tool = _get_tool("get_replication_status")
    return tool(**kwargs)


# Generic tool execution function - simplified signature for ADK
def execute_tool(tool_name: str):
    """Execute any PostgreSQL tool by name without parameters."""
    try:
        tool = _get_tool(tool_name)
        return tool()
    except Exception as e:
        logger.error(f"Error executing tool {tool_name}: {e}")
        return {"error": f"Failed to execute {tool_name}: {str(e)}"}


# Tool discovery functions
def list_available_tools():
    """List all available PostgreSQL tools."""
    try:
        # Return list from tools.yaml categories
        tools = [
            "list_database_tables",
            "get_table_sizes_summary",
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
        
        **AVAILABLE TOOLS & AGENTS:**
        
        **Direct PostgreSQL Tools (use execute_tool or execute_postgresql_tool):**
        
        **Schema & Structure:**
        - list_database_tables (optional: schema_name, table_name)
        - get_table_sizes_summary (optional: schema_name, limit - defaults: public, 20)
        - find_invalid_indexes (no parameters)
        - get_unused_indexes (optional: min_size_mb - default: 1)
        - get_table_maintenance_stats (optional: table_name)
        
        **Security & Users:**
        - get_database_users_and_roles (no parameters)
        - get_user_table_permissions (required: username, optional: table_name)
        - get_user_role_memberships (required: username)
        - get_current_connections_summary (no parameters)
        
        **Performance & Monitoring:**
        - list_active_queries (optional: min_duration_ms, exclude_apps)
        - get_slowest_historical_queries (optional: limit - default: 10)
        - get_most_io_intensive_queries (optional: limit - default: 10)
        - get_most_frequent_queries (optional: limit - default: 10)
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
        - Step 1: list_database_tables() → Get complete table structure
          → Present: "Found X schemas with Y tables total. Continue to get sizes? ✅ Yes / ❌ No"
        - Step 2: For each schema found, get_table_sizes_summary(schema_name=schema)
          → Present: "Schema [name] sizes: [summary]. Continue to next schema? ✅ Yes / ❌ No"
        - Step 3: Ask SynthesisAgent to combine all results
          → "SynthesisAgent, please synthesize the table size data from all schemas"
          → Present final comprehensive report with all tables and their sizes
        
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
        - Step 2: get_slowest_historical_queries() → Get historical slow queries
          → Present results and ask for validation
        - Step 3: get_blocking_sessions() → Check for blocking sessions
          → Present results and ask for validation
        - Step 4: get_cache_hit_ratios() → Check cache performance
          → Present results and ask for validation
        - Step 5: Ask SynthesisAgent to analyze and combine all results
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
        
        **TABLE SIZE ANALYSIS WORKFLOW:**
        1. Call list_database_tables() to get all schemas
        2. For each schema: get_table_sizes_summary(schema_name=schema)
        3. Ask SynthesisAgent to combine results
        4. Always ask for user validation between schemas
        
        **EXECUTION CAPABILITIES:**
        
        You have access to the following capabilities:
        
        **Direct Tool Execution:**
        - Most common tools available directly: list_database_tables(), get_table_sizes_summary(), get_slowest_historical_queries(), etc.
        - execute_tool(tool_name) → For other PostgreSQL tools without parameters
        
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
        
        **CRITICAL RULES:**
        - Execute ONE tool/agent at a time with user validation
        - Use sub-agents for specialized analysis (PerformanceAgent, SecurityAgent, etc.)
        - Use SynthesisAgent to combine multiple results
        - Handle user "No" responses gracefully
        
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
        tools=[
            # Direct PostgreSQL tool wrappers (complete coverage of tools.yaml)
            list_database_tables,
            get_table_sizes_summary,
            get_slowest_historical_queries,
            get_most_io_intensive_queries,
            get_most_frequent_queries,
            get_blocking_sessions,
            get_long_running_transactions,
            get_database_users_and_roles,
            get_cache_hit_ratios,
            find_invalid_indexes,
            list_active_queries,
            list_installed_extensions,
            list_available_extensions,
            get_unused_indexes,
            get_user_table_permissions,
            get_current_connections_summary,
            get_user_role_memberships,
            get_database_sizes,
            get_table_maintenance_stats,
            get_memory_configuration,
            get_postgresql_version_info,
            get_replication_status,
            # Generic tool execution (simplified signature)
            execute_tool,
            # Tool discovery functions
            list_available_tools,
            get_tool_info,
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
