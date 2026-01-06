import unittest
import sqlite3
from src.budget import add_budget

class TestBudget(unittest.TestCase):
   
    
    def setUp(self):
        # Cette fonction s'exécute AVANT chaque test.
        # On crée une BDD temporaire en mémoire pour isoler le test.
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        
        # On crée la table (car pour tester l'insertion, la table doit exister !)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT,
                amount REAL,
                period TEXT
            )
        ''')
        self.conn.commit()

    def tearDown(self):
        # S'exécute APRES chaque test : on ferme proprement.
        self.conn.close()

    def test_add_budget_saves_to_db(self):
        # Given : J'ai une connexion à ma base de test
        category = "Loisirs"
        amount = 50.0
        period = "2026-02"
        
        # When : J'appelle ma fonction en lui passant ma connexion de test
   
        add_budget(self.conn, category, amount, period)
        
        # Then : Je vérifie directement en SQL que la ligne existe
        self.cursor.execute("SELECT category, amount, period FROM budgets WHERE category='Loisirs'")
        result = self.cursor.fetchone()
        
        self.assertIsNotNone(result, "La transaction n'a pas été trouvée en base")
        self.assertEqual(result[0], "Loisirs")
        self.assertEqual(result[1], 50.0)
        self.assertEqual(result[2], "2026-02")

if __name__ == '__main__':
    unittest.main()

  