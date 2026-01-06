from datetime import date
from decimal import Decimal
from typing import Optional
import uuid


class Transaction:
    """Modèle pour représenter une transaction financière"""
    
    VALID_TYPES = ['REVENU', 'DEPENSE']
    
    def __init__(
        self,
        user_id: int,
        date: date,
        amount: Decimal,
        category: str,
        type: str,
        description: Optional[str] = None
    ):
        """
        Initialiser une transaction avec validation.
        
        Args:
            user_id: ID de l'utilisateur
            date: Date de la transaction
            amount: Montant de la transaction
            category: Catégorie de la transaction
            type: Type de la transaction (REVENU ou DEPENSE)
            description: Description optionnelle
            
        Raises:
            ValueError: Si le type est invalide ou le montant n'est pas positif
        """
        # Validation du type
        if type not in self.VALID_TYPES:
            raise ValueError(f"Le type doit être 'REVENU' ou 'DEPENSE', reçu: {type}")
        
        # Validation du montant
        if amount <= 0:
            raise ValueError(f"Le montant doit être positif, reçu: {amount}")
        
        # Assignation des attributs
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.date = date
        self.amount = amount
        self.category = category
        self.type = type
        self.description = description
    
    def __str__(self) -> str:
        """Représentation lisible d'une transaction"""
        return f"{self.date} - {self.type} - {self.amount}€ - {self.category}"
    
    def __repr__(self) -> str:
        """Représentation pour le debug"""
        return f"Transaction(id={self.id}, user_id={self.user_id}, date={self.date}, type={self.type}, amount={self.amount})"
