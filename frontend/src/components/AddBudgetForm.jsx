import React, { useState } from "react";

const AddBudgetForm = ({ onBudgetAdded }) => {
  const [category, setCategory] = useState("");
  const [amount, setAmount] = useState("");
  const [period, setPeriod] = useState("2026-01");

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Prépare les données
    const payload = {
      category: category,
      amount: parseFloat(amount),
      period: period,
    };

    try {
      // Envoie au backend
      const response = await fetch("http://127.0.0.1:8000/budgets/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        // Reset du formulaire
        setCategory("");
        setAmount("");
        // Notifie le parent pour recharger la liste
        if (onBudgetAdded) onBudgetAdded();
        alert("Budget ajouté avec succès !");
      } else {
        alert("Erreur lors de l'ajout");
      }
    } catch (error) {
      console.error("Erreur:", error);
    }
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow-md border border-gray-100 mb-8">
      <h2 className="text-xl font-bold text-gray-800 mb-4">
        ➕ Définir un nouveau budget
      </h2>
      <form onSubmit={handleSubmit} className="flex flex-wrap gap-4 items-end">
        {/* Catégorie */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Catégorie
          </label>
          <input
            type="text"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            placeholder="Ex: Sport"
            className="border border-gray-300 rounded px-3 py-2 w-48"
            required
          />
        </div>

        {/* Montant */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Montant (€)
          </label>
          <input
            type="number"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            placeholder="Ex: 50"
            className="border border-gray-300 rounded px-3 py-2 w-32"
            required
          />
        </div>

        {/* Période */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Période
          </label>
          <input
            type="text"
            value={period}
            onChange={(e) => setPeriod(e.target.value)}
            placeholder="YYYY-MM"
            className="border border-gray-300 rounded px-3 py-2 w-32"
            required
          />
        </div>

        <button
          type="submit"
          className="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 transition-colors font-semibold"
        >
          Ajouter
        </button>
      </form>
    </div>
  );
};

export default AddBudgetForm;
