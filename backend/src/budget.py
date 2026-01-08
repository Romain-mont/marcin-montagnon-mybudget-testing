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

def calculate_budget_percentage(connection, category, period):
    cursor = connection.cursor()
    
    # 1. Récupérer le budget
    cursor.execute("SELECT amount FROM budgets WHERE category = ? AND period = ?", (category, period))
    row = cursor.fetchone()
    if not row:
        return 0.0
    budget_total = row[0]
    
    if budget_total == 0:
        return 0.0 # Protection anti-crash
        
    # 2. Récupérer les dépenses
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE category = ? AND type = 'DEPENSE'", (category,))
    expense_result = cursor.fetchone()
    total_spent = expense_result[0] if expense_result[0] is not None else 0.0
    
    # 3. Calcul
    return (total_spent / budget_total) * 100

def check_budget_alert(connection, category, period):
    """
    Renvoie un message d'alerte si le budget est consommé à >= 80%.
    Sinon, renvoie None.
    """
    # 1. On réutilise la logique existante (DRY - Don't Repeat Yourself)
    percent = calculate_budget_percentage(connection, category, period)
    
    # 2. Vérification du seuil critique (80%)
    if percent >= 80.0:
        return f"Attention : vous avez consommé {percent}% de votre budget {category}"
    
    return None