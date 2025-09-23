-- ============================================================================
-- PostgreSQL DBA Multi-Agent - Security Issues Creation
-- ============================================================================
-- Ce script crée intentionnellement des vulnérabilités de sécurité pour tester
-- les capacités du Security Agent
--
-- MODES D'UTILISATION:
-- 1. AGENT DBA (privilèges limités): Exécute ce script tel quel
--    - Crée des tables et vues avec des problèmes de sécurité
--    - Documente les problèmes que l'agent peut détecter
--    - Les sections nécessitant des privilèges admin sont commentées
--
-- 2. ADMINISTRATEUR (privilèges SUPERUSER): Décommente les sections admin
--    - Peut créer de vrais utilisateurs avec des privilèges problématiques
--    - Peut appliquer des permissions dangereuses
--    - Crée un environnement de test plus complet
--
-- IMPORTANT: Les sections commentées nécessitent des privilèges SUPERUSER
-- ============================================================================

-- ============================================================================
-- 1. DOCUMENTER LES PROBLÈMES D'UTILISATEURS (au lieu de les créer)
-- ============================================================================

-- Créer une table pour documenter les problèmes de sécurité des utilisateurs
CREATE TABLE IF NOT EXISTS test_security_schema.user_security_issues (
    issue_type VARCHAR(50),
    description TEXT,
    risk_level VARCHAR(10),
    current_state TEXT,
    recommendation TEXT
);

-- Documenter les types de problèmes que l'agent devrait détecter
INSERT INTO test_security_schema.user_security_issues VALUES
('superuser_privileges', 'Users with unnecessary SUPERUSER privileges', 'CRITICAL', 'Multiple non-admin users have SUPERUSER', 'Remove SUPERUSER from non-admin accounts'),
('createdb_privileges', 'Users with CREATEDB privileges who dont need them', 'HIGH', 'Service accounts have CREATEDB', 'Revoke CREATEDB from service accounts'),
('createrole_privileges', 'Users who can create other roles', 'HIGH', 'Non-admin users can create roles', 'Limit CREATEROLE to DBAs only'),
('shared_accounts', 'Shared service accounts used by multiple applications', 'HIGH', 'Single account used by multiple services', 'Create separate accounts per service'),
('no_password', 'Users without passwords', 'CRITICAL', 'Accounts exist with no authentication', 'Set passwords for all accounts'),
('weak_passwords', 'Users with weak passwords', 'HIGH', 'Passwords like 123, password, etc.', 'Enforce strong password policy');

-- ============================================================================
-- 1bis. CRÉER DES UTILISATEURS AVEC DES PRIVILÈGES EXCESSIFS (COMMENTÉ)
-- ============================================================================
-- ATTENTION: Ces commandes nécessitent des privilèges SUPERUSER
-- Décommentez et exécutez en tant qu'administrateur si vous voulez créer de vrais utilisateurs de test

-- -- Utilisateur avec des privilèges superuser (risque élevé)
-- CREATE ROLE test_superuser WITH LOGIN SUPERUSER PASSWORD 'weak_password_123';
-- COMMENT ON ROLE test_superuser IS 'Test user with excessive superuser privileges';

-- -- Utilisateur avec des privilèges de création de base de données
-- CREATE ROLE test_createdb WITH LOGIN CREATEDB PASSWORD 'another_weak_password';
-- COMMENT ON ROLE test_createdb IS 'Test user with database creation privileges';

-- -- Utilisateur avec des privilèges de création de rôles
-- CREATE ROLE test_createrole WITH LOGIN CREATEROLE PASSWORD 'password123';
-- COMMENT ON ROLE test_createrole IS 'Test user with role creation privileges';

-- -- Utilisateur de service partagé (mauvaise pratique)
-- CREATE ROLE shared_service_account WITH LOGIN PASSWORD 'shared_secret';
-- COMMENT ON ROLE shared_service_account IS 'Shared service account (security risk)';

-- -- Utilisateur sans mot de passe (risque critique)
-- CREATE ROLE test_no_password WITH LOGIN;
-- COMMENT ON ROLE test_no_password IS 'User without password - critical security risk';

-- -- Utilisateur avec mot de passe faible
-- CREATE ROLE test_weak_password WITH LOGIN PASSWORD '123';
-- COMMENT ON ROLE test_weak_password IS 'User with very weak password';

-- ============================================================================
-- 2. CRÉER DES PROBLÈMES DE PERMISSIONS (ce que l'agent peut faire)
-- ============================================================================

-- L'agent peut créer des tables avec des permissions problématiques dans les schémas de test
-- Créer une table avec des données sensibles exposées (risque de sécurité)
CREATE TABLE IF NOT EXISTS test_security_schema.exposed_user_data (
    user_id INTEGER,
    username VARCHAR(50),
    email_domain VARCHAR(100),
    last_login_ip INET,
    failed_login_count INTEGER,
    account_status VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Insérer des données simulées
INSERT INTO test_security_schema.exposed_user_data (user_id, username, email_domain, last_login_ip, failed_login_count, account_status) VALUES
(1, 'admin_user', 'company.com', '192.168.1.100', 0, 'active'),
(2, 'service_account', 'internal.local', '10.0.0.50', 5, 'locked'),
(3, 'test_user', 'external.com', '203.0.113.45', 12, 'suspicious');

-- Créer une vue qui expose trop d'informations
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
-- 2bis. PERMISSIONS EXCESSIVES (COMMENTÉ - nécessite privilèges admin)
-- ============================================================================
-- Ces commandes nécessitent des privilèges administrateur pour GRANT sur les schémas existants

-- -- Accorder ALL PRIVILEGES sur des schémas critiques
-- GRANT ALL PRIVILEGES ON SCHEMA ecommerce_schema TO test_createdb;
-- GRANT ALL PRIVILEGES ON SCHEMA analytics_schema TO test_createrole;
-- GRANT ALL PRIVILEGES ON SCHEMA audit_schema TO shared_service_account;

-- -- Permissions publiques sur des tables sensibles (très risqué)
-- GRANT SELECT ON ecommerce_schema.users TO PUBLIC;
-- GRANT SELECT ON audit_schema.login_logs TO PUBLIC;

-- ============================================================================
-- 3. CRÉER DES OBJETS DANS LE SCHÉMA PUBLIC (risque de sécurité)
-- ============================================================================

-- Table avec des données sensibles exposées  
CREATE TABLE test_security_schema.sensitive_data (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    credit_card_number VARCHAR(20), -- Données sensibles non chiffrées
    ssn VARCHAR(11),                -- Numéro de sécurité sociale
    password_backup TEXT,           -- Mots de passe en clair
    api_secret_key TEXT,            -- Clés API en clair
    created_at TIMESTAMP DEFAULT NOW()
);

-- Insérer des données sensibles factices
INSERT INTO test_security_schema.sensitive_data (user_id, credit_card_number, ssn, password_backup, api_secret_key) VALUES
(1, '4532-1234-5678-9012', '123-45-6789', 'user_password_123', 'sk_test_abc123def456'),
(2, '5678-9012-3456-7890', '987-65-4321', 'another_password', 'ak_prod_xyz789uvw012'),
(3, '9012-3456-7890-1234', '555-66-7777', 'weak_pwd', 'secret_key_qwerty123');

-- Fonction dangereuse accessible à tous
CREATE OR REPLACE FUNCTION test_security_schema.get_user_password(username TEXT)
RETURNS TEXT AS $$
BEGIN
    RETURN (SELECT password_backup FROM test_security_schema.sensitive_data WHERE user_id = (
        SELECT user_id FROM ecommerce_schema.users WHERE ecommerce_schema.users.username = $1
    ));
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- COMMENTÉ: Nécessite des privilèges pour GRANT EXECUTE
-- GRANT EXECUTE ON FUNCTION public.get_user_password(TEXT) TO PUBLIC;

-- ============================================================================
-- 4. CRÉER DES VUES AVEC DES FUITES DE DONNÉES
-- ============================================================================

-- Vue qui expose des données sensibles
CREATE VIEW test_security_schema.user_details AS
SELECT 
    u.user_id,
    u.username,
    u.email,
    u.password_hash,  -- Hash de mot de passe exposé
    u.phone,
    sd.credit_card_number,
    sd.ssn
FROM ecommerce_schema.users u
LEFT JOIN test_security_schema.sensitive_data sd ON u.user_id = sd.user_id;

-- COMMENTÉ: Nécessite des privilèges pour GRANT SELECT
-- GRANT SELECT ON public.user_details TO PUBLIC;

-- ============================================================================
-- 5. CONFIGURER DES MÉTHODES D'AUTHENTIFICATION FAIBLES
-- ============================================================================

-- Note: Ces configurations nécessitent la modification de pg_hba.conf
-- Voici ce que l'agent de sécurité devrait détecter comme problématique:

/*
Configurations problématiques à détecter dans pg_hba.conf:
- host all all 0.0.0.0/0 trust          # Trust sans authentification
- host all all 0.0.0.0/0 md5            # MD5 faible au lieu de scram-sha-256
- local all all trust                    # Connexions locales sans mot de passe
- host all postgres 0.0.0.0/0 password  # Mot de passe en clair
*/

-- Créer des entrées dans la base pour documenter les problèmes de configuration
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
-- 6. CRÉER DES RÔLES AVEC INHERITANCE PROBLÉMATIQUE
-- ============================================================================

-- COMMENTÉ: Création de rôles nécessite des privilèges administrateur
-- CREATE ROLE dangerous_parent_role WITH CREATEDB CREATEROLE;
-- CREATE ROLE child_role WITH LOGIN PASSWORD 'child_pass';

-- COMMENTÉ: Nécessite des privilèges pour GRANT des rôles
-- GRANT dangerous_parent_role TO child_role;

-- COMMENTÉ: Ces commandes nécessitent des privilèges pour créer des rôles
-- CREATE ROLE escalation_risk WITH LOGIN PASSWORD 'escalate_me';
-- GRANT test_createrole TO escalation_risk; -- Peut créer d'autres rôles

-- ============================================================================
-- 7. CRÉER DES PROBLÈMES DE ROW LEVEL SECURITY
-- ============================================================================

-- Table sensible sans Row Level Security activée
CREATE TABLE test_security_schema.multi_tenant_data (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    sensitive_info TEXT,
    financial_data DECIMAL(15,2),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Insérer des données multi-tenant
INSERT INTO test_security_schema.multi_tenant_data (tenant_id, user_id, sensitive_info, financial_data) VALUES
(1, 101, 'Tenant 1 secret data', 50000.00),
(1, 102, 'More tenant 1 data', 75000.00),
(2, 201, 'Tenant 2 confidential info', 30000.00),
(2, 202, 'Tenant 2 financial details', 120000.00),
(3, 301, 'Tenant 3 sensitive content', 95000.00);

-- COMMENTÉ: Nécessite des privilèges pour GRANT SELECT
-- GRANT SELECT ON test_security_schema.multi_tenant_data TO test_weak_password;

-- ============================================================================
-- 8. CRÉER DES FONCTIONS SECURITY DEFINER DANGEREUSES
-- ============================================================================

-- Fonction avec SECURITY DEFINER qui peut être exploitée
CREATE OR REPLACE FUNCTION test_security_schema.admin_function(query TEXT)
RETURNS TEXT AS $$
BEGIN
    -- Fonction dangereuse qui exécute du SQL dynamique
    EXECUTE query;
    RETURN 'Query executed';
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- COMMENTÉ: Nécessite des privilèges pour GRANT EXECUTE
-- GRANT EXECUTE ON FUNCTION test_security_schema.admin_function(TEXT) TO test_weak_password;

-- Autre fonction problématique
CREATE OR REPLACE FUNCTION test_security_schema.get_any_user_data(target_user_id INTEGER)
RETURNS TABLE(username TEXT, email TEXT, password_hash TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT u.username, u.email, u.password_hash
    FROM ecommerce_schema.users u
    WHERE u.user_id = target_user_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- COMMENTÉ: Nécessite des privilèges pour GRANT EXECUTE
-- GRANT EXECUTE ON FUNCTION test_security_schema.get_any_user_data(INTEGER) TO PUBLIC;

-- ============================================================================
-- 9. CRÉER DES LOGS D'AUDIT INSUFFISANTS
-- ============================================================================

-- Désactiver la journalisation pour des opérations critiques (simulé)
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
-- 10. CRÉER DES EXTENSIONS NON SÉCURISÉES
-- ============================================================================

-- Note: Ces extensions nécessitent des privilèges superuser
-- Documenter les problèmes potentiels
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
-- 11. CRÉER DES PROBLÈMES DE CHIFFREMENT
-- ============================================================================

-- Table avec des données sensibles non chiffrées
CREATE TABLE test_security_schema.unencrypted_sensitive (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER,
    credit_card_number VARCHAR(20),    -- Devrait être chiffré
    bank_account VARCHAR(20),          -- Devrait être chiffré
    social_security VARCHAR(11),       -- Devrait être chiffré
    medical_record_number VARCHAR(20), -- Devrait être chiffré
    notes TEXT                         -- Pourrait contenir des infos sensibles
);

-- Insérer des données non chiffrées
INSERT INTO test_security_schema.unencrypted_sensitive VALUES
(1, 1001, '4532123456789012', '123456789', '123-45-6789', 'MR-2023-001', 'Patient has diabetes'),
(2, 1002, '5678901234567890', '987654321', '987-65-4321', 'MR-2023-002', 'Allergy to penicillin');

-- ============================================================================
-- RÉCAPITULATIF ET VALIDATION DES PROBLÈMES DE SÉCURITÉ
-- ============================================================================

-- Créer une vue résumé pour l'agent de sécurité
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

-- Afficher un résumé des problèmes de sécurité créés
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
-- NETTOYAGE DES OBJETS DE SÉCURITÉ (COMMENTÉ POUR LES TESTS)
-- ============================================================================
-- RAPPEL: Décommenter ces lignes à la fin des tests pour nettoyer les objets
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
