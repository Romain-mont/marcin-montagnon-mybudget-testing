import unittest
import sqlite3
import os
from fastapi.testclient import TestClient

try:
    from main import app
except ImportError:
    app = None

class TestBudgetAPI(unittest.TestCase):
    
    def setUp(self):
        
        if os.path.exists('budget.db'):
            os.remove('budget.db')

        if app:
            self.client = TestClient(app)
            
            # --- MISE EN PLACE DE LA BDD POUR LES TESTS ---
            conn = sqlite3.connect('budget.db') 
            
            
            
            # 1. On s'assure que la table BUDGETS existe
            conn.execute('''
                CREATE TABLE IF NOT EXISTS budgets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT,
                    amount REAL,
                    period TEXT
                )
            ''')
            
            # 2. On s'assure que la table TRANSACTIONS existe )
            conn.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    amount REAL,
                    category TEXT,
                    type TEXT,
                    label TEXT
                )
            ''')
            
            conn.commit()
            conn.close()
        else:
            self.fail("App non trouvée")
  
    def tearDown(self):
        
        if os.path.exists('budget.db'):
            os.remove('budget.db')

    def test_create_budget_api(self):
        # Test 1 : Création 
        payload = { "category": "Loisirs", "amount": 200.0, "period": "2026-03" }
        response = self.client.post("/budgets/", json=payload)
        self.assertEqual(response.status_code, 200)

    def test_get_budget_status_api(self):
        # Test 2 : Consultation 
        
        # GIVEN : On injecte des données directement en base
        conn = sqlite3.connect('budget.db')
        # Budget : 100€
        conn.execute("INSERT INTO budgets (category, amount, period) VALUES ('Resto', 100.0, '2026-05')")
        # Dépense : 20€
        conn.execute("INSERT INTO transactions (amount, category, type) VALUES (20.0, 'Resto', 'DEPENSE')")
        conn.commit()
        conn.close()

        # WHEN : On appelle la route GET
        response = self.client.get("/budgets/Resto/2026-05")
        
        # THEN : On s'attend à un succès
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(data["budget_amount"], 100.0)
        self.assertEqual(data["remaining"], 80.0)
        self.assertIsNone(data["alert"]) 

if __name__ == '__main__':
    unittest.main()