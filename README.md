# 💰 MyBudget - Application de Gestion de Budget Personnel

Application web full-stack pour suivre vos dépenses, définir des budgets par catégorie et visualiser votre consommation budgétaire en temps réel.

## 📋 Table des matières

- [Technologies utilisées](#technologies-utilisées)
- [Installation](#installation)
- [Lancement de l'application](#lancement-de-lapplication)
- [Fonctionnalités MVP](#fonctionnalités-mvp)
- [Scénarios BDD](#scénarios-bdd)
- [Exécution des tests](#exécution-des-tests)
- [Structure du projet](#structure-du-projet)

---

## 🛠 Technologies utilisées

### Backend
- **FastAPI** - Framework Python pour l'API REST
- **SQLite** - Base de données légère
- **unittest** - Framework de tests unitaires Python (natif)
- **coverage** - Outil de couverture de code (optionnel)

### Frontend
- **React** - Bibliothèque JavaScript UI
- **Vite** - Build tool moderne
- **Tailwind CSS** - Framework CSS
- **Vitest** - Framework de tests unitaires React
- **React Testing Library** - Tests des composants

---

## 📦 Installation

### Prérequis
- Python 3.8+ installé
- Node.js 16+ et npm installés
- Git

### 1. Cloner le repository

```bash
git clone <url-du-repo>
cd marcin-montagnon-mybudget-testing
```

### 2. Installation Backend

```bash
cd backend

# Créer un environnement virtuel (recommandé)
python3 -m venv .venv
source .venv/bin/activate  # Sur macOS/Linux
# ou
.venv\Scripts\activate  # Sur Windows

# Installer les dépendances
pip install fastapi uvicorn[standard] pydantic httpx coverage
```

**Dépendances principales** :
- `fastapi` - Framework API
- `uvicorn` - Serveur ASGI
- `pydantic` - Validation de données
- `httpx` - Client HTTP pour les tests API
- `coverage` - Couverture de code (optionnel)

### 3. Installation Frontend

```bash
cd frontend
npm install
```

---

## 🚀 Lancement de l'application

L'application nécessite deux terminaux distincts (backend + frontend).

### Terminal 1 : Backend (API)

```bash
cd backend
source venv/bin/activate  # Si environnement virtuel utilisé
uvicorn main:app --reload
```
.
✅ L'API sera accessible sur : **http://127.0.0.1:8000**

📚 Documentation API auto-générée : **http://127.0.0.1:8000/docs**

### Terminal 2 : Frontend (Interface web)

```bash
cd frontend
npm run dev
```

✅ L'interface sera accessible sur : **http://localhost:5173**

---

## ✨ Fonctionnalités MVP

### 🔹 US1 : Ajouter une transaction

**Fonctionnalité** : Enregistrer une dépense ou un revenu avec montant, catégorie, date et libellé.

**Utilisation via l'interface** :
1. Ouvrir http://localhost:5173
2. Remplir le formulaire "Nouvelle Transaction" :
   - Type : Dépense ou Revenu
   - Date : Date de la transaction
   - Catégorie : Ex. "Alimentation"
   - Libellé : Ex. "Courses Super U"
   - Montant : Ex. 42.50
3. Cliquer sur "Ajouter"
4. ✅ Confirmation : "Transaction ajoutée avec succès !"

**Utilisation via API** :
```bash
curl -X POST http://127.0.0.1:8000/transactions/ \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2026-02-11",
    "amount": 42.50,
    "category": "Alimentation",
    "type": "DEPENSE",
    "label": "Courses Super U"
  }'
```

**Règles de validation** :
- ❌ Montant doit être > 0
- ❌ Type doit être "DEPENSE" ou "REVENU"
- ❌ Tous les champs sont obligatoires

---

### 🔹 US2 : Voir et filtrer les transactions

**Fonctionnalité** : Consulter l'historique des transactions avec filtre par catégorie.

**Utilisation** :
1. La liste "📜 Historique" s'affiche automatiquement en bas de page
2. Utiliser le champ "Filtrer par catégorie..." pour rechercher
3. La liste se met à jour instantanément

**Exemple de filtre** :
- Saisir "Alimentation" → Affiche uniquement les transactions de cette catégorie
- Effacer le filtre → Affiche toutes les transactions

**API - Récupérer toutes les transactions** :
```bash
curl http://127.0.0.1:8000/transactions/
```

---

### 🔹 US3 : Définir un budget par catégorie

**Fonctionnalité** : Fixer un budget mensuel pour contrôler les dépenses d'une catégorie.

**Utilisation via l'interface** :
1. Remplir le formulaire "Nouveau Budget" :
   - Catégorie : Ex. "Alimentation"
   - Montant : Ex. 500
   - Période : Ex. "2026-02" (format YYYY-MM)
2. Cliquer sur "Ajouter Budget"
3. ✅ Une carte budget apparaît immédiatement

**Utilisation via API** :
```bash
curl -X POST http://127.0.0.1:8000/budgets/ \
  -H "Content-Type: application/json" \
  -d '{
    "category": "Alimentation",
    "amount": 500,
    "period": "2026-02"
  }'
```

**Règles** :
- ❌ Impossible de créer deux budgets identiques (même catégorie + période)
- ❌ Montant doit être positif

---

### 🔹 US4 : Suivre la consommation du budget

**Fonctionnalité** : Visualiser en temps réel le montant dépensé, restant et un pourcentage de consommation.

**Affichage sur les cartes budget** :
- 💸 **Dépensé** : Total des dépenses de la catégorie
- 💰 **Budget** : Montant fixé
- ✅ **Reste** : Budget - Dépensé
- 📊 **Pourcentage** : (Dépensé / Budget) × 100

**Alertes visuelles** :
- 🟢 < 80% : Carte verte, tout va bien
- 🟡 ≥ 80% : Carte jaune + message "⚠️ Attention seuil critique"
- 🔴 > 100% : Carte rouge + badge "DÉPASSÉ"

**API - Consulter un budget** :
```bash
curl http://127.0.0.1:8000/budgets/Alimentation/2026-02
```

Réponse :
```json
{
  "category": "Alimentation",
  "budget_amount": 500.0,
  "remaining": 150.0,
  "percent_consumed": 70.0,
  "alert": null
}
```

---

## 📝 Scénarios BDD

Le projet utilise une **approche BDD (Behavior-Driven Development)** pour les tests, avec la notation **Given/When/Then**.

### Méthodologie

Les tests suivent la structure :
- **Given** (Étant donné) : Contexte/État initial
- **When** (Quand) : Action déclenchée
- **Then** (Alors) : Résultat attendu

### Scénario 1 : Calcul du budget restant

**Fichier** : [test_budget.py](backend/test/test_budget.py)

```gherkin
Feature: Calcul du budget restant
  En tant qu'utilisateur
  Je veux connaître le montant restant de mon budget
  Afin de gérer mes dépenses

  Scenario: Calculer le reste avec des dépenses existantes
    Given un budget de 500€ pour la catégorie "Alimentation" en "2026-01"
    And des dépenses de 100€ et 50€ dans cette catégorie
    When je calcule le budget restant
    Then le système retourne 350€ (500 - 150)
```

**Implémentation** :
```python
def test_calculate_remaining_budget(self):
    # Given : Un budget de 500€
    add_budget(self.conn, "Alimentation", 500.0, "2026-01")
    
    # And : Des dépenses existantes dans cette catégorie (Total = 150€)
    self.cursor.execute("INSERT INTO transactions (amount, category, type) VALUES (100.0, 'Alimentation', 'DEPENSE')")
    self.cursor.execute("INSERT INTO transactions (amount, category, type) VALUES (50.0, 'Alimentation', 'DEPENSE')")
    self.conn.commit()

    # When : Je calcule le reste
    remaining = calculate_remaining_budget(self.conn, "Alimentation", "2026-01")

    # Then : Il doit rester 350€ (500 - 150)
    self.assertEqual(remaining, 350.0)
```

---

### Scénario 2 : Alerte de dépassement budgétaire

**Fichier** : [test_budget.py](backend/test/test_budget.py)

```gherkin
Feature: Alertes budgétaires
  En tant qu'utilisateur
  Je veux recevoir une alerte quand j'atteins 80% de mon budget
  Afin d'éviter les dépassements

  Scenario: Alerte au seuil de 80%
    Given un budget de 100€ pour la catégorie "Resto"
    And des dépenses totales de 85€
    When je vérifie le statut du budget
    Then le système retourne une alerte "Attention : vous avez consommé 85.0% de votre budget Resto"
```

**Implémentation** :
```python
def test_check_budget_alert_threshold(self):
    # Given : Budget 100€, Dépenses actuelles 75€
    add_budget(self.conn, "Resto", 100.0, "2026-05")
    self.cursor.execute("INSERT INTO transactions (amount, category, type) VALUES (75.0, 'Resto', 'DEPENSE')")
    self.cursor.execute("INSERT INTO transactions (amount, category, type) VALUES (10.0, 'Resto', 'DEPENSE')")
    self.conn.commit()
    
    # When : On vérifie l'alerte
    message = check_budget_alert(self.conn, "Resto", "2026-05")
    
    # Then : Alerte présente
    self.assertEqual(message, "Attention : vous avez consommé 85.0% de votre budget Resto")
```

---

### Scénario 3 : Validation d'une transaction

**Fichier** : [test_transaction.py](backend/test/test_transaction.py)

```gherkin
Feature: Validation des transactions
  En tant que système
  Je veux rejeter les transactions invalides
  Afin de garantir l'intégrité des données

  Scenario: Rejet d'un montant négatif
    Given je tente de créer une transaction avec un montant de -50€
    When le système valide la transaction
    Then une erreur ValueError est levée avec le message "Le montant doit être positif"

  Scenario: Rejet d'un montant nul
    Given je tente de créer une transaction avec un montant de 0€
    When le système valide la transaction
    Then une erreur ValueError est levée
```

**Implémentation** :
```python
def test_amount_must_be_positive(self):
    """Le montant doit être positif"""
    with self.assertRaises(ValueError):
        Transaction(
            user_id=1,
            date=date.today(),
            amount=Decimal('-50.00'),
            category='Test',
            type='DEPENSE'
        )

def test_amount_cannot_be_zero(self):
    """Le montant ne peut pas être zéro"""
    with self.assertRaises(ValueError):
        Transaction(
            user_id=1,
            date=date.today(),
            amount=Decimal('0.00'),
            category='Test',
            type='DEPENSE'
        )
```

---

### Scénario 4 : Consultation d'un budget via API

**Fichier** : [test_api_budget.py](backend/test/test_api_budget.py)

```gherkin
Feature: API de consultation des budgets
  En tant que client de l'API
  Je veux consulter le statut d'un budget
  Afin d'afficher les informations dans l'interface

  Scenario: Récupérer le statut d'un budget avec dépenses
    Given un budget "Resto" de 100€ pour la période "2026-05"
    And une dépense de 20€ dans cette catégorie
    When je consulte GET /budgets/Resto/2026-05
    Then je reçois un statut 200
    And les données contiennent budget_amount=100.0
    And les données contiennent remaining=80.0
    And aucune alerte n'est présente
```

**Implémentation** :
```python
def test_get_budget_status_api(self):
    # GIVEN : On injecte des données directement en base
    conn = sqlite3.connect('budget.db')
    conn.execute("INSERT INTO budgets (category, amount, period) VALUES ('Resto', 100.0, '2026-05')")
    conn.execute("INSERT INTO transactions (amount, category, type) VALUES (20.0, 'Resto', 'DEPENSE')")
    conn.commit()
    conn.close()

    # WHEN : On appelle la route GET
    response = self.client.get("/budgets/Resto/2026-05")
    
    # THEN : On s'attend à un succès
    self.assertEqual(response.status_code, 200)
    data = response.json()
    self.assertEqual(data["budget_amount"], 100.0)
    self.assertEqual(data["remaining"], 80.0)
    self.assertIsNone(data["alert"])
```

---

### Scénario 5 : Rejet d'une transaction invalide par l'API

**Fichier** : [test_api_transaction.py](backend/test/test_api_transaction.py)

```gherkin
Feature: Validation des transactions via API
  En tant que système
  Je veux rejeter les transactions avec montant négatif
  Afin de protéger l'intégrité de la base de données

  Scenario: Tentative de création avec montant négatif
    Given je prépare une requête POST /transactions/ avec amount=-10.0
    When j'envoie la requête à l'API
    Then je reçois un statut 400
    And le message d'erreur contient "Le montant doit être positif"
```

**Implémentation** :
```python
def test_create_transaction_business_rule_error(self):
    """Cas d'erreur : On viole une règle métier (Montant négatif)"""
    payload = {
        "date": "2026-01-20",
        "amount": -10.0,  
        "category": "Alimentation",
        "type": "DEPENSE",
        "label": "Test"
    }
    response = self.client.post("/transactions/", json=payload)
    
    self.assertEqual(response.status_code, 400)
    self.assertIn("Le montant doit être positif", response.json()['detail'])
```

---

### Avantages de l'approche BDD

✅ **Lisibilité** : Les tests sont compréhensibles par des non-développeurs  
✅ **Documentation vivante** : Les tests servent de spécification fonctionnelle  
✅ **Traçabilité** : Chaque scénario est lié à une User Story  
✅ **Maintenabilité** : Structure claire et prévisible  

---

## 🧪 Exécution des tests

### Tests Backend (Python)

**Lancer tous les tests** :
```bashunittest)

Les tests backend utilisent le framework **unittest** (natif Python).

**Lancer tous les tests** :
```bash
cd backend
python -m unittest discover -s test -p "test_*.py"
```

**Lancer un fichier de test spécifique** :
```bash
# Tests transactions
python -m unittest test.test_transaction

# Tests budgets
python -m unittest test.test_budget

# Tests API transactions
python -m unittest test.test_api_transaction

# Tests API budgets
python -m unittest test.test_api_budget
```

**Avec rapport de couverture (nécessite coverage)** :
```bash
# Installer coverage si besoin
pip install coverage

# Lancer les tests avec couverture
coverage run -m unittest discover -s test -p "test_*.py"

# Afficher le rapport
coverage report -m

# Générer un rapport HTML détaillé
coverage html
# Puis ouvrir htmlcov/index.html dans un navigateur
```

**Alternative : Lancer directement un fichier** :
```bash
python test/test_budget.py
python test/test_transaction.py
```

**Résultats attendus** :
- ✅ 15+ tests passent
- ✅ Couverture > 80% sur la logique métier (src/)

**Tests disponibles** :
- `test_transaction.py` : Validation métier des transactions (montant > 0, type valide, etc.)
- `test_budget.py` : Calculs budgétaires (reste, pourcentage, alertes à 80%)
- `test_api_transaction.py` : Routes API transactions (POST, validation)
- `test_api_budget.py` : Routes API budgets (POST, GET, calculs)
### Tests Frontend (React)

**Lancer tous les tests** :
```bash
cd frontend
npm run test
```



**Tests disponibles** :
- `AddTransactionForm.test.jsx` : Validation formulaire + envoi API
- `TransactionList.test.jsx` : Affichage et filtrage
- `BudgetCard.test.jsx` : Affichage alertes et dépassement

---

## 📁 Structure du projet

```
marcin-montagnon-mybudget-testing/
├── backend/
│   ├── main.py                 # API FastAPI
│   ├── budget.db               # Base de données SQLite (auto-créée)
│   ├── src/
│   │   ├── budget.py           # Logique métier budgets
│   │   └── transaction.py      # Modèle Transaction
│   └── test/
│       ├── test_budget.py      # Tests unitaires budgets
│       ├── test_transaction.py # Tests unitaires transactions
│       ├── test_api_budget.py  # Tests d'intégration API
│       └── test_api_transaction.py
├── frontend/
│   ├── src/
│   │   ├── App.jsx             # Composant principal
│   │   ├── components/
│   │   │   ├── AddBudgetForm.jsx
│   │   │   ├── AddTransactionForm.jsx
│   │   │   ├── BudgetCard.jsx
│   │   │   ├── TransactionList.jsx
│   │   │   └── __tests__/      # Tests composants
│   │   └── ...
│   ├── package.json
│   └── vite.config.js
└── README.md
```

---

## 🎯 User Stories implémentées

- ✅ **US1** : Ajouter une transaction avec validation
- ✅ **US2** : Voir et filtrer les transactions
- ✅ **US3** : Définir un budget par catégorie
- ✅ **US4** : Suivre la consommation avec alertes

---

## 👤 Auteurs

Projet réalisé dans le cadre du cours **Tests Unitaires** - EPSI 2026

---

## 📝 Licence

Ce projet est un projet pédagogique.