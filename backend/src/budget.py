def add_budget(category, amount, period):
    # On retourne simplement les données pour valider le test
    # (Plus tard, on remplacera ça par l'enregistrement en base de données)
    return {
        "category": category,
        "amount": amount,
        "period": period
    }