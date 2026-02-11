import React, { useState } from 'react';

const AddTransactionForm = ({ onTransactionAdded }) => {
  // Critère : Saisie obligatoire montant, libellé, type, catégorie, date
  const [label, setLabel] = useState('');
  const [amount, setAmount] = useState('');
  const [category, setCategory] = useState('');
  const [date, setDate] = useState(new Date().toISOString().split('T')[0]); 
  const [type, setType] = useState('DEPENSE');

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // On prépare les données pour l'API
    const payload = {
      label: label,
      amount: parseFloat(amount),
      category: category,
      date: date,
      type: type
    };

    try {
      const response = await fetch('http://127.0.0.1:8000/transactions/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        // Critère : Validation visuelle
        alert("Transaction ajoutée avec succès !");
        
        // Reset du formulaire pour enchainer
        setLabel('');
        setAmount('');
        
        // Callback pour rafraichir la liste parente
        if (onTransactionAdded) onTransactionAdded();
      } else {
        // Critère : Gestion d'erreur (ex: Montant négatif renvoyé par le back)
        const errorData = await response.json();
        alert("Erreur : " + (errorData.detail || "Inconnue"));
      }
    } catch (error) {
      console.error("Erreur:", error);
      alert("Erreur de connexion au serveur");
    }
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow-md border border-gray-100 mb-8 mt-6">
      <h3 className="text-lg font-bold text-gray-800 mb-4 flex items-center gap-2">
        💳 Nouvelle Transaction
      </h3>
      
      <form onSubmit={handleSubmit} className="flex flex-wrap gap-4 items-end">
        {/* Type (Revenu / Dépense) */}
        <div>
            <label className="block text-xs font-bold text-gray-500 uppercase mb-1">Type</label>
            <select 
                value={type} 
                onChange={(e) => setType(e.target.value)}
                className="border border-gray-300 rounded px-3 py-2 bg-white"
            >
                <option value="DEPENSE">Dépense</option>
                <option value="REVENU">Revenu</option>
            </select>
        </div>

        {/* Date */}
        <div>
          <label className="block text-xs font-bold text-gray-500 uppercase mb-1">Date</label>
          <input 
            type="date" 
            value={date} onChange={(e) => setDate(e.target.value)}
            className="border border-gray-300 rounded px-3 py-2"
            required 
          />
        </div>

        {/* Catégorie */}
        <div>
          <label className="block text-xs font-bold text-gray-500 uppercase mb-1">Catégorie</label>
          <input 
            type="text" 
            value={category} onChange={(e) => setCategory(e.target.value)}
            placeholder="Ex: Alimentation"
            className="border border-gray-300 rounded px-3 py-2 w-32"
            required 
          />
        </div>

        {/* Description */}
        <div className="flex-grow">
          <label className="block text-xs font-bold text-gray-500 uppercase mb-1">Libellé</label>
          <input 
            type="text" 
            value={label} onChange={(e) => setLabel(e.target.value)}
            placeholder="Ex: Courses Super U"
            className="border border-gray-300 rounded px-3 py-2 w-full"
            required 
          />
        </div>

        {/* Montant */}
        <div>
          <label className="block text-xs font-bold text-gray-500 uppercase mb-1">Montant (€)</label>
          <input 
            type="number" 
            value={amount} onChange={(e) => setAmount(e.target.value)}
            placeholder="0.00"
            step="0.01"
            className="border border-gray-300 rounded px-3 py-2 w-24 font-bold text-right"
            required 
          />
        </div>

        <button 
          type="submit"
          className="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 transition-colors font-bold shadow-lg shadow-indigo-200"
        >
          Ajouter
        </button>
      </form>
    </div>
  );
};

export default AddTransactionForm;