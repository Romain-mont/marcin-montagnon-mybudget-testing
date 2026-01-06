def add_budget(connection, category, amount, period):
    """
    Enregistre un budget dans la base de données via la connexion fournie.
    """
    cursor = connection.cursor()
    
    # On prépare la requête SQL (les ? protègent contre les injections SQL)
    sql = "INSERT INTO budgets (category, amount, period) VALUES (?, ?, ?)"
    
    # On exécute la requête avec les données
    cursor.execute(sql, (category, amount, period))
    
    # On sauvegarde (commit) la transaction
    connection.commit()
    
    return True