# Carnet de Bord - User Stories

## US 1 : Ajouter une transaction
**En tant qu’** utilisateur  
**Je veux** pouvoir ajouter une transaction (revenu ou dépense)  
**Afin de** suivre mon budget au fil du temps.

### Critères d’acceptation (Backend & Front)
- [x] Backend : Route POST /transactions/ créée
- [x] Backend : Refus si montant <= 0 (Testé TDD)
- [x] Frontend : Formulaire avec champs (Montant, Libellé, Type, Catégorie, Date)
- [x] Frontend : Le bouton "Ajouter" envoie les données à l'API
- [x] Frontend : La transaction s'affiche ou les budgets se mettent à jour après ajout
- [x] Frontend : Gestion des erreurs (alerte si échec)
---

## US 2 : Voir et filtrer les transactions
**En tant qu’** utilisateur  
**Je veux** consulter mes transactions avec un filtre simple  
**Afin de** retrouver rapidement mes dépenses.

### Critères d’acceptation
- [x] Liste/tableau de transactions visible
- [x] Filtrage possible par catégorie ou par période
- [x] Le filtre met à jour la liste instantanément (Testé Front)
- [x] Si aucune transaction : message “Aucune transaction”

## US 3 : Définir un budget par catégorie
**En tant qu’** utilisateur  
**Je veux** définir un budget mensuel par catégorie  
**Afin de** contrôler mes dépenses.

### Critères d’acceptation
- [x] Choix de la catégorie, période et montant maximum
- [x] Budget enregistré en base et affiché immédiatement
- [x] Impossible de mettre un budget négatif (Message d'erreur)
- [x] Une catégorie ne peut pas avoir deux budgets sur la même période

## US 4 : Suivre la consommation du budget
**En tant qu’** utilisateur  
**Je veux** voir combien j’ai dépensé et combien il me reste  
**Afin de** savoir si je dépasse mon budget.

### Critères d’acceptation
- [x] [cite_start]Affichage par catégorie : total dépensé, budget, restant/dépassement 
- [x] [cite_start]Si dépassement : affichage clair (alerte visuelle) 
- [x] [cite_start]Calcul correct du pourcentage consommé