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
        Transaction._id_counter += 1
        self.id = Transaction._id_counter
        self.user_id = user_id
        self.date = date
        self.amount = amount
        self.category = category
        self.type = type
        self.description = description

