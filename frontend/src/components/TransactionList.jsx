import React, { useState, useEffect } from 'react';

const TransactionList = ({ refreshTrigger }) => {
  const [transactions, setTransactions] = useState([]);
  const [filterCategory, setFilterCategory] = useState('');
  const [loading, setLoading] = useState(true);
  const [deletingId, setDeletingId] = useState(null);

  // Fonction pour charger les transactions
  const fetchTransactions = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/transactions/');
      const data = await response.json();
      
      setTransactions(data.reverse());
      setLoading(false);
    } catch (error) {
      console.error("Erreur chargement transactions:", error);
      setLoading(false);
    }
  };

  // Recharger quand le parent le demande (refreshTrigger)
  useEffect(() => {
    fetchTransactions();
  }, [refreshTrigger]);

  const handleDelete = async (transactionId) => {
    if (!transactionId) return;

    setDeletingId(transactionId);
    try {
      await fetch(`http://127.0.0.1:8000/transactions/${transactionId}/`, {
        method: 'DELETE'
      });
      await fetchTransactions();
    } catch (error) {
      console.error('Erreur suppression transaction:', error);
    } finally {
      setDeletingId(null);
    }
  };

  // Logique de filtrage (JS pur)
  const filteredTransactions = transactions.filter(t => {
    if (filterCategory === '') return true; 
    return t.category.toLowerCase().includes(filterCategory.toLowerCase());
  });

  return (
    <div className="bg-white p-6 rounded-xl shadow-md border border-gray-100 mt-8">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold text-gray-800">📜 Historique</h2>
        
        {/* Filtre simple */}
        <input 
          type="text" 
          placeholder="Filtrer par catégorie..." 
          value={filterCategory}
          onChange={(e) => setFilterCategory(e.target.value)}
          className="border border-gray-300 rounded px-3 py-1 text-sm"
        />
      </div>

      {loading ? (
        <p>Chargement...</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="min-w-full text-sm text-left text-gray-500">
            <thead className="text-xs text-gray-700 uppercase bg-gray-50">
              <tr>
                <th className="px-6 py-3">Date</th>
                <th className="px-6 py-3">Libellé</th>
                <th className="px-6 py-3">Catégorie</th>
                <th className="px-6 py-3 text-right">Montant</th>
                <th className="px-6 py-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredTransactions.length > 0 ? (
                filteredTransactions.map((t, index) => (
                  <tr key={index} className="bg-white border-b hover:bg-gray-50">
                    <td className="px-6 py-4">{t.date}</td>
                    <td className="px-6 py-4 font-medium text-gray-900">{t.label || t.description}</td>
                    <td className="px-6 py-4">
                      <span className="bg-indigo-100 text-indigo-800 text-xs font-medium mr-2 px-2.5 py-0.5 rounded">
                        {t.category}
                      </span>
                    </td>
                    <td className={`px-6 py-4 text-right font-bold ${t.type === 'DEPENSE' ? 'text-red-600' : 'text-green-600'}`}>
                      {t.type === 'DEPENSE' ? '-' : '+'} {t.amount} €
                    </td>
                    <td className="px-6 py-4 text-right">
                      <button
                        type="button"
                        onClick={() => handleDelete(t.id)}
                        disabled={deletingId === t.id}
                        className="text-red-600 hover:text-red-800 text-xs font-semibold disabled:opacity-50"
                      >
                        {deletingId === t.id ? 'Suppression...' : 'Supprimer'}
                      </button>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="5" className="text-center py-4">Aucune transaction trouvée</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default TransactionList;