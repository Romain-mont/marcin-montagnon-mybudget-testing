from django.test import TestCase
from django.contrib.auth.models import User
from src.transaction import Transaction
from datetime import date
from decimal import Decimal


# =======================
# Tests du Model Transaction
# =======================

class TransactionModelTest(TestCase):
    """Tests pour le modèle Transaction"""
    
    def setUp(self):
        """Préparation des données de test"""
        self.user = User.objects.create_user(
            username='test_user',
            password='testpass123'
        )
    
    def test_create_transaction_valid(self):
        """Test RED: Créer une transaction valide avec tous les champs requis"""
        transaction = Transaction.objects.create(
            user=self.user,
            date=date(2026, 1, 6),
            amount=Decimal('150.50'),
            description='Courses supermarché',
            category='Alimentation',
            type='DEPENSE'
        )
        
        self.assertEqual(transaction.user, self.user)
        self.assertEqual(transaction.date, date(2026, 1, 6))
        self.assertEqual(transaction.amount, Decimal('150.50'))
        self.assertEqual(transaction.description, 'Courses supermarché')
        self.assertEqual(transaction.category, 'Alimentation')
        self.assertEqual(transaction.type, 'DEPENSE')
        self.assertIsNotNone(transaction.id)
    
    def test_transaction_type_choices(self):
        """Test RED: Valider que le type accepte uniquement REVENU ou DEPENSE"""
        # Type valide: DEPENSE
        transaction_depense = Transaction.objects.create(
            user=self.user,
            date=date.today(),
            amount=Decimal('50.00'),
            category='Transport',
            type='DEPENSE'
        )
        self.assertEqual(transaction_depense.type, 'DEPENSE')
        
        # Type valide: REVENU
        transaction_revenu = Transaction.objects.create(
            user=self.user,
            date=date.today(),
            amount=Decimal('2500.00'),
            category='Salaire',
            type='REVENU'
        )
        self.assertEqual(transaction_revenu.type, 'REVENU')
    
    def test_transaction_str_method(self):
        """Test RED: Vérifier la représentation string d'une transaction"""
        transaction = Transaction.objects.create(
            user=self.user,
            date=date(2026, 1, 6),
            amount=Decimal('100.00'),
            description='Test transaction',
            category='Loisirs',
            type='DEPENSE'
        )
        
        expected_str = f"{transaction.date} - DEPENSE - 100.00€ - Loisirs"
        self.assertEqual(str(transaction), expected_str)