import unittest
from datetime import date
from decimal import Decimal
from src.transaction import Transaction


class TestTransactionCreation(unittest.TestCase):
    """Tests pour la création d'une Transaction"""
    
    def test_create_simple_transaction(self):
        """Créer une transaction simple avec les données minimales"""
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
    
    def test_transaction_has_unique_id(self):
        """Chaque transaction doit avoir un ID unique"""
        trans1 = Transaction(
            user_id=1,
            date=date.today(),
            amount=Decimal('50.00'),
            category='Test',
            type='DEPENSE'
        )
        
        trans2 = Transaction(
            user_id=1,
            date=date.today(),
            amount=Decimal('50.00'),
            category='Test',
            type='DEPENSE'
        )
        
        self.assertIsNotNone(trans1.id)
        self.assertIsNotNone(trans2.id)
        self.assertNotEqual(trans1.id, trans2.id)
    
    def test_transaction_with_description(self):
        """Créer une transaction avec une description optionnelle"""
        transaction = Transaction(
            user_id=1,
            date=date(2026, 1, 6),
            amount=Decimal('50.00'),
            category='Alimentation',
            type='DEPENSE',
            description='Courses supermarché'
        )
        
        self.assertEqual(transaction.description, 'Courses supermarché')
    
    def test_invalid_type_raises_error(self):
        """Un type invalide doit lever une ValueError"""
        with self.assertRaises(ValueError):
            Transaction(
                user_id=1,
                date=date.today(),
                amount=Decimal('50.00'),
                category='Test',
                type='INVALID'
            )
    
    def test_amount_must_be_positive(self):
        """Le montant doit être positif"""
        with self.assertRaises(ValueError):
            Transaction(
                user_id=1,
                date=date.today(),
                amount=Decimal('-50.00'),
                category='Test',
                type='DEPENSE'
            )
    
    def test_amount_cannot_be_zero(self):
        """Le montant ne peut pas être zéro"""
        with self.assertRaises(ValueError):
            Transaction(
                user_id=1,
                date=date.today(),
                amount=Decimal('0.00'),
                category='Test',
                type='DEPENSE'
            )


if __name__ == '__main__':
    unittest.main()
