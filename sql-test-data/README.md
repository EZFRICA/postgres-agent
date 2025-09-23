# PostgreSQL DBA Multi-Agent - Test Data SQL Scripts

SQL scripts to populate your PostgreSQL database with realistic test data that will demonstrate all the capabilities of your multi-agent DBA system.

## 🎯 Objective

Create realistic database scenarios that will trigger and demonstrate:

- **Performance Issues**: Slow queries, blocking sessions, index problems
- **Security Vulnerabilities**: Weak access controls, weak authentication
- **Schema Issues**: Bloated tables, missing indexes, design anti-patterns
- **Maintenance Needs**: VACUUM requirements, configuration problems

## 🚀 Quick Usage

```bash
# 1. Connect to your PostgreSQL database
psql -h localhost -U postgres -d your_database

# 2. Execute scripts in order
\i sql-test-data/01-schema/create_schema.sql
\i sql-test-data/02-data/populate_data.sql
\i sql-test-data/03-performance-issues/create_performance_issues.sql
\i sql-test-data/04-security-issues/create_security_issues.sql
\i sql-test-data/05-maintenance-issues/create_maintenance_issues.sql

# 3. Test your DBA agent
# "Why is my database slow?" → Performance Agent
# "Audit database security" → Security Agent
# etc.

# 4. Cleanup after tests
\i sql-test-data/99-cleanup/cleanup_all.sql
```

## 📁 Script Structure

```
sql-test-data/
├── 01-schema/           # Basic schema creation
│   └── create_schema.sql
├── 02-data/             # Data population
│   ├── populate_data.sql
│   └── insert_large_datasets.sql
├── 03-performance-issues/  # Performance problems creation
│   ├── create_performance_issues.sql
│   ├── missing_indexes.sql
│   └── slow_queries.sql
├── 04-security-issues/     # Security vulnerabilities creation
│   ├── create_security_issues.sql
│   ├── weak_users.sql
│   └── poor_permissions.sql
├── 05-maintenance-issues/  # Maintenance problems creation
│   ├── create_maintenance_issues.sql
│   ├── bloated_tables.sql
│   └── config_issues.sql
└── 99-cleanup/            # Cleanup scripts
    └── cleanup_all.sql
```

## 🎲 Test Scenarios Created

### Performance (Performance Agent)
- Tables with millions of rows without appropriate indexes
- Queries with Cartesian products
- Blocking sessions and deadlocks
- Cache misses and I/O intensive operations

### Security (Security Agent)
- Users with excessive privileges
- Weak authentication methods
- Public objects with sensitive data
- Missing row-level security policies

### Schema (Schema Agent)
- Bloated tables (>20% bloat)
- Unused and redundant indexes
- Poor data type choices
- Missing foreign key constraints

### Maintenance (Maintenance Agent)
- Tables requiring VACUUM
- Obsolete statistics
- Sub-optimal configuration parameters
- Simulated database growth

## ⚠️ Important Notes

- **Use only on test databases**: These scripts intentionally create problems
- **Resource usage**: Large datasets will consume disk space and memory
- **Backup**: Consider backing up your database before extensive testing
- **Cleanup**: Use cleanup scripts after testing

## 🧪 Validation

After executing the scripts, your PostgreSQL DBA Multi-Agent system should be able to:

1. **Detect performance issues** and suggest optimizations
2. **Find security vulnerabilities** and recommend fixes
3. **Analyze schema issues** and propose improvements
4. **Plan maintenance** and optimize configuration
5. **Handle complex problems** with coordinated multi-domain analysis
