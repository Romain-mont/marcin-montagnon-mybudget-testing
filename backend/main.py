
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from src.budget import add_budget, calculate_remaining_budget, calculate_budget_percentage, check_budget_alert

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
    conn.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            amount REAL,
            category TEXT,
            type TEXT,
            label TEXT
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

# Route GET (Consultation)

@app.get("/budgets/{category}/{period}")
def get_budget_status_route(category: str, period: str):
    conn = get_db_connection()
    try:
        # 1. On vérifie si le budget existe
        cursor = conn.cursor()
        cursor.execute("SELECT amount FROM budgets WHERE category=? AND period=?", (category, period))
        row = cursor.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail="Budget introuvable")
        
        budget_total = row[0]
        
        # 2. On utilise tes fonctions pour les calculs
        remaining = calculate_remaining_budget(conn, category, period)
        percent = calculate_budget_percentage(conn, category, period)
        alert = check_budget_alert(conn, category, period)
        
        return {
            "category": category,
            "period": period,
            "budget_amount": budget_total,
            "remaining": remaining,
            "percent_consumed": percent,
            "alert": alert
        }
    finally:
        conn.close()