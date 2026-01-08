def add_budget(connection, category, amount, period):
    cursor = connection.cursor()
    sql = "INSERT INTO budgets (category, amount, period) VALUES (?, ?, ?)"
    cursor.execute(sql, (category, amount, period))
    connection.commit()
    return True

def calculate_remaining_budget(connection, category, period):
    cursor = connection.cursor()
    
    # 1. On récupère le montant du budget fixé
    cursor.execute("SELECT amount FROM budgets WHERE category = ? AND period = ?", (category, period))
    budget_row = cursor.fetchone()
    
    if not budget_row:
        return 0.0 # Pas de budget défini = 0 reste
        
    budget_total = budget_row[0]
    
    # 2. On calcule la somme des DÉPENSES pour cette catégorie
   
    sql_expenses = "SELECT SUM(amount) FROM transactions WHERE category = ? AND type = 'DEPENSE'"
    cursor.execute(sql_expenses, (category,))
    expense_result = cursor.fetchone()
    
    # Si aucune dépense, SUM renvoie None en SQL. On transforme ça en 0.0
    total_spent = expense_result[0] if expense_result[0] is not None else 0.0
    
    # 3. On retourne la différence
    return budget_total - total_spent