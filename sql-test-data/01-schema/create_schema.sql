-- ============================================================================
-- PostgreSQL DBA Multi-Agent Test Schema Creation
-- ============================================================================
-- Ce script crée la structure de base pour tester le système DBA multi-agent
-- ============================================================================

-- Activer les extensions nécessaires
-- CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
-- CREATE EXTENSION IF NOT EXISTS pgcrypto;
-- CREATE EXTENSION IF NOT EXISTS btree_gin;

-- Créer les schémas de test
-- CREATE SCHEMA IF NOT EXISTS ecommerce_schema;
-- CREATE SCHEMA IF NOT EXISTS analytics_schema;
-- CREATE SCHEMA IF NOT EXISTS audit_schema;
-- CREATE SCHEMA IF NOT EXISTS test_performance_schema;
-- CREATE SCHEMA IF NOT EXISTS test_security_schema;

-- ============================================================================
-- SCHEMA ECOMMERCE - Application e-commerce réaliste
-- ============================================================================

-- Table des utilisateurs
CREATE TABLE IF NOT EXISTS ecommerce_schema.users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    date_of_birth DATE,
    phone VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT TRUE,
    user_type VARCHAR(20) DEFAULT 'customer'
);

-- Table des catégories de produits
CREATE TABLE IF NOT EXISTS ecommerce_schema.categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    description TEXT,
    parent_category_id INTEGER REFERENCES ecommerce_schema.categories(category_id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table des produits
CREATE TABLE IF NOT EXISTS ecommerce_schema.products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(200) NOT NULL,
    description TEXT,
    category_id INTEGER REFERENCES ecommerce_schema.categories(category_id),
    sku VARCHAR(50) UNIQUE NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    cost DECIMAL(10,2),
    weight DECIMAL(8,3),
    dimensions JSONB,
    inventory_count INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table des commandes
CREATE TABLE IF NOT EXISTS ecommerce_schema.orders (
    order_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES ecommerce_schema.users(user_id),
    order_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    status VARCHAR(20) DEFAULT 'pending',
    total_amount DECIMAL(12,2) NOT NULL,
    shipping_cost DECIMAL(8,2) DEFAULT 0,
    tax_amount DECIMAL(10,2) DEFAULT 0,
    discount_amount DECIMAL(10,2) DEFAULT 0,
    shipping_address JSONB,
    billing_address JSONB,
    payment_method VARCHAR(50),
    payment_status VARCHAR(20) DEFAULT 'pending',
    notes TEXT
);

-- Table des articles de commande
CREATE TABLE IF NOT EXISTS ecommerce_schema.order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES ecommerce_schema.orders(order_id),
    product_id INTEGER NOT NULL REFERENCES ecommerce_schema.products(product_id),
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(12,2) NOT NULL
);

-- Table des avis clients
CREATE TABLE IF NOT EXISTS ecommerce_schema.reviews (
    review_id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES ecommerce_schema.products(product_id),
    user_id INTEGER NOT NULL REFERENCES ecommerce_schema.users(user_id),
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    title VARCHAR(200),
    review_text TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_verified BOOLEAN DEFAULT FALSE
);

-- ============================================================================
-- SCHEMA ANALYTICS - Tables d'analyse et reporting
-- ============================================================================

-- Table des sessions utilisateur
CREATE TABLE IF NOT EXISTS analytics_schema.user_sessions (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id INTEGER REFERENCES ecommerce_schema.users(user_id),
    session_start TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    session_end TIMESTAMP WITH TIME ZONE,
    ip_address INET,
    user_agent TEXT,
    page_views INTEGER DEFAULT 0,
    actions_taken INTEGER DEFAULT 0,
    conversion BOOLEAN DEFAULT FALSE
);

-- Table des événements
CREATE TABLE IF NOT EXISTS analytics_schema.events (
    event_id BIGSERIAL PRIMARY KEY,
    session_id UUID REFERENCES analytics_schema.user_sessions(session_id),
    user_id INTEGER REFERENCES ecommerce_schema.users(user_id),
    event_type VARCHAR(50) NOT NULL,
    event_data JSONB,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    page_url VARCHAR(500)
);

-- Table des métriques quotidiennes
CREATE TABLE IF NOT EXISTS analytics_schema.daily_metrics (
    metric_date DATE PRIMARY KEY,
    total_users INTEGER,
    active_users INTEGER,
    new_users INTEGER,
    total_orders INTEGER,
    total_revenue DECIMAL(15,2),
    average_order_value DECIMAL(10,2),
    conversion_rate DECIMAL(5,4),
    bounce_rate DECIMAL(5,4)
);

-- ============================================================================
-- SCHEMA AUDIT - Tables d'audit et logs
-- ============================================================================

-- Table des logs d'activité
CREATE TABLE IF NOT EXISTS audit_schema.activity_logs (
    log_id BIGSERIAL PRIMARY KEY,
    table_name VARCHAR(100),
    operation VARCHAR(10), -- INSERT, UPDATE, DELETE
    record_id BIGINT,
    old_values JSONB,
    new_values JSONB,
    user_id INTEGER,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ip_address INET
);

-- Table des logs de connexion
CREATE TABLE IF NOT EXISTS audit_schema.login_logs (
    log_id BIGSERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES ecommerce_schema.users(user_id),
    username VARCHAR(50),
    login_time TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ip_address INET,
    user_agent TEXT,
    success BOOLEAN,
    failure_reason VARCHAR(200)
);

-- ============================================================================
-- TABLES DE TEST PERFORMANCE
-- ============================================================================

-- Grande table pour tester les performances (sera remplie plus tard)
CREATE TABLE IF NOT EXISTS test_performance_schema.large_table (
    id BIGSERIAL PRIMARY KEY,
    data_column1 VARCHAR(100),
    data_column2 INTEGER,
    data_column3 DECIMAL(15,5),
    data_column4 TEXT,
    data_column5 TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_column6 JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table avec des données dupliquées (pour tester les index)
CREATE TABLE IF NOT EXISTS test_performance_schema.duplicate_data (
    id SERIAL PRIMARY KEY,
    duplicate_field VARCHAR(50), -- Beaucoup de valeurs dupliquées
    search_field VARCHAR(100),   -- Champ recherché sans index
    random_data TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================================
-- CRÉATION D'INDEX BASIQUES (certains manqueront intentionnellement)
-- ============================================================================

-- Index essentiels pour ecommerce
CREATE INDEX IF NOT EXISTS idx_users_email ON ecommerce_schema.users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON ecommerce_schema.users(username);
CREATE INDEX IF NOT EXISTS idx_products_category ON ecommerce_schema.products(category_id);
CREATE INDEX IF NOT EXISTS idx_orders_user ON ecommerce_schema.orders(user_id);
CREATE INDEX IF NOT EXISTS idx_orders_date ON ecommerce_schema.orders(order_date);
CREATE INDEX IF NOT EXISTS idx_order_items_order ON ecommerce_schema.order_items(order_id);

-- Index pour analytics (certains manqueront)
CREATE INDEX IF NOT EXISTS idx_sessions_user ON analytics_schema.user_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_events_session ON analytics_schema.events(session_id);
-- Manquera intentionnellement : index sur analytics_schema.events(timestamp)
-- Manquera intentionnellement : index sur analytics_schema.events(event_type)

-- Index pour audit
CREATE INDEX IF NOT EXISTS idx_activity_logs_timestamp ON audit_schema.activity_logs(timestamp);
-- Manquera intentionnellement : index sur audit_schema.activity_logs(table_name)

-- ============================================================================
-- CONFIGURATION INITIALE
-- ============================================================================

-- Commenter pour permettre les tests sans extension
COMMENT ON SCHEMA ecommerce_schema IS 'E-commerce application schema with realistic tables';
COMMENT ON SCHEMA analytics_schema IS 'Analytics and reporting schema';
COMMENT ON SCHEMA audit_schema IS 'Audit and logging schema';
COMMENT ON SCHEMA test_performance_schema IS 'Performance testing tables';
COMMENT ON SCHEMA test_security_schema IS 'Security testing objects';

-- Afficher un résumé de création
DO $$
BEGIN
    RAISE NOTICE '============================================================================';
    RAISE NOTICE 'PostgreSQL DBA Multi-Agent Test Schema Created Successfully!';
    RAISE NOTICE '============================================================================';
    RAISE NOTICE 'Schemas created: ecommerce_schema, analytics_schema, audit_schema, test_performance_schema, test_security_schema';
    RAISE NOTICE 'Extensions enabled: pg_stat_statements, pgcrypto, btree_gin';
    RAISE NOTICE 'Tables created: % tables total', (
        SELECT count(*) 
        FROM information_schema.tables 
        WHERE table_schema IN ('ecommerce_schema', 'analytics_schema', 'audit_schema', 'test_performance_schema', 'test_security_schema')
    );
    RAISE NOTICE '============================================================================';
    RAISE NOTICE 'Next step: Run 02-data/populate_data.sql to add test data';
    RAISE NOTICE '============================================================================';
END $$;
