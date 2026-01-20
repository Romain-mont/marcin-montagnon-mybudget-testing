from datetime import date
from decimal import Decimal
from typing import Optional


class Transaction:
    """Modèle pour représenter une transaction financière"""
    
    _id_counter = 0
    
    def __init__(
        self,
        user_id: int,
        date: date,
        amount: Decimal,
        category: str,
        type: str,
        description: Optional[str] = None
    ):
        if type not in ['REVENU', 'DEPENSE']:
            raise ValueError(f"Le type doit être 'REVENU' ou 'DEPENSE', reçu: {type}")
        
        if amount <= 0:
            raise ValueError(f"Le montant doit être positif, reçu: {amount}")
        
        Transaction._id_counter += 1
        self.id = Transaction._id_counter
        self.user_id = user_id
        self.date = date
        self.amount = amount
        self.category = category
        self.type = type
        self.description = description
    
    def __str__(self) -> str:
        """Représentation lisible d'une transaction"""
        return f"{self.date} - {self.type} - {self.amount} - {self.category}"
    
    def __eq__(self, other) -> bool:
        """Deux transactions sont égales si elles ont le même ID"""
        if not isinstance(other, Transaction):
            return False
        return self.id == other.id

