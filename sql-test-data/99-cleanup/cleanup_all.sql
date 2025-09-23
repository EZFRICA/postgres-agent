-- ============================================================================
-- PostgreSQL DBA Multi-Agent - Complete Cleanup Script
-- ============================================================================
-- This script cleans up all test data created by previous scripts
-- WARNING: Use ONLY on test databases!
-- ============================================================================

-- ============================================================================
-- 1. REMOVE TEST USERS (if created by an administrator)
-- ============================================================================

-- IMPORTANT: These commands require administrator privileges
-- They will only work if users were created by an administrator

-- Revoke privileges before deleting users (if they exist)
-- COMMENTED because the DBA agent cannot execute these commands
/*
REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA ecommerce_schema FROM test_createdb;
REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA analytics_schema FROM test_createrole;
REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA audit_schema FROM shared_service_account;
REVOKE ALL PRIVILEGES ON SCHEMA ecommerce_schema FROM test_createdb;
REVOKE ALL PRIVILEGES ON SCHEMA analytics_schema FROM test_createrole;
REVOKE ALL PRIVILEGES ON SCHEMA audit_schema FROM shared_service_account;

-- Révoquer les privilèges sur les objets publics
REVOKE SELECT ON ecommerce_schema.users FROM PUBLIC;
REVOKE SELECT ON audit_schema.login_logs FROM PUBLIC;
REVOKE SELECT ON public.user_details FROM PUBLIC;
REVOKE EXECUTE ON FUNCTION public.get_user_password(TEXT) FROM PUBLIC;

-- Supprimer les utilisateurs de test
DROP ROLE IF EXISTS test_superuser;
DROP ROLE IF EXISTS test_createdb;
DROP ROLE IF EXISTS test_createrole;
DROP ROLE IF EXISTS shared_service_account;
DROP ROLE IF EXISTS test_no_password;
DROP ROLE IF EXISTS test_weak_password;
DROP ROLE IF EXISTS dangerous_parent_role;
DROP ROLE IF EXISTS child_role;
DROP ROLE IF EXISTS escalation_risk;
*/

-- ============================================================================
-- 2. REMOVE DANGEROUS SECURITY OBJECTS
-- ============================================================================

-- Remove dangerous functions
DROP FUNCTION IF EXISTS public.get_user_password(TEXT);
DROP FUNCTION IF EXISTS test_security_schema.admin_function(TEXT);
DROP FUNCTION IF EXISTS test_security_schema.get_any_user_data(INTEGER);

-- Remove views with data leaks
DROP VIEW IF EXISTS public.user_details;
DROP VIEW IF EXISTS test_security_schema.security_issues_summary;

-- Remove tables with sensitive data
DROP TABLE IF EXISTS public.sensitive_data;
DROP TABLE IF EXISTS test_security_schema.multi_tenant_data;
DROP TABLE IF EXISTS test_security_schema.unencrypted_sensitive;
DROP TABLE IF EXISTS test_security_schema.authentication_issues;
DROP TABLE IF EXISTS test_security_schema.audit_gaps;
DROP TABLE IF EXISTS test_security_schema.extension_risks;

-- ============================================================================
-- 3. REMOVE PERFORMANCE OBJECTS
-- ============================================================================

-- Remove performance monitoring views
DROP VIEW IF EXISTS test_performance_schema.problematic_queries;
DROP VIEW IF EXISTS test_performance_schema.blocking_info;
DROP VIEW IF EXISTS test_performance_schema.long_running_view;

-- Remove large test tables
DROP TABLE IF EXISTS test_performance_schema.large_table;
DROP TABLE IF EXISTS test_performance_schema.duplicate_data;

-- ============================================================================
-- 4. REMOVE MAINTENANCE OBJECTS
-- ============================================================================

-- Remove maintenance monitoring views
DROP VIEW IF EXISTS test_performance_schema.tables_needing_vacuum;
DROP VIEW IF EXISTS test_performance_schema.tables_needing_analyze;
DROP VIEW IF EXISTS test_performance_schema.unused_indexes;
DROP VIEW IF EXISTS test_performance_schema.database_size_monitoring;

-- Remove configuration tables and maintenance logs
DROP TABLE IF EXISTS test_performance_schema.maintenance_config_issues;
DROP TABLE IF EXISTS test_performance_schema.growing_table;
DROP TABLE IF EXISTS test_performance_schema.connection_issues;
DROP TABLE IF EXISTS test_performance_schema.log_growth_simulation;
DROP TABLE IF EXISTS test_performance_schema.backup_maintenance_issues;
DROP TABLE IF EXISTS test_performance_schema.replication_maintenance_issues;

-- ============================================================================
-- 5. CLEAN UP DATA IN MAIN TABLES
-- ============================================================================

-- Empty main tables (keep structure for future tests)
TRUNCATE TABLE ecommerce_schema.reviews CASCADE;
TRUNCATE TABLE ecommerce_schema.order_items CASCADE;
TRUNCATE TABLE ecommerce_schema.orders CASCADE;
TRUNCATE TABLE ecommerce_schema.products CASCADE;
TRUNCATE TABLE ecommerce_schema.categories CASCADE;
TRUNCATE TABLE ecommerce_schema.users CASCADE;

TRUNCATE TABLE analytics_schema.events CASCADE;
TRUNCATE TABLE analytics_schema.user_sessions CASCADE;
TRUNCATE TABLE analytics_schema.daily_metrics CASCADE;

TRUNCATE TABLE audit_schema.activity_logs CASCADE;
TRUNCATE TABLE audit_schema.login_logs CASCADE;

-- ============================================================================
-- 6. REMOVE REDUNDANT AND TEST INDEXES
-- ============================================================================

-- Remove redundant indexes created for tests
DROP INDEX IF EXISTS idx_redundant_users_email_1;
DROP INDEX IF EXISTS idx_redundant_users_email_2;
DROP INDEX IF EXISTS idx_redundant_orders_user_date;
DROP INDEX IF EXISTS idx_redundant_orders_date_user;

-- Remove unused indexes created for tests
DROP INDEX IF EXISTS idx_unused_products_weight;
DROP INDEX IF EXISTS idx_unused_reviews_title;
DROP INDEX IF EXISTS idx_unused_sessions_ip;

-- ============================================================================
-- 7. RESTORE IMPORTANT MISSING INDEXES
-- ============================================================================

-- Recreate indexes that were intentionally removed
CREATE INDEX IF NOT EXISTS idx_events_timestamp ON analytics_schema.events(timestamp);
CREATE INDEX IF NOT EXISTS idx_events_event_type ON analytics_schema.events(event_type);
CREATE INDEX IF NOT EXISTS idx_activity_logs_table_name ON audit_schema.activity_logs(table_name);
CREATE INDEX IF NOT EXISTS idx_products_price ON ecommerce_schema.products(price);
CREATE INDEX IF NOT EXISTS idx_order_items_product ON ecommerce_schema.order_items(product_id);

-- ============================================================================
-- 8. CLEAN UP STATISTICS AND OPTIMIZE
-- ============================================================================

-- Reset pg_stat_statements
-- COMMENTED: Requires special privileges
-- SELECT pg_stat_statements_reset();

-- Execute VACUUM and ANALYZE on all tables
-- COMMENTED: The DBA agent might not have privileges for VACUUM/ANALYZE
-- VACUUM ANALYZE;

-- ============================================================================
-- 9. FINAL VERIFICATION AND REPORT
-- ============================================================================

-- Create a cleanup report
DO $$
DECLARE
    remaining_test_objects INTEGER;
    remaining_test_users INTEGER;
    db_size_after TEXT;
    tables_count INTEGER;
    indexes_count INTEGER;
BEGIN
    -- Count remaining test objects
    SELECT count(*) INTO remaining_test_objects
    FROM information_schema.tables 
    WHERE table_name LIKE '%test%' OR table_name LIKE '%maintenance%';
    
    -- Count remaining test users
    SELECT count(*) INTO remaining_test_users
    FROM pg_roles 
    WHERE rolname LIKE 'test_%';
    
    -- Get database size after cleanup
    SELECT pg_size_pretty(pg_database_size(current_database())) INTO db_size_after;
    
    -- Count remaining tables in test schemas
    SELECT count(*) INTO tables_count
    FROM information_schema.tables 
    WHERE table_schema IN ('ecommerce_schema', 'analytics_schema', 'audit_schema', 'test_performance_schema', 'test_security_schema');
    
    -- Count indexes in test schemas
    SELECT count(*) INTO indexes_count
    FROM pg_indexes 
    WHERE schemaname IN ('ecommerce_schema', 'analytics_schema', 'audit_schema', 'test_performance_schema', 'test_security_schema');
    
    RAISE NOTICE '============================================================================';
    RAISE NOTICE 'PostgreSQL DBA Multi-Agent - Cleanup Complete!';
    RAISE NOTICE '============================================================================';
    RAISE NOTICE 'Cleanup Summary:';
    RAISE NOTICE '- Database size after cleanup: %', db_size_after;
    RAISE NOTICE '- Remaining test objects: %', remaining_test_objects;
    RAISE NOTICE '- Remaining test users: %', remaining_test_users;
    RAISE NOTICE '- Tables in test schemas: %', tables_count;
    RAISE NOTICE '- Indexes in test schemas: %', indexes_count;
    RAISE NOTICE '============================================================================';
    
    IF remaining_test_objects = 0 AND remaining_test_users = 0 THEN
        RAISE NOTICE 'SUCCESS: All test objects and users have been cleaned up!';
    ELSE
        RAISE NOTICE 'WARNING: Some test objects may still exist. Manual review recommended.';
    END IF;
    
    RAISE NOTICE '============================================================================';
    RAISE NOTICE 'The database is now clean and ready for new tests.';
    RAISE NOTICE 'You can re-run the test data scripts to recreate the test environment.';
    RAISE NOTICE '============================================================================';
END $$;

-- ============================================================================
-- 10. OPTIONAL: COMPLETELY REMOVE TEST SCHEMAS
-- ============================================================================

-- Uncomment the following lines if you want to completely remove schemas
-- WARNING: This will remove ALL data and structures in these schemas!

/*
DROP SCHEMA IF EXISTS test_performance_schema CASCADE;
DROP SCHEMA IF EXISTS test_security_schema CASCADE;
-- Keep main schemas but empty for future tests
-- DROP SCHEMA IF EXISTS ecommerce_schema CASCADE;
-- DROP SCHEMA IF EXISTS analytics_schema CASCADE;
-- DROP SCHEMA IF EXISTS audit_schema CASCADE;
*/

RAISE NOTICE 'Cleanup script execution completed successfully!';
