-- ============================================================================
-- PostgreSQL DBA Multi-Agent - Performance Issues Creation
-- ============================================================================
-- Ce script crée intentionnellement des problèmes de performance pour tester
-- les capacités du Performance Agent
-- ============================================================================

-- ============================================================================
-- 1. CRÉER DES INDEX MANQUANTS (problèmes de performance)
-- ============================================================================

-- Supprimer des index importants pour créer des problèmes
DROP INDEX IF EXISTS idx_events_timestamp;
DROP INDEX IF EXISTS idx_events_event_type;
DROP INDEX IF EXISTS idx_activity_logs_table_name;
DROP INDEX IF EXISTS idx_products_price;
DROP INDEX IF EXISTS idx_order_items_product;

-- Laisser des tables importantes sans index sur des colonnes fréquemment interrogées
-- Ces requêtes deviendront lentes et seront détectées par l'agent

-- ============================================================================
-- 2. CRÉER DES REQUÊTES LENTES ET PROBLÉMATIQUES
-- ============================================================================

-- Fonction pour exécuter des requêtes lentes et populer pg_stat_statements
-- Créer dans test_performance_schema au lieu de public
CREATE OR REPLACE FUNCTION test_performance_schema.create_slow_queries()
RETURNS void AS $$
BEGIN
    -- Requête 1: Scan de table complète sans index (events par timestamp)
    PERFORM count(*) FROM analytics_schema.events 
    WHERE timestamp > NOW() - INTERVAL '7 days'
    AND event_type = 'purchase';
    
    -- Requête 2: Join coûteux sans index approprié
    PERFORM o.order_id, u.username, p.product_name
    FROM ecommerce_schema.orders o
    JOIN ecommerce_schema.users u ON o.user_id = u.user_id
    JOIN ecommerce_schema.order_items oi ON o.order_id = oi.order_id
    JOIN ecommerce_schema.products p ON oi.product_id = p.product_id
    WHERE o.order_date > NOW() - INTERVAL '30 days'
    AND p.price > 100;
    
    -- Requête 3: Sous-requête corrélée lente
    PERFORM p.product_name,
           (SELECT count(*) FROM ecommerce_schema.reviews r WHERE r.product_id = p.product_id) as review_count
    FROM ecommerce_schema.products p
    WHERE p.price > 50;
    
    -- Requête 4: Recherche de texte sans index
    PERFORM * FROM test_performance_schema.large_table
    WHERE data_column4 LIKE '%lorem%';
    
    -- Requête 5: Agrégation sur grande table sans index
    PERFORM data_column2, count(*), avg(data_column3)
    FROM test_performance_schema.large_table
    GROUP BY data_column2
    HAVING count(*) > 1;
    
    RAISE NOTICE 'Slow queries executed to populate pg_stat_statements';
END;
$$ LANGUAGE plpgsql;

-- Exécuter les requêtes lentes plusieurs fois pour créer des statistiques
SELECT test_performance_schema.create_slow_queries();
SELECT test_performance_schema.create_slow_queries();
SELECT test_performance_schema.create_slow_queries();

-- ============================================================================
-- 3. CRÉER DES SESSIONS BLOQUANTES ET DES DEADLOCKS
-- ============================================================================

-- Créer une fonction pour simuler des locks
CREATE OR REPLACE FUNCTION test_performance_schema.simulate_blocking_sessions()
RETURNS void AS $$
DECLARE
    pid1 INTEGER;
    pid2 INTEGER;
BEGIN
    -- Démarrer une transaction longue qui va bloquer
    -- (Ceci est pour simulation - en pratique, vous devriez utiliser des sessions séparées)
    
    -- Simuler un UPDATE qui prend du temps
    UPDATE ecommerce_schema.products SET inventory_count = inventory_count + 1 
    WHERE product_id BETWEEN 1 AND 100;
    
    -- Créer une table temporaire pour simuler un lock
    CREATE TEMP TABLE IF NOT EXISTS temp_lock_test (id INTEGER, data TEXT);
    
    -- Insérer des données pour créer de l'activité
    INSERT INTO temp_lock_test SELECT i, 'data' || i FROM generate_series(1, 1000) i;
    
    RAISE NOTICE 'Blocking simulation setup complete';
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- 4. CRÉER DES PROBLÈMES DE BUFFER CACHE
-- ============================================================================

-- Créer une requête qui force des cache misses
CREATE OR REPLACE FUNCTION test_performance_schema.create_cache_pressure()
RETURNS void AS $$
BEGIN
    -- Requête qui va forcer la lecture de beaucoup de données
    PERFORM count(*) FROM (
        SELECT * FROM test_performance_schema.large_table 
        ORDER BY RANDOM() 
        LIMIT 10000
    ) subq;
    
    -- Requête qui accède à beaucoup de données différentes
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
-- 5. CRÉER DES STATISTIQUES OBSOLÈTES
-- ============================================================================

-- Modifier beaucoup de données sans ANALYZE pour créer des statistiques obsolètes
UPDATE ecommerce_schema.products SET price = price * 1.1 WHERE product_id % 2 = 0;
UPDATE test_performance_schema.large_table SET data_column2 = data_column2 + 1000 WHERE id % 3 = 0;
DELETE FROM test_performance_schema.duplicate_data WHERE id % 10 = 0;

-- ============================================================================
-- 6. CRÉER DES TRANSACTIONS LONGUES
-- ============================================================================

-- Créer une vue qui simule une transaction longue
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
-- 7. CRÉER DES REQUÊTES AVEC CARTESIAN PRODUCTS
-- ============================================================================

CREATE OR REPLACE FUNCTION test_performance_schema.create_cartesian_products()
RETURNS void AS $$
BEGIN
    -- Requête avec produit cartésien accidentel (join condition manquante)
    PERFORM u.username, p.product_name
    FROM ecommerce_schema.users u, ecommerce_schema.products p
    WHERE u.user_id <= 10 AND p.product_id <= 100;
    
    -- Autre requête problématique
    PERFORM c1.category_name, c2.category_name
    FROM ecommerce_schema.categories c1, ecommerce_schema.categories c2
    WHERE c1.category_id != c2.category_id;
    
    RAISE NOTICE 'Cartesian product queries executed';
END;
$$ LANGUAGE plpgsql;

SELECT test_performance_schema.create_cartesian_products();

-- ============================================================================
-- 8. CRÉER DES PROBLÈMES DE CONCURRENCE
-- ============================================================================

-- Ajouter plus de données à une table pour créer de la contention
INSERT INTO test_performance_schema.duplicate_data (duplicate_field, search_field, random_data)
SELECT 
    'hot_spot_' || (i % 10), -- Beaucoup de contention sur quelques valeurs
    'concurrent_access_' || i,
    repeat('X', 1000) -- Données plus larges pour plus d'I/O
FROM generate_series(1, 10000) i;

-- ============================================================================
-- 9. CONFIGURER DES PARAMÈTRES SOUS-OPTIMAUX
-- ============================================================================

-- Note: Ces paramètres nécessitent des privilèges SUPERUSER
-- Ils sont commentés mais montrés comme exemple de ce que l'agent devrait détecter

/*
-- Paramètres que l'agent devrait recommander d'optimiser:
-- work_mem trop petit pour les sorts
-- shared_buffers trop petit pour la charge de travail
-- effective_cache_size mal configuré
-- random_page_cost pas optimisé pour SSD

SHOW work_mem;           -- L'agent devrait suggérer d'augmenter si < 4MB
SHOW shared_buffers;     -- L'agent devrait analyser vs. charge de travail
SHOW effective_cache_size; -- L'agent devrait vérifier vs. mémoire système
SHOW random_page_cost;   -- L'agent devrait suggérer 1.1 pour SSD
*/

-- ============================================================================
-- 10. CRÉER DES REQUÊTES DE MONITORING POUR L'AGENT
-- ============================================================================

-- Créer des vues pour aider l'agent à détecter les problèmes
-- Adaptée pour PostgreSQL 13+ (colonnes total_exec_time/mean_exec_time)
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

-- Vue des sessions bloquantes potentielles
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
-- RÉCAPITULATIF ET VALIDATION
-- ============================================================================

-- Exécuter ANALYZE sur certaines tables seulement (laisser d'autres avec des stats obsolètes)
-- COMMENTÉ: L'agent DBA pourrait ne pas avoir les privilèges pour ANALYZE
-- ANALYZE ecommerce_schema.users;
-- ANALYZE ecommerce_schema.categories;
-- NE PAS analyser: ecommerce_schema.products, test_performance_schema.large_table

-- Afficher un résumé des problèmes créés
DO $$
DECLARE
    slow_queries_count INTEGER;
    missing_indexes_count INTEGER;
    large_table_size TEXT;
BEGIN
    SELECT count(*) INTO slow_queries_count 
    FROM pg_stat_statements 
    WHERE mean_exec_time > 100; -- Requêtes > 100ms en moyenne
    
    -- Compter approximativement les index manquants en vérifiant les tables sans index sur colonnes importantes
    missing_indexes_count := 5; -- Estimation basée sur les index supprimés
    
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
-- NETTOYAGE DES FONCTIONS TEMPORAIRES (COMMENTÉ POUR LES TESTS)
-- ============================================================================
-- RAPPEL: Décommenter ces lignes à la fin des tests pour nettoyer les fonctions
-- DROP FUNCTION IF EXISTS test_performance_schema.create_slow_queries();
-- DROP FUNCTION IF EXISTS test_performance_schema.simulate_blocking_sessions();
-- DROP FUNCTION IF EXISTS test_performance_schema.create_cache_pressure();
-- DROP FUNCTION IF EXISTS test_performance_schema.create_cartesian_products();
