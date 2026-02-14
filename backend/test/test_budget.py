import unittest
import sqlite3
from src.budget import add_budget, calculate_remaining_budget, calculate_budget_percentage, check_budget_alert, delete_budget

class TestBudget(unittest.TestCase):
    
    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        
        # 1. On crée la table BUDGETS
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT,
                amount REAL,
                period TEXT
            )
        ''')

        # 2. On crée la table TRANSACTIONS (Simulée pour ton test)
     
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                amount REAL,
                category TEXT,
                type TEXT
            )
        ''')
        self.conn.commit()

    def tearDown(self):
        self.conn.close()

    def test_add_budget_saves_to_db(self):
        # Test précédent (toujours valide)
        add_budget(self.conn, "Loisirs", 50.0, "2026-02")
        self.cursor.execute("SELECT amount FROM budgets WHERE category='Loisirs'")
        result = self.cursor.fetchone()
        self.assertEqual(result[0], 50.0)

    def test_calculate_remaining_budget(self):
        # Given : Un budget de 500€
        add_budget(self.conn, "Alimentation", 500.0, "2026-01")
        
        # And : Des dépenses existantes dans cette catégorie (Total = 150€)

        self.cursor.execute("INSERT INTO transactions (amount, category, type) VALUES (100.0, 'Alimentation', 'DEPENSE')")
        self.cursor.execute("INSERT INTO transactions (amount, category, type) VALUES (50.0, 'Alimentation', 'DEPENSE')")
        self.conn.commit()

        # When : Je calcule le reste
        remaining = calculate_remaining_budget(self.conn, "Alimentation", "2026-01")

        # Then : Il doit rester 350€ (500 - 150)
        self.assertEqual(remaining, 350.0)
    def test_calculate_percentage(self):
        # Cas 1 : Normal (50% consommé)
        
        # Pour ce test, on repart de zéro pour être propre.
        
        # Nettoyage des tables pour ce test spécifique
        self.cursor.execute("DELETE FROM budgets")
        self.cursor.execute("DELETE FROM transactions")
        
        add_budget(self.conn, "Loisirs", 200.0, "2026-03")
        self.cursor.execute("INSERT INTO transactions (amount, category, type) VALUES (100.0, 'Loisirs', 'DEPENSE')")
        self.conn.commit()
        
        percent = calculate_budget_percentage(self.conn, "Loisirs", "2026-03")
        self.assertEqual(percent, 50.0)

    def test_calculate_percentage_division_zero(self):
        # Cas 2 : Budget à 0 (pour éviter le crash)
        add_budget(self.conn, "Vide", 0.0, "2026-03")
        percent = calculate_budget_percentage(self.conn, "Vide", "2026-03")
        self.assertEqual(percent, 0.0) 
    
    def test_check_budget_alert_threshold(self):
        # Given : Budget 100€, Dépenses actuelles 75€
        self.cursor.execute("DELETE FROM budgets")
        self.cursor.execute("DELETE FROM transactions")
        
        add_budget(self.conn, "Resto", 100.0, "2026-05")
        # On insère 75€ de dépenses
        self.cursor.execute("INSERT INTO transactions (amount, category, type) VALUES (75.0, 'Resto', 'DEPENSE')")
        self.conn.commit()
        
        # When : On vérifie l'alerte APRES avoir ajouté 10€ virtuellement (ou si on teste l'état actuel)
        
        self.cursor.execute("INSERT INTO transactions (amount, category, type) VALUES (10.0, 'Resto', 'DEPENSE')")
        self.conn.commit()
        
        message = check_budget_alert(self.conn, "Resto", "2026-05")
        
        # Then
        self.assertEqual(message, "Attention : vous avez consommé 85.0% de votre budget Resto")

    def test_check_budget_no_alert(self):
        # Given : Budget 100€, Dépenses 10€
        add_budget(self.conn, "Resto", 100.0, "2026-06")
        self.cursor.execute("INSERT INTO transactions (amount, category, type) VALUES (10.0, 'Resto', 'DEPENSE')")
        self.conn.commit()
        
        message = check_budget_alert(self.conn, "Resto", "2026-06")
        
        # Then : Pas de message
        self.assertIsNone(message)

    def test_delete_budget(self):
        # Given : un budget existant
        add_budget(self.conn, "Loisirs", 50.0, "2026-02")

        # When : suppression
        deleted = delete_budget(self.conn, "Loisirs", "2026-02")

        # Then : supprimé
        self.assertTrue(deleted)
        self.cursor.execute("SELECT COUNT(*) FROM budgets WHERE category='Loisirs' AND period='2026-02'")
        result = self.cursor.fetchone()
        self.assertEqual(result[0], 0)

if __name__ == '__main__':
    unittest.main()