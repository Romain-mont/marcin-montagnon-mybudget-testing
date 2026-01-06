-- Création de la base de données SQLite pour l'application Budget Personnel

-- Table des utilisateurs
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

-- Table des transactions
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    date DATE NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    description VARCHAR(255),
    category VARCHAR(100) NOT NULL,
    type VARCHAR(10) NOT NULL CHECK (type IN ('REVENU', 'DEPENSE')),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Table des budgets
CREATE TABLE IF NOT EXISTS budgets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    category VARCHAR(100) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    period VARCHAR(7) NOT NULL,  -- Format: "YYYY-MM" (ex: "2026-01")
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- -- Index pour optimiser les requêtes
-- CREATE INDEX IF NOT EXISTS idx_transactions_user ON transactions(user_id);
-- CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(date);
-- CREATE INDEX IF NOT EXISTS idx_transactions_category ON transactions(category);
-- CREATE INDEX IF NOT EXISTS idx_budgets_user ON budgets(user_id);
-- CREATE INDEX IF NOT EXISTS idx_budgets_period ON budgets(period);


-- Utilisateurs (mot de passe = "password123" hashé avec bcrypt)
INSERT INTO users (username, password_hash) VALUES 
('jean_dupont', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LeU8eLakmSTK8Vtx.'),
('marie_martin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LeU8eLakmSTK8Vtx.');

-- Transactions pour jean_dupont (user_id = 1)
INSERT INTO transactions (user_id, date, amount, description, category, type) VALUES 
-- Revenus
(1, '2026-01-01', 2500.00, 'Salaire janvier', 'Salaire', 'REVENU'),
(1, '2026-01-15', 150.00, 'Vente Leboncoin', 'Ventes', 'REVENU'),
-- Dépenses
(1, '2026-01-02', 85.50, 'Courses Leclerc', 'Alimentation', 'DEPENSE'),
(1, '2026-01-05', 45.00, 'Essence voiture', 'Transport', 'DEPENSE'),
(1, '2026-01-08', 120.00, 'Facture électricité', 'Logement', 'DEPENSE'),
(1, '2026-01-10', 35.90, 'Restaurant avec amis', 'Loisirs', 'DEPENSE'),
(1, '2026-01-12', 62.30, 'Courses Carrefour', 'Alimentation', 'DEPENSE'),
(1, '2026-01-18', 29.99, 'Abonnement Netflix', 'Loisirs', 'DEPENSE'),
(1, '2026-01-20', 800.00, 'Loyer janvier', 'Logement', 'DEPENSE'),
(1, '2026-01-25', 55.00, 'Plein essence', 'Transport', 'DEPENSE');

-- Transactions pour marie_martin (user_id = 2)
INSERT INTO transactions (user_id, date, amount, description, category, type) VALUES 
-- Revenus
(2, '2026-01-01', 3200.00, 'Salaire janvier', 'Salaire', 'REVENU'),
(2, '2026-01-20', 200.00, 'Freelance design', 'Freelance', 'REVENU'),
-- Dépenses
(2, '2026-01-03', 95.00, 'Courses bio', 'Alimentation', 'DEPENSE'),
(2, '2026-01-07', 75.00, 'Pass Navigo', 'Transport', 'DEPENSE'),
(2, '2026-01-10', 950.00, 'Loyer janvier', 'Logement', 'DEPENSE'),
(2, '2026-01-14', 45.00, 'Cinéma + restaurant', 'Loisirs', 'DEPENSE'),
(2, '2026-01-22', 78.50, 'Courses marché', 'Alimentation', 'DEPENSE');

-- Budgets pour jean_dupont (user_id = 1)
INSERT INTO budgets (user_id, category, amount, period) VALUES 
(1, 'Alimentation', 300.00, '2026-01'),
(1, 'Transport', 150.00, '2026-01'),
(1, 'Logement', 900.00, '2026-01'),
(1, 'Loisirs', 100.00, '2026-01');

-- Budgets pour marie_martin (user_id = 2)
INSERT INTO budgets (user_id, category, amount, period) VALUES 
(2, 'Alimentation', 250.00, '2026-01'),
(2, 'Transport', 80.00, '2026-01'),
(2, 'Logement', 1000.00, '2026-01'),
(2, 'Loisirs', 150.00, '2026-01');