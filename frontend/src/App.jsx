import { useState, useEffect } from "react";
import BudgetCard from "./components/BudgetCard";
import AddBudgetForm from "./components/AddBudgetForm"; 
import AddTransactionForm from "./components/AddTransactionForm";
import TransactionList from './components/TransactionList';

function App() {
  const [budgets, setBudgets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshKey, setRefreshKey] = useState(0);
  const [deletingBudgetKey, setDeletingBudgetKey] = useState(null);
  
  const refreshAll = () => {
    fetchBudgets();
    setRefreshKey(old => old + 1); 
  };

  // On sort la fonction fetch pour pouvoir l'appeler depuis le formulaire
  const fetchBudgets = async () => {
    try {
      setLoading(true);
      const response = await fetch("http://127.0.0.1:8000/budgets/");
      const data = await response.json();

      const detailedBudgets = await Promise.all(
        data.map(async (b) => {
          const detailRes = await fetch(
            `http://127.0.0.1:8000/budgets/${b.category}/${b.period}`,
          );
          return await detailRes.json();
        }),
      );
      setBudgets(detailedBudgets);
      setLoading(false);
    } catch (error) {
      console.error("Erreur:", error);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBudgets();
  }, []);

  const handleDeleteBudget = async (category, period) => {
    if (!category || !period) return;

    const key = `${category}-${period}`;
    setDeletingBudgetKey(key);
    try {
      await fetch(`http://127.0.0.1:8000/budgets/${category}/${period}`, {
        method: "DELETE"
      });
      await fetchBudgets();
    } catch (error) {
      console.error("Erreur suppression budget:", error);
    } finally {
      setDeletingBudgetKey(null);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold text-center mb-10 text-indigo-800">
          💰 Mon Budget Personnel
        </h1>

        {/* Le Formulaire d'ajout */}
        <AddBudgetForm onBudgetAdded={refreshAll} />
        <AddTransactionForm onTransactionAdded={refreshAll} />

        <div className="border-t border-gray-200 my-8"></div>

        {/* La liste des cartes */}
        {loading ? (
          <p className="text-center text-gray-500">Chargement...</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {budgets.length > 0 ? (
              budgets.map((budget, index) => (
                <BudgetCard
                  key={index}
                  category={budget.category}
                  period={budget.period}
                  amount={budget.budget_amount}
                  spent={budget.budget_amount - budget.remaining}
                  percent={budget.percent_consumed}
                  alert={budget.alert}
                  onDelete={handleDeleteBudget}
                  isDeleting={deletingBudgetKey === `${budget.category}-${budget.period}`}
                />
              ))
            ) : (
              <p className="text-center col-span-3 text-gray-500">
                Aucun budget défini. Utilisez le formulaire ci-dessus !
              </p>
            )}
          </div>
        )}

        <div className="border-t border-gray-200 my-8"></div>

        {/* Liste des transactions */}
        <TransactionList refreshTrigger={refreshKey} />
      </div>
    </div>
  );
}

export default App;
