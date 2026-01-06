import unittest
from src.budget import add_budget

class TestBudget(unittest.TestCase):
    def test_add_budget(self):
        # Given : Je veux définir un budget pour l'alimentation
        category = "alimentation"
        amount = 300.0
        period = "2026-01"
        
        # When : J'appelle la fonction (qui va retourner un dictionnaire ou un objet)
        result = add_budget(category, amount, period)
        
        # Then : Je vérifie que les données sont bien enregistrées
        self.assertEqual(result['category'], category)
        self.assertEqual(result['amount'], 300.0)
        self.assertEqual(result['period'], "2026-01")

if __name__ == '__main__':
    unittest.main()

  