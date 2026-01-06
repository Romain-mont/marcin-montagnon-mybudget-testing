import unittest
from datetime import date
from decimal import Decimal
from src.transaction import Transaction


class TestTransactionCreation(unittest.TestCase):
    """TDD: Tests pour la création d'une Transaction"""
    
    def test_create_simple_transaction(self):
        """RED: Créer une transaction simple avec les données minimales"""
        transaction = Transaction(
            user_id=1,
            date=date(2026, 1, 6),
            amount=Decimal('50.00'),
            category='Alimentation',
            type='DEPENSE'
        )
        
        self.assertEqual(transaction.user_id, 1)
        self.assertEqual(transaction.date, date(2026, 1, 6))
        self.assertEqual(transaction.amount, Decimal('50.00'))
        self.assertEqual(transaction.category, 'Alimentation')
        self.assertEqual(transaction.type, 'DEPENSE')


if __name__ == '__main__':
    unittest.main()
