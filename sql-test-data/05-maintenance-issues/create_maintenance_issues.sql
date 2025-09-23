-- ============================================================================
-- PostgreSQL DBA Multi-Agent - Maintenance Issues Creation
-- ============================================================================
-- This script intentionally creates maintenance issues to test
-- the capabilities of the Maintenance Agent
-- ============================================================================

-- ============================================================================
-- 1. CREATE TABLES REQUIRING VACUUM AND ANALYZE
-- ============================================================================

-- Simulate many UPDATEs and DELETEs to create bloat
UPDATE ecommerce_schema.products SET price = price * 1.01 WHERE product_id % 2 = 0;
UPDATE ecommerce_schema.products SET price = price * 0.99 WHERE product_id % 2 = 1;
UPDATE ecommerce_schema.users SET updated_at = NOW() WHERE user_id % 3 = 0;

-- Create bloat with repeated DELETEs and INSERTs
DELETE FROM test_performance_schema.duplicate_data WHERE id % 5 = 0;
INSERT INTO test_performance_schema.duplicate_data (duplicate_field, search_field, random_data)
SELECT 
    'maintenance_test_' || i,
    'needs_vacuum_' || i,
    repeat('BLOAT_DATA_', 100)
FROM generate_series(1, 5000) i;

-- ============================================================================
-- 2. CREATE UNUSED AND REDUNDANT INDEXES
-- ============================================================================

-- Redundant indexes (cover the same columns)
CREATE INDEX idx_redundant_users_email_1 ON ecommerce_schema.users(email);
CREATE INDEX idx_redundant_users_email_2 ON ecommerce_schema.users(email, username);
CREATE INDEX idx_redundant_orders_user_date ON ecommerce_schema.orders(user_id, order_date);
CREATE INDEX idx_redundant_orders_date_user ON ecommerce_schema.orders(order_date, user_id);

-- Unused indexes (do not match any query pattern)
CREATE INDEX idx_unused_products_weight ON ecommerce_schema.products(weight);
CREATE INDEX idx_unused_reviews_title ON ecommerce_schema.reviews(title);
CREATE INDEX idx_unused_sessions_ip ON analytics_schema.user_sessions(ip_address);

-- ============================================================================
-- 3. CREATE STATISTICS PROBLEMS
-- ============================================================================

-- Modify a lot of data without ANALYZE
INSERT INTO analytics_schema.events (session_id, user_id, event_type, event_data, timestamp)
SELECT 
    (SELECT session_id FROM analytics_schema.user_sessions ORDER BY RANDOM() LIMIT 1),
    (2 + (RANDOM() * 8)::INTEGER),
    'maintenance_event',
    ('{"maintenance": true, "timestamp": "' || NOW() || '"}')::JSONB,
    NOW() - (RANDOM() * INTERVAL '30 days')
FROM generate_series(1, 10000);

-- Do not execute ANALYZE to leave statistics obsolete

-- ============================================================================
-- 4. CREATE CONFIGURATION PROBLEMS
-- ============================================================================

-- Create a table documenting configuration problems
CREATE TABLE IF NOT EXISTS test_performance_schema.maintenance_config_issues (
    issue_type VARCHAR(50),
    current_setting TEXT,
    recommended_setting TEXT,
    impact_description TEXT,
    priority VARCHAR(10)
);

INSERT INTO test_performance_schema.maintenance_config_issues VALUES
('autovacuum_naptime', '1min', '30s', 'Autovacuum runs too infrequently for high-write workload', 'HIGH'),
('checkpoint_completion_target', '0.5', '0.9', 'Checkpoints complete too quickly, causing I/O spikes', 'MEDIUM'),
('effective_cache_size', '4GB', '75% of RAM', 'Query planner underestimates available cache', 'HIGH'),
('shared_buffers', '128MB', '25% of RAM', 'Buffer pool too small for workload', 'HIGH'),
('work_mem', '4MB', '64MB', 'Sort operations spill to disk unnecessarily', 'MEDIUM'),
('maintenance_work_mem', '64MB', '1GB', 'VACUUM and index operations are slow', 'MEDIUM'),
('wal_buffers', '16MB', '64MB', 'WAL buffer too small causing frequent flushes', 'LOW'),
('random_page_cost', '4.0', '1.1', 'Cost model inappropriate for SSD storage', 'MEDIUM');

-- ============================================================================
-- 5. CREATE DATABASE SIZE PROBLEMS
-- ============================================================================

-- Create a table that grows quickly
CREATE TABLE IF NOT EXISTS test_performance_schema.growing_table (
    id BIGSERIAL PRIMARY KEY,
    data_payload TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Insert a lot of data to simulate rapid growth
INSERT INTO test_performance_schema.growing_table (data_payload)
SELECT repeat('GROWTH_SIMULATION_DATA_', 1000)
FROM generate_series(1, 1000);

-- ============================================================================
-- 6. CREATE IDLE CONNECTIONS AND SESSION PROBLEMS
-- ============================================================================

-- Simulate connection problems (documented)
CREATE TABLE IF NOT EXISTS test_performance_schema.connection_issues (
    issue_type VARCHAR(50),
    description TEXT,
    recommendation TEXT
);

INSERT INTO test_performance_schema.connection_issues VALUES
('idle_connections', 'Many connections in idle state consuming resources', 'Implement connection pooling'),
('long_running_transactions', 'Transactions open for extended periods', 'Review application transaction management'),
('connection_limit_reached', 'Database hitting max_connections limit', 'Increase max_connections or optimize connection usage'),
('too_many_prepared_statements', 'Excessive prepared statements consuming memory', 'Review prepared statement lifecycle');

-- ============================================================================
-- 7. CREATE LOG AND AUDIT PROBLEMS
-- ============================================================================

-- Simulate large logs
CREATE TABLE IF NOT EXISTS test_performance_schema.log_growth_simulation (
    log_entry_id BIGSERIAL PRIMARY KEY,
    log_level VARCHAR(10),
    log_message TEXT,
    log_timestamp TIMESTAMP DEFAULT NOW()
);

-- Insert large log entries
INSERT INTO test_performance_schema.log_growth_simulation (log_level, log_message)
SELECT 
    CASE (RANDOM() * 4)::INTEGER
        WHEN 0 THEN 'ERROR'
        WHEN 1 THEN 'WARNING'
        WHEN 2 THEN 'INFO'
        ELSE 'DEBUG'
    END,
    'Maintenance test log entry ' || i || ' - ' || repeat('LOG_DATA_', 50)
FROM generate_series(1, 5000) i;

-- ============================================================================
-- 8. CREATE BACKUP AND ARCHIVING PROBLEMS
-- ============================================================================

-- Table documenting backup problems
CREATE TABLE IF NOT EXISTS test_performance_schema.backup_maintenance_issues (
    backup_type VARCHAR(50),
    issue_description TEXT,
    risk_level VARCHAR(10),
    recommendation TEXT
);

INSERT INTO test_performance_schema.backup_maintenance_issues VALUES
('full_backup', 'Full backups taking too long and impacting performance', 'HIGH', 'Schedule during low-usage periods, consider parallel backup'),
('wal_archiving', 'WAL archive location running out of space', 'CRITICAL', 'Monitor archive location disk space, implement cleanup policy'),
('backup_verification', 'Backup integrity not regularly verified', 'HIGH', 'Implement automated backup testing'),
('retention_policy', 'Backup retention policy not enforced', 'MEDIUM', 'Implement automated cleanup of old backups'),
('point_in_time_recovery', 'PITR testing not performed regularly', 'HIGH', 'Schedule regular PITR recovery tests');

-- ============================================================================
-- 9. CREATE REPLICATION PROBLEMS (if applicable)
-- ============================================================================

-- Table documenting replication problems
CREATE TABLE IF NOT EXISTS test_performance_schema.replication_maintenance_issues (
    replication_aspect VARCHAR(50),
    issue_description TEXT,
    monitoring_query TEXT,
    fix_recommendation TEXT
);

INSERT INTO test_performance_schema.replication_maintenance_issues VALUES
('replication_lag', 'Standby servers lagging behind primary', 'SELECT * FROM pg_stat_replication;', 'Check network, increase wal_sender_timeout'),
('wal_sender_slots', 'Replication slots consuming too much disk space', 'SELECT * FROM pg_replication_slots;', 'Monitor slot usage, clean up unused slots'),
('hot_standby_feedback', 'Hot standby feedback causing bloat on primary', 'SELECT * FROM pg_stat_database;', 'Tune hot_standby_feedback setting'),
('streaming_replication', 'Streaming replication connection issues', 'SELECT state FROM pg_stat_replication;', 'Check network connectivity and authentication');

-- ============================================================================
-- 10. CREATE MONITORING VIEWS FOR THE AGENT
-- ============================================================================

-- View to detect tables requiring VACUUM
CREATE OR REPLACE VIEW test_performance_schema.tables_needing_vacuum AS
SELECT 
    schemaname,
    relname as tablename,
    n_dead_tup,
    n_live_tup,
    CASE 
        WHEN n_live_tup > 0 
        THEN (n_dead_tup::FLOAT / n_live_tup::FLOAT) * 100 
        ELSE 0 
    END AS dead_tuple_percent,
    last_vacuum,
    last_autovacuum
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000 
   OR (n_live_tup > 0 AND (n_dead_tup::FLOAT / n_live_tup::FLOAT) > 0.1);

-- View to detect tables requiring ANALYZE
CREATE OR REPLACE VIEW test_performance_schema.tables_needing_analyze AS
SELECT 
    schemaname,
    relname as tablename,
    n_mod_since_analyze,
    last_analyze,
    last_autoanalyze
FROM pg_stat_user_tables
WHERE n_mod_since_analyze > 1000
   OR last_analyze IS NULL
   OR last_autoanalyze IS NULL;

-- View to detect unused indexes
CREATE OR REPLACE VIEW test_performance_schema.unused_indexes AS
SELECT 
    schemaname,
    relname as tablename,
    indexrelname as indexname,
    idx_scan,
    pg_size_pretty(pg_relation_size(indexrelid)) as size
FROM pg_stat_user_indexes
WHERE idx_scan < 10
  AND pg_relation_size(indexrelid) > 1024 * 1024; -- Plus de 1MB

-- View to monitor database growth
CREATE OR REPLACE VIEW test_performance_schema.database_size_monitoring AS
SELECT 
    datname,
    pg_size_pretty(pg_database_size(datname)) as size,
    pg_database_size(datname) as size_bytes
FROM pg_database
WHERE datname = current_database();

-- ============================================================================
-- SUMMARY AND VALIDATION OF MAINTENANCE PROBLEMS
-- ============================================================================

-- Display a summary of created maintenance problems
DO $$
DECLARE
    tables_needing_vacuum INTEGER;
    unused_indexes_count INTEGER;
    db_size TEXT;
    config_issues_count INTEGER;
BEGIN
    -- Count tables requiring VACUUM (estimation based on modifications)
    SELECT count(*) INTO tables_needing_vacuum 
    FROM pg_stat_user_tables 
    WHERE n_dead_tup > 1000 
       OR (n_live_tup > 0 AND (n_dead_tup::FLOAT / n_live_tup::FLOAT) > 0.1);
    
    -- Count unused indexes (estimation)
    SELECT count(*) INTO unused_indexes_count 
    FROM pg_stat_user_indexes 
    WHERE idx_scan < 10 AND pg_relation_size(indexrelid) > 1024 * 1024;
    
    SELECT pg_size_pretty(pg_database_size(current_database())) INTO db_size;
    
    SELECT count(*) INTO config_issues_count 
    FROM test_performance_schema.maintenance_config_issues;
    
    RAISE NOTICE '============================================================================';
    RAISE NOTICE 'PostgreSQL DBA Multi-Agent - Maintenance Issues Created Successfully!';
    RAISE NOTICE '============================================================================';
    RAISE NOTICE 'Maintenance problems to detect:';
    RAISE NOTICE '- Tables needing VACUUM: %', tables_needing_vacuum;
    RAISE NOTICE '- Unused indexes: %', unused_indexes_count;
    RAISE NOTICE '- Database size: %', db_size;
    RAISE NOTICE '- Configuration issues documented: %', config_issues_count;
    RAISE NOTICE '- Obsolete statistics on multiple tables';
    RAISE NOTICE '- Backup and replication issues documented';
    RAISE NOTICE '============================================================================';
    RAISE NOTICE 'Test your Maintenance Agent with questions like:';
    RAISE NOTICE '- "Identify tables that need maintenance"';
    RAISE NOTICE '- "Check for unused indexes"';
    RAISE NOTICE '- "Analyze database performance configuration"';
    RAISE NOTICE '- "Review backup and maintenance policies"';
    RAISE NOTICE '============================================================================';
    RAISE NOTICE 'Next step: Run 99-cleanup/cleanup_all.sql when testing is complete';
    RAISE NOTICE '============================================================================';
END $$;

-- ============================================================================
-- CLEANUP OF MAINTENANCE OBJECTS (COMMENTED FOR TESTS)
-- ============================================================================
-- REMINDER: Uncomment these lines at the end of tests to clean up objects
-- DROP VIEW IF EXISTS test_performance_schema.tables_needing_vacuum;
-- DROP VIEW IF EXISTS test_performance_schema.tables_needing_analyze;
-- DROP VIEW IF EXISTS test_performance_schema.unused_indexes;
-- DROP VIEW IF EXISTS test_performance_schema.database_size_monitoring;
-- DROP TABLE IF EXISTS test_performance_schema.maintenance_config_issues;
-- DROP TABLE IF EXISTS test_performance_schema.growing_table;
-- DROP TABLE IF EXISTS test_performance_schema.connection_issues;
-- DROP TABLE IF EXISTS test_performance_schema.log_growth_simulation;
-- DROP TABLE IF EXISTS test_performance_schema.backup_maintenance_issues;
-- DROP TABLE IF EXISTS test_performance_schema.replication_maintenance_issues;
