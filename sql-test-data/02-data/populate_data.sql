-- ============================================================================
-- PostgreSQL DBA Multi-Agent Test Data Population
-- ============================================================================
-- Ce script remplit la base avec des données réalistes pour tester les agents
-- ============================================================================

-- Reset pg_stat_statements pour des statistiques fraîches
-- COMMENTÉ: Nécessite des privilèges spéciaux que l'agent DBA pourrait ne pas avoir
-- SELECT pg_stat_statements_reset();

-- ============================================================================
-- DONNÉES ECOMMERCE - Application e-commerce réaliste
-- ============================================================================

-- Insérer des catégories (éviter les doublons)
INSERT INTO ecommerce_schema.categories (category_name, description, parent_category_id) 
SELECT * FROM (VALUES
('Electronics', 'Electronic devices and gadgets', NULL),
('Computers', 'Computers and computer accessories', 1),
('Smartphones', 'Mobile phones and accessories', 1),
('Home & Garden', 'Home improvement and garden supplies', NULL),
('Furniture', 'Home and office furniture', 4),
('Clothing', 'Apparel and fashion', NULL),
('Men''s Clothing', 'Clothing for men', 6),
('Women''s Clothing', 'Clothing for women', 6),
('Books', 'Books and educational materials', NULL),
('Sports', 'Sports and outdoor equipment', NULL)
) AS new_categories(category_name, description, parent_category_id)
WHERE NOT EXISTS (
    SELECT 1 FROM ecommerce_schema.categories 
    WHERE categories.category_name = new_categories.category_name
);

-- Insérer des utilisateurs (mixture de types) - éviter les doublons
-- Utilisation de MD5 simple au lieu de pgcrypto pour éviter les dépendances d'extension
INSERT INTO ecommerce_schema.users (username, email, password_hash, first_name, last_name, date_of_birth, phone, user_type) 
SELECT * FROM (VALUES
('admin_user', 'admin@example.com', md5('admin123'), 'Admin', 'User', DATE '1980-01-01', '+1234567890', 'admin'),
('john_doe', 'john.doe@email.com', md5('password123'), 'John', 'Doe', DATE '1985-05-15', '+1234567891', 'customer'),
('jane_smith', 'jane.smith@email.com', md5('password456'), 'Jane', 'Smith', DATE '1990-08-20', '+1234567892', 'customer'),
('bob_wilson', 'bob.wilson@email.com', md5('password789'), 'Bob', 'Wilson', DATE '1978-12-03', '+1234567893', 'customer'),
('alice_brown', 'alice.brown@email.com', md5('password321'), 'Alice', 'Brown', DATE '1992-03-10', '+1234567894', 'customer'),
('charlie_davis', 'charlie.davis@email.com', md5('password654'), 'Charlie', 'Davis', DATE '1988-07-25', '+1234567895', 'customer'),
('emma_jones', 'emma.jones@email.com', md5('password987'), 'Emma', 'Jones', DATE '1995-11-18', '+1234567896', 'customer'),
('david_miller', 'david.miller@email.com', md5('password147'), 'David', 'Miller', DATE '1983-04-12', '+1234567897', 'customer'),
('sarah_garcia', 'sarah.garcia@email.com', md5('password258'), 'Sarah', 'Garcia', DATE '1987-09-30', '+1234567898', 'customer'),
('mike_rodriguez', 'mike.rodriguez@email.com', md5('password369'), 'Mike', 'Rodriguez', DATE '1991-01-22', '+1234567899', 'customer')
) AS new_users(username, email, password_hash, first_name, last_name, date_of_birth, phone, user_type)
WHERE NOT EXISTS (
    SELECT 1 FROM ecommerce_schema.users 
    WHERE users.username = new_users.username
);

-- Insérer des produits - éviter les doublons
INSERT INTO ecommerce_schema.products (product_name, description, category_id, sku, price, cost, weight, inventory_count) 
SELECT * FROM (VALUES
('Laptop Pro 15"', 'High-performance laptop for professionals', 2, 'LAPTOP-PRO-15', 1299.99, 899.99, 2.1, 50),
('Smartphone X', 'Latest smartphone with advanced features', 3, 'PHONE-X-128', 899.99, 599.99, 0.18, 100),
('Wireless Headphones', 'Premium noise-canceling headphones', 1, 'HEADPHONES-WL', 199.99, 119.99, 0.25, 75),
('Gaming Chair', 'Ergonomic gaming chair with RGB lighting', 5, 'CHAIR-GAMING-RGB', 349.99, 199.99, 18.5, 25),
('Men''s T-Shirt', 'Cotton T-shirt in various colors', 7, 'TSHIRT-MEN-001', 19.99, 8.99, 0.2, 200),
('Women''s Jeans', 'Slim fit jeans for women', 8, 'JEANS-WOMEN-001', 59.99, 29.99, 0.8, 150),
('Programming Book', 'Complete guide to PostgreSQL', 9, 'BOOK-POSTGRES-001', 49.99, 24.99, 0.5, 80),
('Tennis Racket', 'Professional tennis racket', 10, 'TENNIS-RACKET-001', 129.99, 69.99, 0.32, 40),
('Office Desk', 'Modern office desk with storage', 5, 'DESK-OFFICE-001', 299.99, 179.99, 25.0, 15),
('Smartphone Case', 'Protective case for Smartphone X', 3, 'CASE-PHONE-X', 24.99, 8.99, 0.05, 300)
) AS new_products(product_name, description, category_id, sku, price, cost, weight, inventory_count)
WHERE NOT EXISTS (
    SELECT 1 FROM ecommerce_schema.products 
    WHERE products.sku = new_products.sku
);

-- Générer plus de produits pour avoir des données substantielles - éviter les doublons
INSERT INTO ecommerce_schema.products (product_name, description, category_id, sku, price, cost, weight, inventory_count)
SELECT 
    'Product ' || i,
    'Description for product ' || i,
    ((i % 10) + 1),
    'SKU-' || LPAD(i::text, 6, '0'),
    (RANDOM() * 500 + 10)::DECIMAL(10,2),
    (RANDOM() * 200 + 5)::DECIMAL(10,2),
    (RANDOM() * 5 + 0.1)::DECIMAL(8,3),
    (RANDOM() * 100 + 1)::INTEGER
FROM generate_series(11, 1000) i
WHERE NOT EXISTS (
    SELECT 1 FROM ecommerce_schema.products 
    WHERE products.sku = 'SKU-' || LPAD(i::text, 6, '0')
);

-- Insérer des commandes réalistes (étalées sur plusieurs mois)
DO $$
DECLARE
    current_order_date TIMESTAMP := NOW() - INTERVAL '6 months';
    end_date TIMESTAMP := NOW();
    order_count INTEGER := 0;
    current_order_id INTEGER;
    selected_user_id INTEGER;
    product_count INTEGER;
    selected_product_id INTEGER;
    product_price DECIMAL(10,2);
    order_total DECIMAL(12,2);
BEGIN
    -- Vérifier qu'il y a des utilisateurs clients
    IF NOT EXISTS (SELECT 1 FROM ecommerce_schema.users WHERE user_type = 'customer') THEN
        RAISE NOTICE 'Aucun utilisateur client trouvé. Arrêt de la création de commandes.';
        RETURN;
    END IF;
    
    WHILE current_order_date <= end_date LOOP
        -- Créer 0-5 commandes par jour
        FOR day_orders IN 0..(RANDOM() * 5)::INTEGER LOOP
            order_count := order_count + 1;
            -- Sélectionner un utilisateur aléatoire directement depuis la table
            SELECT user_id INTO selected_user_id 
            FROM ecommerce_schema.users 
            WHERE user_type = 'customer' 
            ORDER BY RANDOM() 
            LIMIT 1;
            
            -- Vérifier qu'on a bien un utilisateur
            IF selected_user_id IS NULL THEN
                CONTINUE; -- Passer à la prochaine itération
            END IF;
            
            -- Insérer la commande
            INSERT INTO ecommerce_schema.orders (user_id, order_date, status, total_amount, shipping_cost, tax_amount, payment_method, payment_status)
            VALUES (
                selected_user_id,
                current_order_date + (RANDOM() * INTERVAL '24 hours'),
                CASE (RANDOM() * 4)::INTEGER 
                    WHEN 0 THEN 'pending'
                    WHEN 1 THEN 'processing'
                    WHEN 2 THEN 'shipped'
                    ELSE 'delivered'
                END,
                0, -- sera mis à jour après insertion des items
                9.99,
                0, -- sera calculé
                CASE (RANDOM() * 3)::INTEGER
                    WHEN 0 THEN 'credit_card'
                    WHEN 1 THEN 'debit_card'
                    ELSE 'paypal'
                END,
                CASE WHEN RANDOM() > 0.1 THEN 'completed' ELSE 'pending' END
            ) RETURNING order_id INTO current_order_id;
            
            order_total := 0;
            
            -- Ajouter 1-5 produits à la commande
            product_count := 1 + (RANDOM() * 4)::INTEGER;
            FOR product_num IN 1..product_count LOOP
                -- Sélectionner un produit existant au hasard
                SELECT product_id, price INTO selected_product_id, product_price 
                FROM ecommerce_schema.products 
                ORDER BY RANDOM() 
                LIMIT 1;
                
                IF product_price IS NOT NULL THEN
                    INSERT INTO ecommerce_schema.order_items (order_id, product_id, quantity, unit_price, total_price)
                    VALUES (
                        current_order_id,
                        selected_product_id,
                        1 + (RANDOM() * 3)::INTEGER,
                        product_price,
                        product_price * (1 + (RANDOM() * 3)::INTEGER)
                    );
                    
                    order_total := order_total + (product_price * (1 + (RANDOM() * 3)::INTEGER));
                END IF;
            END LOOP;
            
            -- Mettre à jour le total de la commande
            UPDATE ecommerce_schema.orders 
            SET total_amount = order_total + shipping_cost,
                tax_amount = order_total * 0.08
            WHERE order_id = current_order_id;
            
        END LOOP;
        
        current_order_date := current_order_date + INTERVAL '1 day';
    END LOOP;
    
    RAISE NOTICE 'Inserted % orders with items', order_count;
END $$;

-- Insérer des avis produits - éviter les doublons
INSERT INTO ecommerce_schema.reviews (product_id, user_id, rating, title, review_text, is_verified)
SELECT 
    p.product_id,
    u.user_id,
    (1 + (RANDOM() * 4)::INTEGER), -- Rating de 1 à 5
    'Review title ' || i,
    'This is a review text for product. ' || 
    CASE WHEN RANDOM() > 0.5 THEN 'I really like this product!' ELSE 'Could be better.' END,
    RANDOM() > 0.3
FROM generate_series(1, 500) i,
     (SELECT product_id FROM ecommerce_schema.products ORDER BY RANDOM() LIMIT 1) p,
     (SELECT user_id FROM ecommerce_schema.users WHERE user_type = 'customer' ORDER BY RANDOM() LIMIT 1) u
WHERE NOT EXISTS (
    SELECT 1 FROM ecommerce_schema.reviews 
    WHERE reviews.product_id = p.product_id AND reviews.user_id = u.user_id
)
LIMIT 500;

-- ============================================================================
-- DONNÉES ANALYTICS
-- ============================================================================

-- Insérer des sessions utilisateur
INSERT INTO analytics_schema.user_sessions (user_id, session_start, session_end, ip_address, page_views, actions_taken, conversion)
SELECT 
    (CASE WHEN RANDOM() > 0.3 THEN 2 + (RANDOM() * 8)::INTEGER ELSE NULL END), -- Certaines sessions anonymes
    NOW() - (RANDOM() * INTERVAL '30 days'),
    NOW() - (RANDOM() * INTERVAL '30 days') + (RANDOM() * INTERVAL '2 hours'),
    ('192.168.' || (1 + RANDOM() * 254)::INTEGER || '.' || (1 + RANDOM() * 254)::INTEGER)::INET,
    (1 + RANDOM() * 20)::INTEGER,
    (0 + RANDOM() * 10)::INTEGER,
    RANDOM() > 0.85
FROM generate_series(1, 2000);

-- Insérer des événements
INSERT INTO analytics_schema.events (session_id, user_id, event_type, event_data, timestamp)
SELECT 
    s.session_id,
    s.user_id,
    CASE (RANDOM() * 5)::INTEGER
        WHEN 0 THEN 'page_view'
        WHEN 1 THEN 'click'
        WHEN 2 THEN 'add_to_cart'
        WHEN 3 THEN 'purchase'
        ELSE 'search'
    END,
    ('{"page": "/product/' || (1 + RANDOM() * 1000)::INTEGER || '"}')::JSONB,
    s.session_start + (RANDOM() * (s.session_end - s.session_start))
FROM analytics_schema.user_sessions s,
     generate_series(1, 3); -- 3 événements par session en moyenne

-- ============================================================================
-- DONNÉES D'AUDIT
-- ============================================================================

-- Insérer des logs de connexion (certains échecs)
INSERT INTO audit_schema.login_logs (user_id, username, login_time, ip_address, success, failure_reason)
SELECT 
    CASE WHEN RANDOM() > 0.1 THEN (2 + (RANDOM() * 8)::INTEGER) ELSE NULL END,
    CASE WHEN RANDOM() > 0.1 THEN u.username ELSE 'invalid_user_' || i END,
    NOW() - (RANDOM() * INTERVAL '30 days'),
    ('10.0.' || (1 + RANDOM() * 254)::INTEGER || '.' || (1 + RANDOM() * 254)::INTEGER)::INET,
    RANDOM() > 0.15, -- 15% d'échecs
    CASE WHEN RANDOM() > 0.15 THEN NULL ELSE 
        CASE (RANDOM() * 3)::INTEGER
            WHEN 0 THEN 'invalid_password'
            WHEN 1 THEN 'account_locked'
            ELSE 'user_not_found'
        END
    END
FROM generate_series(1, 1000) i
LEFT JOIN ecommerce_schema.users u ON u.user_id = (2 + (RANDOM() * 8)::INTEGER);

-- ============================================================================
-- DONNÉES DE TEST PERFORMANCE
-- ============================================================================

-- Remplir la grande table (cela prendra du temps - commencer petit)
INSERT INTO test_performance_schema.large_table (data_column1, data_column2, data_column3, data_column4, data_column6)
SELECT 
    'Data ' || i,
    (RANDOM() * 1000000)::INTEGER,
    (RANDOM() * 999999.99999)::DECIMAL(15,5),
    'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
    ('{"key": "value", "number": ' || i || ', "random": ' || RANDOM() || '}')::JSONB
FROM generate_series(1, 100000) i; -- Commencer avec 100k lignes

-- Remplir la table avec des données dupliquées (pour test d'index)
INSERT INTO test_performance_schema.duplicate_data (duplicate_field, search_field, random_data)
SELECT 
    'duplicate_value_' || ((i % 100) + 1), -- Beaucoup de doublons
    'search_me_' || i,
    'Random data ' || i || ' with some text to make it larger'
FROM generate_series(1, 50000) i;

-- ============================================================================
-- MISE À JOUR DES STATISTIQUES ET AFFICHAGE DU RÉSUMÉ
-- ============================================================================

-- Analyser toutes les tables pour des statistiques fraîches
-- COMMENTÉ: L'agent DBA pourrait ne pas avoir les privilèges pour ANALYZE sur tous les schémas
-- ANALYZE;

-- Afficher un résumé
DO $$
DECLARE
    total_users INTEGER;
    total_products INTEGER;
    total_orders INTEGER;
    total_events INTEGER;
    db_size TEXT;
BEGIN
    SELECT count(*) INTO total_users FROM ecommerce_schema.users;
    SELECT count(*) INTO total_products FROM ecommerce_schema.products;
    SELECT count(*) INTO total_orders FROM ecommerce_schema.orders;
    SELECT count(*) INTO total_events FROM analytics_schema.events;
    SELECT pg_size_pretty(pg_database_size(current_database())) INTO db_size;
    
    RAISE NOTICE '============================================================================';
    RAISE NOTICE 'PostgreSQL DBA Multi-Agent Test Data Population Complete!';
    RAISE NOTICE '============================================================================';
    RAISE NOTICE 'Database size: %', db_size;
    RAISE NOTICE 'Users: %', total_users;
    RAISE NOTICE 'Products: %', total_products;
    RAISE NOTICE 'Orders: %', total_orders;
    RAISE NOTICE 'Analytics events: %', total_events;
    RAISE NOTICE 'Performance test records: 150,000+';
    RAISE NOTICE '============================================================================';
    RAISE NOTICE 'Next step: Run 03-performance-issues/create_performance_issues.sql';
    RAISE NOTICE '============================================================================';
END $$;
