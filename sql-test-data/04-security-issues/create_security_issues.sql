-- ============================================================================
-- PostgreSQL DBA Multi-Agent - Security Issues Creation
-- ============================================================================
-- This script intentionally creates security vulnerabilities to test
-- the capabilities of the Security Agent
--
-- USAGE MODES:
-- 1. DBA AGENT (limited privileges): Execute this script as is
--    - Creates tables and views with security problems
--    - Documents problems that the agent can detect
--    - Sections requiring admin privileges are commented
--
-- 2. ADMINISTRATOR (SUPERUSER privileges): Uncomment admin sections
--    - Can create real users with problematic privileges
--    - Can apply dangerous permissions
--    - Creates a more complete test environment
--
-- IMPORTANT: Commented sections require SUPERUSER privileges
-- ============================================================================

-- ============================================================================
-- 1. DOCUMENT USER PROBLEMS (instead of creating them)
-- ============================================================================

-- Create a table to document user security issues
CREATE TABLE IF NOT EXISTS test_security_schema.user_security_issues (
    issue_type VARCHAR(50),
    description TEXT,
    risk_level VARCHAR(10),
    current_state TEXT,
    recommendation TEXT
);

-- Document the types of problems the agent should detect
INSERT INTO test_security_schema.user_security_issues VALUES
('superuser_privileges', 'Users with unnecessary SUPERUSER privileges', 'CRITICAL', 'Multiple non-admin users have SUPERUSER', 'Remove SUPERUSER from non-admin accounts'),
('createdb_privileges', 'Users with CREATEDB privileges who dont need them', 'HIGH', 'Service accounts have CREATEDB', 'Revoke CREATEDB from service accounts'),
('createrole_privileges', 'Users who can create other roles', 'HIGH', 'Non-admin users can create roles', 'Limit CREATEROLE to DBAs only'),
('shared_accounts', 'Shared service accounts used by multiple applications', 'HIGH', 'Single account used by multiple services', 'Create separate accounts per service'),
('no_password', 'Users without passwords', 'CRITICAL', 'Accounts exist with no authentication', 'Set passwords for all accounts'),
('weak_passwords', 'Users with weak passwords', 'HIGH', 'Passwords like 123, password, etc.', 'Enforce strong password policy');

-- ============================================================================
-- 1bis. CREATE USERS WITH EXCESSIVE PRIVILEGES (COMMENTED)
-- ============================================================================
-- WARNING: These commands require SUPERUSER privileges
-- Uncomment and execute as administrator if you want to create real test users

-- -- User with superuser privileges (high risk)
-- CREATE ROLE test_superuser WITH LOGIN SUPERUSER PASSWORD 'weak_password_123';
-- COMMENT ON ROLE test_superuser IS 'Test user with excessive superuser privileges';

-- -- User with database creation privileges
-- CREATE ROLE test_createdb WITH LOGIN CREATEDB PASSWORD 'another_weak_password';
-- COMMENT ON ROLE test_createdb IS 'Test user with database creation privileges';

-- -- User with role creation privileges
-- CREATE ROLE test_createrole WITH LOGIN CREATEROLE PASSWORD 'password123';
-- COMMENT ON ROLE test_createrole IS 'Test user with role creation privileges';

-- -- Shared service user (bad practice)
-- CREATE ROLE shared_service_account WITH LOGIN PASSWORD 'shared_secret';
-- COMMENT ON ROLE shared_service_account IS 'Shared service account (security risk)';

-- -- User without password (critical risk)
-- CREATE ROLE test_no_password WITH LOGIN;
-- COMMENT ON ROLE test_no_password IS 'User without password - critical security risk';

-- -- User with weak password
-- CREATE ROLE test_weak_password WITH LOGIN PASSWORD '123';
-- COMMENT ON ROLE test_weak_password IS 'User with very weak password';

-- ============================================================================
-- 2. CREATE PERMISSION PROBLEMS (what the agent can do)
-- ============================================================================

-- The agent can create tables with problematic permissions in test schemas
-- Create a table with exposed sensitive data (security risk)
CREATE TABLE IF NOT EXISTS test_security_schema.exposed_user_data (
    user_id INTEGER,
    username VARCHAR(50),
    email_domain VARCHAR(100),
    last_login_ip INET,
    failed_login_count INTEGER,
    account_status VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Insert simulated data
INSERT INTO test_security_schema.exposed_user_data (user_id, username, email_domain, last_login_ip, failed_login_count, account_status) VALUES
(1, 'admin_user', 'company.com', '192.168.1.100', 0, 'active'),
(2, 'service_account', 'internal.local', '10.0.0.50', 5, 'locked'),
(3, 'test_user', 'external.com', '203.0.113.45', 12, 'suspicious');

-- Create a view that exposes too much information
CREATE OR REPLACE VIEW test_security_schema.user_login_summary AS
SELECT 
    user_id,
    username,
    email_domain,
    last_login_ip,
    failed_login_count,
    CASE 
        WHEN failed_login_count > 10 THEN 'Security Risk'
        WHEN failed_login_count > 5 THEN 'Monitoring Required' 
        ELSE 'Normal'
    END as risk_assessment
FROM test_security_schema.exposed_user_data;

-- ============================================================================
-- 2bis. EXCESSIVE PERMISSIONS (COMMENTED - requires admin privileges)
-- ============================================================================
-- These commands require administrator privileges to GRANT on existing schemas

-- -- Grant ALL PRIVILEGES on critical schemas
-- GRANT ALL PRIVILEGES ON SCHEMA ecommerce_schema TO test_createdb;
-- GRANT ALL PRIVILEGES ON SCHEMA analytics_schema TO test_createrole;
-- GRANT ALL PRIVILEGES ON SCHEMA audit_schema TO shared_service_account;

-- -- Public permissions on sensitive tables (very risky)
-- GRANT SELECT ON ecommerce_schema.users TO PUBLIC;
-- GRANT SELECT ON audit_schema.login_logs TO PUBLIC;

-- ============================================================================
-- 3. CREATE OBJECTS IN PUBLIC SCHEMA (security risk)
-- ============================================================================

-- Table with exposed sensitive data  
CREATE TABLE test_security_schema.sensitive_data (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    credit_card_number VARCHAR(20), -- Unencrypted sensitive data
    ssn VARCHAR(11),                -- Social security number
    password_backup TEXT,           -- Passwords in plain text
    api_secret_key TEXT,            -- API keys in plain text
    created_at TIMESTAMP DEFAULT NOW()
);

-- Insert fake sensitive data
INSERT INTO test_security_schema.sensitive_data (user_id, credit_card_number, ssn, password_backup, api_secret_key) VALUES
(1, '4532-1234-5678-9012', '123-45-6789', 'user_password_123', 'sk_test_abc123def456'),
(2, '5678-9012-3456-7890', '987-65-4321', 'another_password', 'ak_prod_xyz789uvw012'),
(3, '9012-3456-7890-1234', '555-66-7777', 'weak_pwd', 'secret_key_qwerty123');

-- Dangerous function accessible to everyone
CREATE OR REPLACE FUNCTION test_security_schema.get_user_password(username TEXT)
RETURNS TEXT AS $$
BEGIN
    RETURN (SELECT password_backup FROM test_security_schema.sensitive_data WHERE user_id = (
        SELECT user_id FROM ecommerce_schema.users WHERE ecommerce_schema.users.username = $1
    ));
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- COMMENTED: Requires privileges to GRANT EXECUTE
-- GRANT EXECUTE ON FUNCTION public.get_user_password(TEXT) TO PUBLIC;

-- ============================================================================
-- 4. CREATE VIEWS WITH DATA LEAKS
-- ============================================================================

-- View that exposes sensitive data
CREATE VIEW test_security_schema.user_details AS
SELECT 
    u.user_id,
    u.username,
    u.email,
    u.password_hash,  -- Exposed password hash
    u.phone,
    sd.credit_card_number,
    sd.ssn
FROM ecommerce_schema.users u
LEFT JOIN test_security_schema.sensitive_data sd ON u.user_id = sd.user_id;

-- COMMENTED: Requires privileges to GRANT SELECT
-- GRANT SELECT ON public.user_details TO PUBLIC;

-- ============================================================================
-- 5. CONFIGURE WEAK AUTHENTICATION METHODS
-- ============================================================================

-- Note: These configurations require modification of pg_hba.conf
-- Here is what the security agent should detect as problematic:

/*
Problematic configurations to detect in pg_hba.conf:
- host all all 0.0.0.0/0 trust          # Trust without authentication
- host all all 0.0.0.0/0 md5            # Weak MD5 instead of scram-sha-256
- local all all trust                    # Local connections without password
- host all postgres 0.0.0.0/0 password  # Plain text password
*/

-- Create database entries to document configuration problems
CREATE TABLE IF NOT EXISTS test_security_schema.authentication_issues (
    issue_type VARCHAR(50),
    description TEXT,
    risk_level VARCHAR(10),
    recommendation TEXT
);

INSERT INTO test_security_schema.authentication_issues VALUES
('trust_method', 'Trust authentication allows connections without password', 'CRITICAL', 'Replace trust with scram-sha-256'),
('md5_method', 'MD5 authentication is cryptographically weak', 'HIGH', 'Upgrade to scram-sha-256'),
('password_method', 'Plain password authentication sends passwords in clear text', 'HIGH', 'Use scram-sha-256 or certificate authentication'),
('wide_host_access', 'Host entries allow connections from any IP (0.0.0.0/0)', 'MEDIUM', 'Restrict to specific IP ranges'),
('postgres_remote_access', 'Postgres superuser allowed remote connections', 'CRITICAL', 'Restrict postgres user to local connections only');

-- ============================================================================
-- 6. CREATE ROLES WITH PROBLEMATIC INHERITANCE
-- ============================================================================

-- COMMENTED: Role creation requires administrator privileges
-- CREATE ROLE dangerous_parent_role WITH CREATEDB CREATEROLE;
-- CREATE ROLE child_role WITH LOGIN PASSWORD 'child_pass';

-- COMMENTED: Requires privileges to GRANT roles
-- GRANT dangerous_parent_role TO child_role;

-- COMMENTED: These commands require privileges to create roles
-- CREATE ROLE escalation_risk WITH LOGIN PASSWORD 'escalate_me';
-- GRANT test_createrole TO escalation_risk; -- Peut créer d'autres rôles

-- ============================================================================
-- 7. CREATE ROW LEVEL SECURITY PROBLEMS
-- ============================================================================

-- Sensitive table without Row Level Security enabled
CREATE TABLE test_security_schema.multi_tenant_data (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    sensitive_info TEXT,
    financial_data DECIMAL(15,2),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Insert multi-tenant data
INSERT INTO test_security_schema.multi_tenant_data (tenant_id, user_id, sensitive_info, financial_data) VALUES
(1, 101, 'Tenant 1 secret data', 50000.00),
(1, 102, 'More tenant 1 data', 75000.00),
(2, 201, 'Tenant 2 confidential info', 30000.00),
(2, 202, 'Tenant 2 financial details', 120000.00),
(3, 301, 'Tenant 3 sensitive content', 95000.00);

-- COMMENTED: Requires privileges to GRANT SELECT
-- GRANT SELECT ON test_security_schema.multi_tenant_data TO test_weak_password;

-- ============================================================================
-- 8. CREATE DANGEROUS SECURITY DEFINER FUNCTIONS
-- ============================================================================

-- Function with SECURITY DEFINER that can be exploited
CREATE OR REPLACE FUNCTION test_security_schema.admin_function(query TEXT)
RETURNS TEXT AS $$
BEGIN
    -- Dangerous function that executes dynamic SQL
    EXECUTE query;
    RETURN 'Query executed';
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- COMMENTED: Requires privileges to GRANT EXECUTE
-- GRANT EXECUTE ON FUNCTION test_security_schema.admin_function(TEXT) TO test_weak_password;

-- Another problematic function
CREATE OR REPLACE FUNCTION test_security_schema.get_any_user_data(target_user_id INTEGER)
RETURNS TABLE(username TEXT, email TEXT, password_hash TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT u.username, u.email, u.password_hash
    FROM ecommerce_schema.users u
    WHERE u.user_id = target_user_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- COMMENTED: Requires privileges to GRANT EXECUTE
-- GRANT EXECUTE ON FUNCTION test_security_schema.get_any_user_data(INTEGER) TO PUBLIC;

-- ============================================================================
-- 9. CREATE INSUFFICIENT AUDIT LOGS
-- ============================================================================

-- Disable logging for critical operations (simulated)
CREATE TABLE test_security_schema.audit_schema_gaps (
    gap_type VARCHAR(50),
    description TEXT,
    risk_assessment TEXT
);

INSERT INTO test_security_schema.audit_schema_gaps VALUES
('no_ddl_logging', 'DDL operations (CREATE, ALTER, DROP) are not logged', 'Cannot detect unauthorized schema changes'),
('no_privilege_logging', 'GRANT/REVOKE operations are not logged', 'Cannot track privilege escalation'),
('no_login_failures', 'Failed login attempts are not comprehensively logged', 'Cannot detect brute force attacks'),
('no_data_access_logging', 'SELECT operations on sensitive tables are not logged', 'Cannot track data breaches'),
('log_retention_short', 'Audit logs are retained for less than 1 year', 'Insufficient for compliance requirements');

-- ============================================================================
-- 10. CREATE UNSECURED EXTENSIONS
-- ============================================================================

-- Note: These extensions require superuser privileges
-- Document potential problems
CREATE TABLE test_security_schema.extension_risks (
    extension_name VARCHAR(50),
    risk_description TEXT,
    mitigation TEXT
);

INSERT INTO test_security_schema.extension_risks VALUES
('dblink', 'Allows connections to other databases, potential data exfiltration', 'Restrict usage to specific trusted roles'),
('file_fdw', 'Allows reading arbitrary files from filesystem', 'Remove if not needed, restrict file access'),
('postgres_fdw', 'Allows connections to remote PostgreSQL servers', 'Ensure secure connection strings and access controls'),
('plpython', 'Allows execution of Python code, potential system access', 'Remove if not needed, sandbox execution');

-- ============================================================================
-- 11. CREATE ENCRYPTION PROBLEMS
-- ============================================================================

-- Table with unencrypted sensitive data
CREATE TABLE test_security_schema.unencrypted_sensitive (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER,
    credit_card_number VARCHAR(20),    -- Should be encrypted
    bank_account VARCHAR(20),          -- Should be encrypted
    social_security VARCHAR(11),       -- Should be encrypted
    medical_record_number VARCHAR(20), -- Should be encrypted
    notes TEXT                         -- Could contain sensitive info
);

-- Insert unencrypted data
INSERT INTO test_security_schema.unencrypted_sensitive VALUES
(1, 1001, '4532123456789012', '123456789', '123-45-6789', 'MR-2023-001', 'Patient has diabetes'),
(2, 1002, '5678901234567890', '987654321', '987-65-4321', 'MR-2023-002', 'Allergy to penicillin');

-- ============================================================================
-- SUMMARY AND VALIDATION OF SECURITY PROBLEMS
-- ============================================================================

-- Create a summary view for the security agent
CREATE VIEW test_security_schema.security_issues_summary AS
SELECT 
    'Excessive Privileges' as issue_category,
    count(*) as issue_count,
    'Users with superuser, createdb, or createrole privileges' as description
FROM pg_roles 
WHERE (rolsuper OR rolcreatedb OR rolcreaterole) 
  AND rolname LIKE 'test_%'

UNION ALL

SELECT 
    'Weak Passwords' as issue_category,
    3 as issue_count,
    'Users with weak or no passwords detected' as description

UNION ALL

SELECT 
    'Public Schema Exposure' as issue_category,
    count(*) as issue_count,
    'Sensitive objects in public schema' as description
FROM information_schema.tables 
WHERE table_schema = 'public' 
  AND table_name LIKE 'sensitive%'

UNION ALL

SELECT 
    'Missing Row Level Security' as issue_category,
    count(*) as issue_count,
    'Multi-tenant tables without RLS' as description
FROM information_schema.tables t
LEFT JOIN pg_class c ON c.relname = t.table_name
WHERE t.table_schema = 'test_security_schema' 
  AND t.table_name LIKE '%tenant%'
  AND (c.relrowsecurity IS NULL OR NOT c.relrowsecurity);

-- Display a summary of created security problems
DO $$
DECLARE
    risky_users_count INTEGER;
    public_objects_count INTEGER;
    definer_functions_count INTEGER;
BEGIN
    SELECT count(*) INTO risky_users_count 
    FROM pg_roles 
    WHERE rolname LIKE 'test_%' AND (rolsuper OR rolcreatedb OR rolcreaterole);
    
    SELECT count(*) INTO public_objects_count 
    FROM information_schema.tables 
    WHERE table_schema = 'public' AND table_name IN ('sensitive_data', 'user_details');
    
    SELECT count(*) INTO definer_functions_count
    FROM information_schema.routines 
    WHERE routine_schema IN ('public', 'test_security_schema') 
      AND security_type = 'DEFINER';
    
    RAISE NOTICE '============================================================================';
    RAISE NOTICE 'PostgreSQL DBA Multi-Agent - Security Issues Created Successfully!';
    RAISE NOTICE '============================================================================';
    RAISE NOTICE 'Security vulnerabilities to detect:';
    RAISE NOTICE '- Risky user accounts: %', risky_users_count;
    RAISE NOTICE '- Sensitive objects in public schema: %', public_objects_count;
    RAISE NOTICE '- SECURITY DEFINER functions: %', definer_functions_count;
    RAISE NOTICE '- Weak authentication methods documented';
    RAISE NOTICE '- Missing Row Level Security policies';
    RAISE NOTICE '- Excessive privileges granted';
    RAISE NOTICE '- Unencrypted sensitive data';
    RAISE NOTICE '============================================================================';
    RAISE NOTICE 'Test your Security Agent with questions like:';
    RAISE NOTICE '- "Audit database security and identify vulnerabilities"';
    RAISE NOTICE '- "Check user privileges and permissions"';
    RAISE NOTICE '- "Analyze authentication methods"';
    RAISE NOTICE '- "Review access controls and identify risks"';
    RAISE NOTICE '============================================================================';
    RAISE NOTICE 'Next step: Run 05-maintenance-issues/create_maintenance_issues.sql';
    RAISE NOTICE '============================================================================';
END $$;

-- ============================================================================
-- CLEANUP OF SECURITY OBJECTS (COMMENTED FOR TESTS)
-- ============================================================================
-- REMINDER: Uncomment these lines at the end of tests to clean up objects
-- DROP VIEW IF EXISTS test_security_schema.user_login_summary;
-- DROP VIEW IF EXISTS test_security_schema.user_details;
-- DROP VIEW IF EXISTS test_security_schema.security_issues_summary;
-- DROP TABLE IF EXISTS test_security_schema.exposed_user_data;
-- DROP TABLE IF EXISTS test_security_schema.user_security_issues;
-- DROP TABLE IF EXISTS test_security_schema.sensitive_data;
-- DROP TABLE IF EXISTS test_security_schema.authentication_issues;
-- DROP TABLE IF EXISTS test_security_schema.multi_tenant_data;
-- DROP TABLE IF EXISTS test_security_schema.audit_gaps;
-- DROP TABLE IF EXISTS test_security_schema.extension_risks;
-- DROP TABLE IF EXISTS test_security_schema.unencrypted_sensitive;
-- DROP FUNCTION IF EXISTS test_security_schema.get_user_password(TEXT);
-- DROP FUNCTION IF EXISTS test_security_schema.admin_function(TEXT);
-- DROP FUNCTION IF EXISTS test_security_schema.get_any_user_data(INTEGER);
