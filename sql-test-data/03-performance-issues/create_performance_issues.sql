-- ============================================================================
-- PostgreSQL DBA Multi-Agent - Performance Issues Creation
-- ============================================================================
-- This script intentionally creates performance issues to test
-- the capabilities of the Performance Agent
-- ============================================================================

-- ============================================================================
-- 1. CREATE MISSING INDEXES (performance issues)
-- ============================================================================

-- Remove important indexes to create problems
DROP INDEX IF EXISTS idx_events_timestamp;
DROP INDEX IF EXISTS idx_events_event_type;
DROP INDEX IF EXISTS idx_activity_logs_table_name;
DROP INDEX IF EXISTS idx_products_price;
DROP INDEX IF EXISTS idx_order_items_product;

-- Leave important tables without indexes on frequently queried columns
-- These queries will become slow and will be detected by the agent

-- ============================================================================
-- 2. CREATE SLOW AND PROBLEMATIC QUERIES
-- ============================================================================

-- Function to execute slow queries and populate pg_stat_statements
-- Create in test_performance_schema instead of public
CREATE OR REPLACE FUNCTION test_performance_schema.create_slow_queries()
RETURNS void AS $$
BEGIN
    -- Query 1: Full table scan without index (events by timestamp)
    PERFORM count(*) FROM analytics_schema.events 
    WHERE timestamp > NOW() - INTERVAL '7 days'
    AND event_type = 'purchase';
    
    -- Query 2: Expensive join without appropriate index
    PERFORM o.order_id, u.username, p.product_name
    FROM ecommerce_schema.orders o
    JOIN ecommerce_schema.users u ON o.user_id = u.user_id
    JOIN ecommerce_schema.order_items oi ON o.order_id = oi.order_id
    JOIN ecommerce_schema.products p ON oi.product_id = p.product_id
    WHERE o.order_date > NOW() - INTERVAL '30 days'
    AND p.price > 100;
    
    -- Query 3: Slow correlated subquery
    PERFORM p.product_name,
           (SELECT count(*) FROM ecommerce_schema.reviews r WHERE r.product_id = p.product_id) as review_count
    FROM ecommerce_schema.products p
    WHERE p.price > 50;
    
    -- Query 4: Text search without index
    PERFORM * FROM test_performance_schema.large_table
    WHERE data_column4 LIKE '%lorem%';
    
    -- Query 5: Aggregation on large table without index
    PERFORM data_column2, count(*), avg(data_column3)
    FROM test_performance_schema.large_table
    GROUP BY data_column2
    HAVING count(*) > 1;
    
    RAISE NOTICE 'Slow queries executed to populate pg_stat_statements';
END;
$$ LANGUAGE plpgsql;

-- Execute slow queries multiple times to create statistics
SELECT test_performance_schema.create_slow_queries();
SELECT test_performance_schema.create_slow_queries();
SELECT test_performance_schema.create_slow_queries();

-- ============================================================================
-- 3. CREATE BLOCKING SESSIONS AND DEADLOCKS
-- ============================================================================

-- Create a function to simulate locks
CREATE OR REPLACE FUNCTION test_performance_schema.simulate_blocking_sessions()
RETURNS void AS $$
DECLARE
    pid1 INTEGER;
    pid2 INTEGER;
BEGIN
    -- Start a long transaction that will block
    -- (This is for simulation - in practice, you should use separate sessions)
    
    -- Simulate an UPDATE that takes time
    UPDATE ecommerce_schema.products SET inventory_count = inventory_count + 1 
    WHERE product_id BETWEEN 1 AND 100;
    
    -- Create a temporary table to simulate a lock
    CREATE TEMP TABLE IF NOT EXISTS temp_lock_test (id INTEGER, data TEXT);
    
    -- Insert data to create activity
    INSERT INTO temp_lock_test SELECT i, 'data' || i FROM generate_series(1, 1000) i;
    
    RAISE NOTICE 'Blocking simulation setup complete';
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- 4. CREATE BUFFER CACHE PROBLEMS
-- ============================================================================

-- Create a query that forces cache misses
CREATE OR REPLACE FUNCTION test_performance_schema.create_cache_pressure()
RETURNS void AS $$
BEGIN
    -- Query that will force reading a lot of data
    PERFORM count(*) FROM (
        SELECT * FROM test_performance_schema.large_table 
        ORDER BY RANDOM() 
        LIMIT 10000
    ) subq;
    
    -- Query that accesses a lot of different data
    PERFORM l1.id, l2.id 
    FROM test_performance_schema.large_table l1
    CROSS JOIN test_performance_schema.large_table l2
    WHERE l1.id < 1000 AND l2.id < 1000
    AND l1.data_column2 + l2.data_column2 > 500000;
    
    RAISE NOTICE 'Cache pressure queries executed';
END;
$$ LANGUAGE plpgsql;

SELECT test_performance_schema.create_cache_pressure();

-- ============================================================================
-- 5. CREATE OBSOLETE STATISTICS
-- ============================================================================

-- Modify a lot of data without ANALYZE to create obsolete statistics
UPDATE ecommerce_schema.products SET price = price * 1.1 WHERE product_id % 2 = 0;
UPDATE test_performance_schema.large_table SET data_column2 = data_column2 + 1000 WHERE id % 3 = 0;
DELETE FROM test_performance_schema.duplicate_data WHERE id % 10 = 0;

-- ============================================================================
-- 6. CREATE LONG TRANSACTIONS
-- ============================================================================

-- Create a view that simulates a long transaction
CREATE OR REPLACE VIEW test_performance_schema.long_running_view AS
WITH RECURSIVE long_calculation AS (
    SELECT 1 as n, 1 as fib_prev, 1 as fib_curr
    UNION ALL
    SELECT n + 1, fib_curr, fib_prev + fib_curr
    FROM long_calculation
    WHERE n < 1000
)
SELECT n, fib_curr FROM long_calculation;

-- ============================================================================
-- 7. CREATE QUERIES WITH CARTESIAN PRODUCTS
-- ============================================================================

CREATE OR REPLACE FUNCTION test_performance_schema.create_cartesian_products()
RETURNS void AS $$
BEGIN
    -- Query with accidental Cartesian product (missing join condition)
    PERFORM u.username, p.product_name
    FROM ecommerce_schema.users u, ecommerce_schema.products p
    WHERE u.user_id <= 10 AND p.product_id <= 100;
    
    -- Another problematic query
    PERFORM c1.category_name, c2.category_name
    FROM ecommerce_schema.categories c1, ecommerce_schema.categories c2
    WHERE c1.category_id != c2.category_id;
    
    RAISE NOTICE 'Cartesian product queries executed';
END;
$$ LANGUAGE plpgsql;

SELECT test_performance_schema.create_cartesian_products();

-- ============================================================================
-- 8. CREATE CONCURRENCY PROBLEMS
-- ============================================================================

-- Add more data to a table to create contention
INSERT INTO test_performance_schema.duplicate_data (duplicate_field, search_field, random_data)
SELECT 
    'hot_spot_' || (i % 10), -- A lot of contention on a few values
    'concurrent_access_' || i,
    repeat('X', 1000) -- Larger data for more I/O
FROM generate_series(1, 10000) i;

-- ============================================================================
-- 9. CONFIGURE SUB-OPTIMAL PARAMETERS
-- ============================================================================

-- Note: These parameters require SUPERUSER privileges
-- They are commented but shown as examples of what the agent should detect

/*
-- Parameters that the agent should recommend optimizing:
-- work_mem too small for sorts
-- shared_buffers too small for workload
-- effective_cache_size misconfigured
-- random_page_cost not optimized for SSD

SHOW work_mem;           -- Agent should suggest increasing if < 4MB
SHOW shared_buffers;     -- Agent should analyze vs. workload
SHOW effective_cache_size; -- Agent should check vs. system memory
SHOW random_page_cost;   -- Agent should suggest 1.1 for SSD
*/

-- ============================================================================
-- 10. CREATE MONITORING QUERIES FOR THE AGENT
-- ============================================================================

-- Create views to help the agent detect problems
-- Adapted for PostgreSQL 13+ (total_exec_time/mean_exec_time columns)
CREATE OR REPLACE VIEW test_performance_schema.problematic_queries AS
SELECT 
    query,
    calls,
    total_exec_time as total_time,  -- PostgreSQL 13+
    mean_exec_time as mean_time,    -- PostgreSQL 13+
    rows,
    100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
FROM pg_stat_statements
WHERE calls > 5
ORDER BY total_exec_time DESC;

-- View of potential blocking sessions
CREATE OR REPLACE VIEW test_performance_schema.blocking_info AS
SELECT 
    blocked_locks.pid AS blocked_pid,
    blocked_activity.usename AS blocked_user,
    blocking_locks.pid AS blocking_pid,
    blocking_activity.usename AS blocking_user,
    blocked_activity.query AS blocked_statement,
    blocking_activity.query AS current_statement_in_blocking_process
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks 
    ON blocking_locks.locktype = blocked_locks.locktype
    AND blocking_locks.DATABASE IS NOT DISTINCT FROM blocked_locks.DATABASE
    AND blocking_locks.relation IS NOT DISTINCT FROM blocked_locks.relation
    AND blocking_locks.page IS NOT DISTINCT FROM blocked_locks.page
    AND blocking_locks.tuple IS NOT DISTINCT FROM blocked_locks.tuple
    AND blocking_locks.virtualxid IS NOT DISTINCT FROM blocked_locks.virtualxid
    AND blocking_locks.transactionid IS NOT DISTINCT FROM blocked_locks.transactionid
    AND blocking_locks.classid IS NOT DISTINCT FROM blocked_locks.classid
    AND blocking_locks.objid IS NOT DISTINCT FROM blocked_locks.objid
    AND blocking_locks.objsubid IS NOT DISTINCT FROM blocked_locks.objsubid
    AND blocking_locks.pid != blocked_locks.pid
JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.GRANTED;

-- ============================================================================
-- SUMMARY AND VALIDATION
-- ============================================================================

-- Execute ANALYZE on some tables only (leave others with obsolete stats)
-- COMMENTED: The DBA agent might not have privileges to ANALYZE
-- ANALYZE ecommerce_schema.users;
-- ANALYZE ecommerce_schema.categories;
-- DO NOT analyze: ecommerce_schema.products, test_performance_schema.large_table

-- Display a summary of created problems
DO $$
DECLARE
    slow_queries_count INTEGER;
    missing_indexes_count INTEGER;
    large_table_size TEXT;
BEGIN
    SELECT count(*) INTO slow_queries_count 
    FROM pg_stat_statements 
    WHERE mean_exec_time > 100; -- Queries > 100ms on average
    
    -- Approximately count missing indexes by checking tables without indexes on important columns
    missing_indexes_count := 5; -- Estimation based on removed indexes
    
    SELECT pg_size_pretty(pg_total_relation_size('test_performance_schema.large_table')) INTO large_table_size;
    
    RAISE NOTICE '============================================================================';
    RAISE NOTICE 'PostgreSQL DBA Multi-Agent - Performance Issues Created Successfully!';
    RAISE NOTICE '============================================================================';
    RAISE NOTICE 'Performance problems to detect:';
    RAISE NOTICE '- Slow queries in pg_stat_statements: %', slow_queries_count;
    RAISE NOTICE '- Missing indexes: % (estimated)', missing_indexes_count;
    RAISE NOTICE '- Large table size: %', large_table_size;
    RAISE NOTICE '- Obsolete statistics on critical tables';
    RAISE NOTICE '- Cache pressure from large data scans';
    RAISE NOTICE '- Potential blocking sessions';
    RAISE NOTICE '============================================================================';
    RAISE NOTICE 'Test your Performance Agent with questions like:';
    RAISE NOTICE '- "Why is my database slow?"';
    RAISE NOTICE '- "Analyze query performance and suggest optimizations"';
    RAISE NOTICE '- "What are the slowest queries?"';
    RAISE NOTICE '- "Check for missing indexes"';
    RAISE NOTICE '============================================================================';
    RAISE NOTICE 'Next step: Run 04-security-issues/create_security_issues.sql';
    RAISE NOTICE '============================================================================';
END $$;

-- ============================================================================
-- CLEANUP OF TEMPORARY FUNCTIONS (COMMENTED FOR TESTS)
-- ============================================================================
-- REMINDER: Uncomment these lines at the end of tests to clean up functions
-- DROP FUNCTION IF EXISTS test_performance_schema.create_slow_queries();
-- DROP FUNCTION IF EXISTS test_performance_schema.simulate_blocking_sessions();
-- DROP FUNCTION IF EXISTS test_performance_schema.create_cache_pressure();
-- DROP FUNCTION IF EXISTS test_performance_schema.create_cartesian_products();
