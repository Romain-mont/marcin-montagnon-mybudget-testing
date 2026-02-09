import unittest
import os
import sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient

try:
    from main import app
except ImportError:
    app = None

class TestTransactionAPI(unittest.TestCase):
    
    def setUp(self):
        """Nettoyage avant chaque test"""
        # 1. Nettoyage fichier DB
        if os.path.exists("budget.db"):
            os.remove("budget.db")
        
        # 2. Initialisation Client + DB
        if app:
            self.client = TestClient(app)
            
            # On force la création des tables pour le test
           
            import sqlite3
            conn = sqlite3.connect('budget.db')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT, amount REAL, category TEXT, type TEXT, label TEXT
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS budgets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT, amount REAL, period TEXT
                )
            ''')
            conn.commit()
            conn.close()
            
        else:
            self.fail("Impossible d'importer l'application 'main'. Vérifie les chemins.")

    def tearDown(self):
        if os.path.exists("budget.db"):
            os.remove("budget.db")

    def test_create_transaction_nominal(self):
        """Cas passant : On envoie des données valides"""
        payload = {
            "date": "2026-01-20",
            "amount": 50.0,
            "category": "Alimentation",
            "type": "DEPENSE",
            "label": "Supermarché"
        }
        # Utilise self.client (créé dans setUp)
        response = self.client.post("/transactions/", json=payload)
        
      
        self.assertEqual(response.status_code, 200)

    def test_create_transaction_business_rule_error(self):
        """Cas d'erreur : On viole une règle métier (Montant négatif)"""
        payload = {
            "date": "2026-01-20",
            "amount": -10.0,  
            "category": "Alimentation",
            "type": "DEPENSE",
            "label": "Test"
        }
        response = self.client.post("/transactions/", json=payload)
        
        self.assertEqual(response.status_code, 400)
        self.assertIn("Le montant doit être positif", response.json()['detail'])

if __name__ == '__main__':
    unittest.main()