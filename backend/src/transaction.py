from datetime import date
from decimal import Decimal
from typing import Optional


class Transaction:
    """Modèle pour représenter une transaction financière"""
    
    def __init__(
        self,
        user_id: int,
        date: date,
        amount: Decimal,
        category: str,
        type: str,
        description: Optional[str] = None
    ):
        self.user_id = user_id
        self.date = date
        self.amount = amount
        self.category = category
        self.type = type
        self.description = description

