
from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from src.budget import add_budget 

app = FastAPI()

# Modèle de données pour valider ce que l'utilisateur envoie
class BudgetModel(BaseModel):
    category: str
    amount: float
    period: str

def get_db_connection():
    # On utilise un fichier budget.db local
    conn = sqlite3.connect('budget.db')
    return conn

# Au démarrage de l'API, on s'assure que la table existe
@app.on_event("startup")
def startup():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            amount REAL,
            period TEXT
        )
    ''')
    conn.commit()
    conn.close()

# La route testée
@app.post("/budgets/")
def create_budget_route(budget: BudgetModel):
    conn = get_db_connection()
    try:
        # On appelle ta fonction logique existante
        add_budget(conn, budget.category, budget.amount, budget.period)
        return {"message": "Budget défini avec succès"}
    finally:
        conn.close()