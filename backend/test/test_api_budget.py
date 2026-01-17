import unittest
from fastapi.testclient import TestClient

try:
    from main import app
except ImportError:
    app = None

class TestBudgetAPI(unittest.TestCase):
    
    def setUp(self):
        # On initialise le client de test uniquement si l'app existe
        if app:
            self.client = TestClient(app)
        else:
            self.fail("Le fichier main.py ou l'application FastAPI n'est pas encore créée")

    def test_create_budget_api(self):
        # Given : Un budget à définir
        payload = {
            "category": "Loisirs",
            "amount": 200.0,
            "period": "2026-03"
        }
        
       
        response = self.client.post("/budgets/", json=payload)
        
        # Then : Ça doit marcher (200 OK)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Budget défini avec succès"})

if __name__ == '__main__':
    unittest.main()