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
    
    def test_transaction_with_description(self):
        """RED: Créer une transaction avec une description"""
        transaction = Transaction(
            user_id=1,
            date=date(2026, 1, 6),
            amount=Decimal('50.00'),
            category='Alimentation',
            type='DEPENSE',
            description='Courses supermarché'
        )
        
        self.assertEqual(transaction.description, 'Courses supermarché')
    
    def test_transaction_has_unique_id(self):
        """RED: Chaque transaction doit avoir un ID unique"""
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


class TestTransactionValidation(unittest.TestCase):
    """TDD: Tests pour la validation des transactions"""
    
    def test_type_must_be_revenu_or_depense(self):
        """RED: Le type doit être REVENU ou DEPENSE"""
        # Type valide DEPENSE
        trans_depense = Transaction(
            user_id=1,
            date=date.today(),
            amount=Decimal('50.00'),
            category='Test',
            type='DEPENSE'
        )
        self.assertEqual(trans_depense.type, 'DEPENSE')
        
        # Type valide REVENU
        trans_revenu = Transaction(
            user_id=1,
            date=date.today(),
            amount=Decimal('50.00'),
            category='Test',
            type='REVENU'
        )
        self.assertEqual(trans_revenu.type, 'REVENU')
    
    def test_invalid_type_raises_error(self):
        """RED: Un type invalide doit lever une ValueError"""
        with self.assertRaises(ValueError):
            Transaction(
                user_id=1,
                date=date.today(),
                amount=Decimal('50.00'),
                category='Test',
                type='INVALID'
            )
    
    def test_amount_must_be_positive(self):
        """RED: Le montant doit être positif"""
        with self.assertRaises(ValueError):
            Transaction(
                user_id=1,
                date=date.today(),
                amount=Decimal('-50.00'),
                category='Test',
                type='DEPENSE'
            )
    
    def test_amount_cannot_be_zero(self):
        """RED: Le montant ne peut pas être zéro"""
        with self.assertRaises(ValueError):
            Transaction(
                user_id=1,
                date=date.today(),
                amount=Decimal('0.00'),
                category='Test',
                type='DEPENSE'
            )


class TestTransactionRepresentation(unittest.TestCase):
    """TDD: Tests pour la représentation d'une Transaction"""
    
    def test_str_representation(self):
        """RED: Représentation string lisible d'une transaction"""
        transaction = Transaction(
            user_id=1,
            date=date(2026, 1, 6),
            amount=Decimal('50.00'),
            category='Alimentation',
            type='DEPENSE'
        )
        
        result = str(transaction)
        self.assertIn('2026-01-06', result)
        self.assertIn('DEPENSE', result)
        self.assertIn('50.00', result)
        self.assertIn('Alimentation', result)


if __name__ == '__main__':
    unittest.main()
