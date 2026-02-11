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