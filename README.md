# PostgreSQL DBA Multi-Agent System

A multi-agent system built with Google's Agent Development Kit (ADK) for comprehensive PostgreSQL database administration, monitoring, and optimization.

## 🎯 Overview

This system provides intelligent database administration through specialized agents that can analyze performance, security, maintenance, and schema issues in PostgreSQL databases. Each agent is designed to handle specific aspects of database management, working together to provide comprehensive insights and recommendations.

## 🏗️ Architecture

### Core Components

- **Coordinator Agent**: Orchestrates multi-agent workflows and coordinates complex database analysis
- **Performance Agent**: Identifies and analyzes performance bottlenecks, slow queries, and optimization opportunities
- **Security Agent**: Audits database security, user privileges, and identifies vulnerabilities
- **Maintenance Agent**: Monitors table maintenance needs, index usage, and database health
- **Schema Agent**: Analyzes database schema design and suggests improvements
- **Synthesis Agent**: Combines results from multiple agents into comprehensive reports

### Technology Stack

- **Google Agent Development Kit (ADK)**: Core agent framework
- **MCP Toolbox for PostgreSQL**: Database tools and utilities
- **PostgreSQL**: Target database system
- **Python**: Primary development language

## 🚀 Quick Start

### Prerequisites

This guide assumes you have already done the following:

- **Python 3.9+** (including pip and your preferred virtual environment tool for managing dependencies e.g. venv)
- **PostgreSQL 16+** and the psql client
- **Google Cloud credentials** (for ADK) - Optional if using Vertex AI

### Cloud Setup (Optional)

If you plan to use Google Cloud's Vertex AI with your agent, follow these one-time setup steps for local development:

1. **Install the Google Cloud CLI**
2. **Set up Application Default Credentials (ADC)**
3. **Set your project and enable Vertex AI**
   ```bash
   gcloud config set project YOUR_PROJECT_ID
   gcloud services enable aiplatform.googleapis.com
   ```

### Step 1: Set up your database

1. **Connect to PostgreSQL**
   ```bash
   psql -h 127.0.0.1 -U postgres
   ```

2. **Create a new database and user (IAM-based)**
   ```sql
   -- For IAM-based authentication, 
   CREATE DATABASE toolbox_db;
   GRANT ALL PRIVILEGES ON DATABASE toolbox_db TO iam_user;
   ALTER DATABASE toolbox_db OWNER TO iam_user;
   \q
   ```

3. **Connect with your new user (IAM authentication)**
   ```bash
   # Using IAM authentication (no password required)
   psql -h 127.0.0.1 -U iam_user -d toolbox_db
   ```

4. **Set up test data (optional)**
   ```bash
   # Run the test data scripts to populate your database
   psql -h 127.0.0.1 -U iam_user -d toolbox_db -f sql-test-data/01-schema/create_schema.sql
   psql -h 127.0.0.1 -U iam_user -d toolbox_db -f sql-test-data/02-data/populate_data.sql
   ```

### Step 2: Install and configure Toolbox

1. **Download the latest version of Toolbox**
   ```bash
   export OS="linux/amd64" # one of linux/amd64, darwin/arm64, darwin/amd64, or windows/amd64
   curl -O https://storage.googleapis.com/genai-toolbox/v0.14.0/$OS/toolbox
   chmod +x toolbox
   ```

2. **Configure your tools.yaml**
   The project includes a pre-configured `mcp-toolbox-postgres/tools.yaml` file with comprehensive PostgreSQL DBA tools.

3. **Run the Toolbox server**
   ```bash
   ./toolbox --tools-file "mcp-toolbox-postgres/tools.yaml"
   ```

### Step 3: Install and run the DBA Agent

1. **Install dependencies**
   ```bash
   pip install toolbox-core google-adk
   ```

2. **Configure environment variables**
   ```bash
   export GOOGLE_API_KEY="your-api-key"
   export DATABASE_HOST="127.0.0.1"
   export DATABASE_PORT="5432"
   export DATABASE_NAME="toolbox_db"
   export DATABASE_USER="iam_user"
   # No password needed with IAM authentication
   ```

3. **Run the DBA Agent**
   ```bash
   python postgres-dba-agent/agent.py
   ```

## 📊 Available Agents

### Performance Analysis
- **Slow Query Detection**: Identifies queries with poor performance
- **Index Analysis**: Finds missing, unused, or redundant indexes
- **Blocking Sessions**: Detects and analyzes blocking processes
- **Cache Hit Ratios**: Monitors buffer cache efficiency

### Security Auditing
- **User Privilege Analysis**: Reviews user permissions and roles
- **Authentication Methods**: Audits authentication configurations
- **Access Control Review**: Identifies security vulnerabilities
- **Data Exposure Detection**: Finds sensitive data exposure risks

### Maintenance Monitoring
- **Table Bloat Analysis**: Identifies tables needing VACUUM
- **Statistics Monitoring**: Tracks outdated table statistics
- **Index Maintenance**: Suggests index optimization
- **Database Size Monitoring**: Tracks database growth

### Schema Analysis
- **Design Pattern Review**: Identifies schema anti-patterns
- **Constraint Analysis**: Reviews foreign key and constraint design
- **Data Type Optimization**: Suggests data type improvements
- **Normalization Assessment**: Evaluates database normalization

## 🛠️ Configuration

### Environment Variables

```bash
# Database Configuration (IAM-based)
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=your_database
DATABASE_USER=your_username
# No password needed with IAM authentication

# ADK Configuration
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json

# Agent Configuration
SPECIALIZED_AGENTS_MODEL=gemini-1.5-pro
COORDINATOR_MODEL=gemini-1.5-pro
TOOLBOX_URL=http://localhost:5000
```

### MCP Toolbox Configuration

The MCP toolbox is configured via `mcp-toolbox-postgres/tools.yaml`. This file contains:
- Database connection settings
- Available tools and their parameters
- Tool descriptions and usage instructions

## 📁 Project Structure

```
postgres-agent/
├── postgres-dba-agent/          # Main agent system
│   ├── agent.py                 # Main coordinator agent
│   ├── config.py               # Configuration settings
│   ├── subagents/              # Specialized agents
│   │   ├── performance_agent.py
│   │   ├── security_agent.py
│   │   ├── maintenance_agent.py
│   │   └── ...
│   └── utils/                  # Utility functions
├── mcp-toolbox-postgres/       # MCP toolbox configuration
│   └── tools.yaml             # Tool definitions
├── sql-test-data/             # Test data and scenarios
│   ├── 01-schema/            # Schema creation scripts
│   ├── 02-data/              # Data population scripts
│   ├── 03-performance-issues/ # Performance test scenarios
│   ├── 04-security-issues/   # Security test scenarios
│   ├── 05-maintenance-issues/ # Maintenance test scenarios
│   └── 99-cleanup/           # Cleanup scripts
└── README.md                  # This file
```

## 🧪 Testing

### Test Data Setup

The project includes comprehensive test data to validate agent capabilities:

1. **Schema Creation**: Creates realistic e-commerce and analytics schemas
2. **Data Population**: Generates test data with various patterns
3. **Performance Issues**: Introduces intentional performance problems
4. **Security Issues**: Creates security vulnerabilities for testing
5. **Maintenance Issues**: Generates maintenance scenarios

### Running Tests

```bash
# Set up test environment
psql -h localhost -U postgres -d test_database -f sql-test-data/01-schema/create_schema.sql
psql -h localhost -U postgres -d test_database -f sql-test-data/02-data/populate_data.sql

# Run performance tests
psql -h localhost -U postgres -d test_database -f sql-test-data/03-performance-issues/create_performance_issues.sql

# Run security tests
psql -h localhost -U postgres -d test_database -f sql-test-data/04-security-issues/create_security_issues.sql

# Run maintenance tests
psql -h localhost -U postgres -d test_database -f sql-test-data/05-maintenance-issues/create_maintenance_issues.sql

# Clean up after testing
psql -h localhost -U postgres -d test_database -f sql-test-data/99-cleanup/cleanup_all.sql
```

## 🚀 Deployment

### Agent Deployment

For deploying the ADK-based agents, follow the official Google ADK deployment guide:

**[Deploy to Container-friendly Infrastructure](https://google.github.io/adk-docs/deploy/#other-container-friendly-infrastructure)**

This covers deployment options including:
- Agent Engine in Vertex AI
- Cloud Run
- Google Kubernetes Engine (GKE)
- Other container-friendly infrastructure

### MCP Toolbox Deployment

For deploying the MCP toolbox service, follow the official MCP Toolbox deployment guide:

**[Deploy MCP Toolbox to Cloud Run](https://googleapis.github.io/genai-toolbox/how-to/deploy_toolbox/)**

This covers:
- Cloud Run deployment
- Kubernetes deployment
- Docker Compose deployment
- Configuration and secrets management

## 📈 Usage Examples

### Performance Analysis
```python
# Analyze slow queries
result = await performance_agent.analyze_slow_queries()

# Check for missing indexes
result = await performance_agent.find_missing_indexes()

# Monitor blocking sessions
result = await performance_agent.get_blocking_sessions()
```

### Security Auditing
```python
# Audit user privileges
result = await security_agent.audit_user_privileges()

# Check authentication methods
result = await security_agent.analyze_authentication()

# Review access controls
result = await security_agent.review_access_controls()
```

### Maintenance Monitoring
```python
# Check table maintenance needs
result = await maintenance_agent.get_table_maintenance_stats("users")

# Find unused indexes
result = await maintenance_agent.get_unused_indexes()

# Monitor database size
result = await maintenance_agent.get_database_sizes()
```

## 🔧 Troubleshooting

### MCP Toolbox Issues

1. **Toolbox Connection Errors**
   - Verify toolbox is running on correct port (default: 5000)
   - Check `TOOLBOX_URL` in configuration
   - Ensure tools.yaml file is properly formatted
   - Review toolbox logs for errors

2. **Tool Execution Errors**
   - Verify database credentials in tools.yaml (IAM-based authentication)
   - Check database permissions for iam_user
   - Ensure database exists and is accessible
   - Verify IAM roles and permissions are properly configured

### Agent Execution Issues

1. **Google Cloud Credentials**
   - Verify `GOOGLE_API_KEY` is set correctly
   - For Vertex AI, ensure Application Default Credentials are configured
   - Check project permissions and API enablement

2. **Model Access Issues**
   - Verify model access permissions
   - Check quota limits
   - Review agent logs for specific errors


### Logging

The system provides comprehensive logging at multiple levels:
- Agent execution logs
- Tool execution logs
- Database query logs
- Error and warning logs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 🙏 Acknowledgments

- Google Agent Development Kit (ADK)
- MCP Toolbox for PostgreSQL
- PostgreSQL community
- Google Cloud Platform

## 📞 Support

For issues and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the official ADK and MCP documentation

---

**Note**: This system is designed for PostgreSQL databases. Ensure you have appropriate permissions and follow security best practices when deploying in production environments.
