# 🧪 Complete Test Guide - PostgreSQL DBA Agent

This guide allows you to systematically test **all tools** and **all sub-agents**.

## 🏗️ Architecture Overview

**Important:** The PostgreSQL DBA Agent uses a **Coordinator-Centric Architecture**:

- **Coordinator Agent**: Has direct access to all PostgreSQL tools and executes all database operations
- **Specialized Sub-Agents** (Performance, Schema, Maintenance, Security): Provide expert guidance and recommendations but **redirect users to the Coordinator** for actual tool execution
- **Pedagogical Agent**: Explains PostgreSQL concepts and best practices
- **Synthesis Agent**: Combines results from multiple analyses

**When to use what:**
- 🎯 **Direct commands** → Coordinator executes tools directly
- 🔍 **Analysis requests** → Coordinator uses `execute_*_analysis` functions
- 📚 **Explanations** → PedagogicalAgent provides educational content
- 🔄 **Synthesis** → SynthesisAgent combines multiple results

---

## 📋 Table of Contents

1. [Direct Tool Tests](#1-direct-tool-tests)
2. [Specialized Sub-Agent Tests](#2-specialized-sub-agent-tests)
3. [Parameter Handling Tests](#3-parameter-handling-tests)
4. [Integration Tests](#4-integration-tests)
5. [Expected Results](#5-expected-results)

---

## 1. Direct Tool Tests

### 🔍 A. Performance Tools

#### Test 1.1: Active Queries
```
Command: What are the currently active queries?
Expected Tool: list_active_queries
Parameters: Optional (min_duration, exclude_application_names, limit)
Expected Result: List of all active queries (default: queries running at least 1 minute, limit 50)

Alternative Commands:
- "Show queries running for at least 5 minutes" → min_duration="5 minutes"
- "Show active queries excluding psql" → exclude_application_names="psql"
- "Show top 10 active queries" → limit=10
```

#### Test 1.2: Slowest Historical Queries
```
Command: Show me the 5 slowest historical queries
Expected Tool: get_slowest_historical_queries
Required Parameters: limit=5
Expected Result: Top 5 slowest queries with execution times
```

#### Test 1.3: Most I/O Intensive Queries
```
Command: Get the 4 most I/O intensive queries
Expected Tool: get_most_io_intensive_queries
Required Parameters: limit=4
Expected Result: Top 4 queries with most disk reads
```

#### Test 1.4: Most Frequent Queries
```
Command: List the 3 most frequent queries
Expected Tool: get_most_frequent_queries
Required Parameters: limit=3
Expected Result: Top 3 most executed queries
```

#### Test 1.5: Blocking Sessions
```
Command: Are there any blocking sessions?
Expected Tool: get_blocking_sessions
Parameters: None
Expected Result: List of sessions blocking other sessions
```

#### Test 1.6: Long Running Transactions
```
Command: Show me long running transactions
Expected Tool: get_long_running_transactions
Parameters: None
Expected Result: Transactions open for a long time
```

---

### 📊 B. Schema Tools

#### Test 2.1: List Schemas
```
Command: List all database schemas
Expected Tool: list_all_schemas
Parameters: None
Expected Result: List of all schemas with owners
```

#### Test 2.2: Tables in a Schema
```
Command: List all tables in the database
Expected Tool: list_database_tables
Parameters: Optional (table_names, output_format)
Expected Result: Complete structure of all database tables (default: detailed format)

Alternative Commands:
- "List tables orders,users,products" → table_names="orders,users,products"
- "List all table names" → output_format="simple"
- "Show structure of orders table" → table_names="orders", output_format="detailed"
```

#### Test 2.3: Table Sizes
```
Command: Get table sizes for ecommerce_schema, limit to 20 tables
Expected Tool: get_table_sizes_summary
Required Parameters: schema_name="ecommerce_schema", limit=20
Expected Result: Top 20 tables with their sizes
```

#### Test 2.4: Invalid Indexes
```
Command: Find invalid indexes
Expected Tool: find_invalid_indexes
Parameters: None
Expected Result: List of corrupted or invalid indexes
```

#### Test 2.5: Unused Indexes
```
Command: Get unused indexes larger than 5 MB
Expected Tool: get_unused_indexes
Required Parameters: min_size_mb=5
Expected Result: Unused indexes larger than 5 MB
```

---

### 🔐 C. Security Tools

#### Test 3.1: Users and Roles
```
Command: List all database users and roles
Expected Tool: get_database_users_and_roles
Parameters: None
Expected Result: Complete list of users with privileges
```

#### Test 3.2: Role Memberships
```
Command: What roles does user 'bokove@ezekias.dev' belong to?
Expected Tool: get_user_role_memberships
Required Parameters: username="bokove@ezekias.dev"
Expected Result: List of user's roles
```

#### Test 3.3: Table Permissions
```
Command: What permissions does 'bokove@ezekias.dev' have on ecommerce_schema.orders?
Expected Tool: get_user_table_permissions
Required Parameters: schema_name="ecommerce_schema", table_name="orders", username="bokove@ezekias.dev"
Expected Result: Direct and inherited permissions on the table
```

#### Test 3.4: Active Connections
```
Command: Show current database connections
Expected Tool: get_current_connections_summary
Parameters: None
Expected Result: Summary of active connections by user/application
```

---

### 🔧 D. Maintenance Tools

#### Test 4.1: Database Sizes
```
Command: Show database sizes
Expected Tool: get_database_sizes
Parameters: None
Expected Result: Size of all databases
```

#### Test 4.2: Memory Configuration
```
Command: Show memory configuration
Expected Tool: get_memory_configuration
Parameters: None
Expected Result: PostgreSQL memory configuration parameters
```

#### Test 4.3: PostgreSQL Version
```
Command: What PostgreSQL version are we running?
Expected Tool: get_postgresql_version_info
Parameters: None
Expected Result: Complete PostgreSQL version
```

#### Test 4.4: Replication Status
```
Command: Check replication status
Expected Tool: get_replication_status
Parameters: None
Expected Result: Replication status (if configured)
```

#### Test 4.5: Cache Ratios
```
Command: Show cache hit ratios
Expected Tool: get_cache_hit_ratios
Parameters: None
Expected Result: Buffer and index cache ratios
```

---

### 🔌 E. Extension Tools

#### Test 5.1: Installed Extensions
```
Command: List installed extensions
Expected Tool: list_installed_extensions
Parameters: None
Expected Result: Installed PostgreSQL extensions
```

#### Test 5.2: Available Extensions
```
Command: What extensions are available?
Expected Tool: list_available_extensions
Parameters: None
Expected Result: Extensions available for installation
```

---

## 2. Specialized Sub-Agent Tests

**IMPORTANT NOTE:** Sub-agents (PerformanceAgent, SchemaAgent, MaintenanceAgent, SecurityAgent) do not have direct access to PostgreSQL tools. They will redirect you to use the Coordinator Agent directly.

### 🚀 A. Performance Agent
#### Test 6.1: Comprehensive Performance Analysis
```
Command: Run a comprehensive performance analysis with limit 10
Expected Agent: PerformanceAgent
Required Parameters: limit=10
Expected Result: 
  - Active queries
  - Top 10 slow queries
  - Top 10 I/O intensive queries
  - Top 10 frequent queries
  - Blocking sessions
  - Long running transactions
  - Cache ratios
  - Memory configuration
```

#### Test 6.2: Query Analysis Only
```
Command: Analyze query performance with limit 5
Expected Agent: PerformanceAgent
Analysis Type: queries
Required Parameters: limit=5
Expected Result: Focus on queries (active + historical top 5)
```


---

### 📐 B. Schema Agent

#### Test 7.1: Comprehensive Schema Analysis
```
Command: Analyze ecommerce_schema comprehensively 
Expected Agent: SchemaAgent
Required Parameters: schema_name="ecommerce_schema"
Expected Result:
  - Table structure
  - Table sizes (top 20)
  - Invalid indexes
  - Unused indexes (>1MB)
```

#### Test 7.2: Structure Analysis
```
Command: Analyze structure of ecommerce_schema
Expected Agent: SchemaAgent
Analysis Type: structure
Required Parameters: schema_name="ecommerce_schema"
Expected Result: Detailed table structure
```

---

### 🔒 C. Security Agent

#### Test 8.1: Comprehensive Security Audit
```
Command: Run a comprehensive security audit
Expected Agent: SecurityAgent
Expected Result:
  - All users and roles
  - Active connections
  - Installed extensions
```

#### Test 8.2: User Audit
```
Command: Audit database users
Expected Agent: SecurityAgent
Audit Type: users
Expected Result: List of users with privileges
```

---

### 🔧 D. Maintenance Agent

#### Test 9.1: Comprehensive Maintenance Analysis
```
Command: Run comprehensive maintenance analysis for ecommerce_schema.orders with limit 20 and min_size_mb 1
Expected Agent: MaintenanceAgent
Required Parameters: schema_name="ecommerce_schema", table_name="orders", limit=20, min_size_mb=1
Expected Result:
  - Orders table maintenance
  - Invalid indexes
  - Unused indexes
  - Database sizes
  - Table sizes
  - PostgreSQL version
  - Replication status
```

---

### 📚 E. Pedagogical Agent

#### Test 10.1: Concept Explanation
```
Command: Explain what VACUUM does in PostgreSQL
Expected Agent: PedagogicalAgent
Expected Result: Detailed pedagogical explanation of VACUUM
```

#### Test 10.2: Best Practice
```
Command: What are best practices for indexing in PostgreSQL?
Expected Agent: PedagogicalAgent
Expected Result: Guide to indexing best practices
```

---

### 🔄 F. Synthesis Agent

#### Test 11.1: Multi-Result Synthesis
```
Command: Synthesize the results from performance and schema analysis
Expected Agent: SynthesisAgent
Expected Result: Consolidated synthesis with cross-recommendations
```

---

## 3. Parameter Handling Tests

### ❌ A. Missing Parameter Tests

#### Test 12.1: Slow Queries Without Limit
```
Command: Get slowest historical queries
Expected Result: Error requesting 'limit' parameter
Message: "Parameter 'limit' is required..."
```

#### Test 12.2: Table Sizes Without Schema
```
Command: Get table sizes
Expected Result: Error requesting 'schema_name' parameter
Message: "Parameter 'schema_name' is required..."
```

#### Test 12.3: Table Sizes Without Limit
```
Command: Get table sizes for ecommerce_schema
Expected Result: Error requesting 'limit' parameter
Message: "Parameter 'limit' is required..."
```

#### Test 12.4: Permissions Without Schema
```
Command: Get permissions for bokove@ezekias.dev on orders table
Expected Result: Error requesting 'schema_name' parameter
Message: "Parameter 'schema_name' is required..."
```

#### Test 12.5: Maintenance Without Schema
```
Command: Get maintenance stats for orders
Expected Result: Error requesting 'schema_name' parameter
Message: "Parameter 'schema_name' is required..."
```

---

### ✅ B. Valid Parameter Tests

#### Test 13.1: Simple Limit Extraction
```
Command: Get slowest queries, limit 5
Expected Result: Agent extracts limit=5 and executes
```

#### Test 13.2: Limit Extraction with "="
```
Command: Get slowest queries limit=10
Expected Result: Agent extracts limit=10 and executes
```

#### Test 13.3: Schema and Limit Extraction
```
Command: Get table sizes for schema ecommerce_schema with limit 20
Expected Result: Agent extracts schema_name="ecommerce_schema", limit=20
```

#### Test 13.4: Multiple Parameter Extraction
```
Command: Check permissions for user bokove@ezekias.dev on ecommerce_schema.orders
Expected Result: Agent extracts username, schema_name, table_name
```

