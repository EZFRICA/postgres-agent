-- ============================================================================
-- PostgreSQL DBA Multi-Agent - Complete Cleanup Script
-- ============================================================================
-- Ce script nettoie toutes les données de test créées par les scripts précédents
-- ATTENTION: Utiliser UNIQUEMENT sur des bases de données de test !
-- ============================================================================

-- ============================================================================
-- 1. SUPPRIMER LES UTILISATEURS DE TEST (si créés par un administrateur)
-- ============================================================================

-- IMPORTANT: Ces commandes nécessitent des privilèges administrateur
-- Elles ne fonctionneront que si les utilisateurs ont été créés par un administrateur

-- Révoquer les privilèges avant de supprimer les utilisateurs (si ils existent)
-- COMMENTÉ car l'agent DBA ne peut pas exécuter ces commandes
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
-- 2. SUPPRIMER LES OBJETS DE SÉCURITÉ DANGEREUX
-- ============================================================================

-- Supprimer les fonctions dangereuses
DROP FUNCTION IF EXISTS public.get_user_password(TEXT);
DROP FUNCTION IF EXISTS test_security_schema.admin_function(TEXT);
DROP FUNCTION IF EXISTS test_security_schema.get_any_user_data(INTEGER);

-- Supprimer les vues avec des fuites de données
DROP VIEW IF EXISTS public.user_details;
DROP VIEW IF EXISTS test_security_schema.security_issues_summary;

-- Supprimer les tables avec des données sensibles
DROP TABLE IF EXISTS public.sensitive_data;
DROP TABLE IF EXISTS test_security_schema.multi_tenant_data;
DROP TABLE IF EXISTS test_security_schema.unencrypted_sensitive;
DROP TABLE IF EXISTS test_security_schema.authentication_issues;
DROP TABLE IF EXISTS test_security_schema.audit_gaps;
DROP TABLE IF EXISTS test_security_schema.extension_risks;

-- ============================================================================
-- 3. SUPPRIMER LES OBJETS DE PERFORMANCE
-- ============================================================================

-- Supprimer les vues de monitoring de performance
DROP VIEW IF EXISTS test_performance_schema.problematic_queries;
DROP VIEW IF EXISTS test_performance_schema.blocking_info;
DROP VIEW IF EXISTS test_performance_schema.long_running_view;

-- Supprimer les grandes tables de test
DROP TABLE IF EXISTS test_performance_schema.large_table;
DROP TABLE IF EXISTS test_performance_schema.duplicate_data;

-- ============================================================================
-- 4. SUPPRIMER LES OBJETS DE MAINTENANCE
-- ============================================================================

-- Supprimer les vues de monitoring de maintenance
DROP VIEW IF EXISTS test_performance_schema.tables_needing_vacuum;
DROP VIEW IF EXISTS test_performance_schema.tables_needing_analyze;
DROP VIEW IF EXISTS test_performance_schema.unused_indexes;
DROP VIEW IF EXISTS test_performance_schema.database_size_monitoring;

-- Supprimer les tables de configuration et logs de maintenance
DROP TABLE IF EXISTS test_performance_schema.maintenance_config_issues;
DROP TABLE IF EXISTS test_performance_schema.growing_table;
DROP TABLE IF EXISTS test_performance_schema.connection_issues;
DROP TABLE IF EXISTS test_performance_schema.log_growth_simulation;
DROP TABLE IF EXISTS test_performance_schema.backup_maintenance_issues;
DROP TABLE IF EXISTS test_performance_schema.replication_maintenance_issues;

-- ============================================================================
-- 5. NETTOYER LES DONNÉES DANS LES TABLES PRINCIPALES
-- ============================================================================

-- Vider les tables principales (garder la structure pour des tests futurs)
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
-- 6. SUPPRIMER LES INDEX REDONDANTS ET DE TEST
-- ============================================================================

-- Supprimer les index redondants créés pour les tests
DROP INDEX IF EXISTS idx_redundant_users_email_1;
DROP INDEX IF EXISTS idx_redundant_users_email_2;
DROP INDEX IF EXISTS idx_redundant_orders_user_date;
DROP INDEX IF EXISTS idx_redundant_orders_date_user;

-- Supprimer les index inutilisés créés pour les tests
DROP INDEX IF EXISTS idx_unused_products_weight;
DROP INDEX IF EXISTS idx_unused_reviews_title;
DROP INDEX IF EXISTS idx_unused_sessions_ip;

-- ============================================================================
-- 7. REMETTRE LES INDEX MANQUANTS IMPORTANTS
-- ============================================================================

-- Recréer les index qui ont été supprimés intentionnellement
CREATE INDEX IF NOT EXISTS idx_events_timestamp ON analytics_schema.events(timestamp);
CREATE INDEX IF NOT EXISTS idx_events_event_type ON analytics_schema.events(event_type);
CREATE INDEX IF NOT EXISTS idx_activity_logs_table_name ON audit_schema.activity_logs(table_name);
CREATE INDEX IF NOT EXISTS idx_products_price ON ecommerce_schema.products(price);
CREATE INDEX IF NOT EXISTS idx_order_items_product ON ecommerce_schema.order_items(product_id);

-- ============================================================================
-- 8. NETTOYER LES STATISTIQUES ET OPTIMISER
-- ============================================================================

-- Réinitialiser pg_stat_statements
-- COMMENTÉ: Nécessite des privilèges spéciaux
-- SELECT pg_stat_statements_reset();

-- Exécuter VACUUM et ANALYZE sur toutes les tables
-- COMMENTÉ: L'agent DBA pourrait ne pas avoir les privilèges pour VACUUM/ANALYZE
-- VACUUM ANALYZE;

-- ============================================================================
-- 9. VÉRIFICATION FINALE ET RAPPORT
-- ============================================================================

-- Créer un rapport de nettoyage
DO $$
DECLARE
    remaining_test_objects INTEGER;
    remaining_test_users INTEGER;
    db_size_after TEXT;
    tables_count INTEGER;
    indexes_count INTEGER;
BEGIN
    -- Compter les objets de test restants
    SELECT count(*) INTO remaining_test_objects
    FROM information_schema.tables 
    WHERE table_name LIKE '%test%' OR table_name LIKE '%maintenance%';
    
    -- Compter les utilisateurs de test restants
    SELECT count(*) INTO remaining_test_users
    FROM pg_roles 
    WHERE rolname LIKE 'test_%';
    
    -- Obtenir la taille de la base après nettoyage
    SELECT pg_size_pretty(pg_database_size(current_database())) INTO db_size_after;
    
    -- Compter les tables restantes dans les schémas de test
    SELECT count(*) INTO tables_count
    FROM information_schema.tables 
    WHERE table_schema IN ('ecommerce_schema', 'analytics_schema', 'audit_schema', 'test_performance_schema', 'test_security_schema');
    
    -- Compter les index dans les schémas de test
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
-- 10. OPTIONNEL: SUPPRIMER COMPLÈTEMENT LES SCHÉMAS DE TEST
-- ============================================================================

-- Décommentez les lignes suivantes si vous voulez supprimer complètement les schémas
-- ATTENTION: Cela supprimera TOUTES les données et structures dans ces schémas !

/*
DROP SCHEMA IF EXISTS test_performance_schema CASCADE;
DROP SCHEMA IF EXISTS test_security_schema CASCADE;
-- Garder les schémas principaux mais vides pour des tests futurs
-- DROP SCHEMA IF EXISTS ecommerce_schema CASCADE;
-- DROP SCHEMA IF EXISTS analytics_schema CASCADE;
-- DROP SCHEMA IF EXISTS audit_schema CASCADE;
*/

RAISE NOTICE 'Cleanup script execution completed successfully!';
