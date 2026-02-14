from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
from datetime import datetime
from decimal import Decimal
from src.budget import add_budget, calculate_remaining_budget, calculate_budget_percentage, check_budget_alert
from src.transaction import Transaction

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modèle de données pour valider ce que l'utilisateur envoie
class BudgetModel(BaseModel):
    category: str
    amount: float
    period: str

class TransactionModel(BaseModel):
    date: str
    amount: float
    category: str
    type: str
    label: str

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
    except ValueError as e:
        conn.close()
        raise HTTPException(status_code=400, detail=str(e))
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


@app.get("/budgets/")
def get_all_budgets_route():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        # On récupère tout
        cursor.execute("SELECT category, amount, period FROM budgets")
        rows = cursor.fetchall()
        
        # On transforme le résultat SQL en liste de dictionnaires propre
        results = []
        for row in rows:
            results.append({
                "category": row[0], 
                "amount": row[1],
                "period": row[2]
            })
        return results
    finally:
        conn.close()


@app.delete("/budgets/{category}/{period}")
def delete_budget_route(category: str, period: str):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM budgets WHERE category = ? AND period = ?",
            (category, period)
        )
        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Budget introuvable")

        return {"message": "Budget supprimé"}
    finally:
        conn.close()


@app.post("/transactions/")
def create_transaction_route(api_data: TransactionModel):
    try:
        
        new_transaction = Transaction(
            user_id=1, 
            date=datetime.strptime(api_data.date, "%Y-%m-%d").date(),
            amount=Decimal(str(api_data.amount)),
            category=api_data.category,
            type=api_data.type,
            description=api_data.label
        )
        
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO transactions (date, amount, category, type, label) VALUES (?, ?, ?, ?, ?)",
            (
                new_transaction.date.isoformat(), 
                float(new_transaction.amount), 
                new_transaction.category, 
                new_transaction.type, 
                new_transaction.description
            )
        )
        conn.commit()
        conn.close()
        
        return {"message": "Transaction ajoutée avec succès"}

    except ValueError as e:
        
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/transactions/")
def get_all_transactions_route():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, date, amount, category, type, label FROM transactions")
        rows = cursor.fetchall()
        
        results = []
        for row in rows:
            results.append({
                "id": row[0],
                "date": row[1],
                "amount": row[2],
                "category": row[3],
                "type": row[4],
                "label": row[5]
            })
        return results
    finally:
        conn.close()


@app.delete("/transactions/{transaction_id}")
def delete_transaction_route(transaction_id: int):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Transaction introuvable")

        return {"message": "Transaction supprimée"}
    finally:
        conn.close()