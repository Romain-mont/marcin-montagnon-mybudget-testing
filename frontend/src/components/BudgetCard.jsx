import React from "react";

const BudgetCard = ({ category, amount, spent, percent, alert }) => {
  const getColor = () => {
    if (percent >= 100) return "bg-red-600";
    if (percent >= 80) return "bg-orange-400";
    return "bg-green-500";
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow-md border border-gray-100 hover:shadow-lg transition-shadow">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-xl font-bold text-gray-800">{category}</h3>
        {alert && (
          <span className="bg-red-100 text-red-800 text-xs font-semibold mr-2 px-2.5 py-0.5 rounded border border-red-400">
            ⚠️ Attention
          </span>
        )}
      </div>

      {/* Montants */}
      <div className="flex justify-between text-sm text-gray-600 mb-2">
        <span>
          Dépensé :{" "}
          <span className="font-semibold text-gray-900">{spent}€</span>
        </span>
        <span>
          Budget :{" "}
          <span className="font-semibold text-gray-900">{amount}€</span>
        </span>
      </div>

      {/* Barre de progression */}
      <div className="w-full bg-gray-200 rounded-full h-4 mb-2 overflow-hidden">
        <div
          className={`${getColor()} h-4 rounded-full transition-all duration-1000 ease-out`}
          style={{ width: `${Math.min(percent, 100)}%` }}
        ></div>
      </div>

      {/* Pourcentage et Reste */}
      <div className="flex justify-between text-xs text-gray-500 mt-2">
        <span>{percent.toFixed(1)}% consommé</span>
        <span
          className={
            percent >= 100
              ? "text-red-600 font-bold"
              : "text-green-600 font-bold"
          }
        >
          {percent >= 100
            ? "DÉPASSÉ"
            : `Reste : ${(amount - spent).toFixed(2)}€`}
        </span>
      </div>

      {/* Message d'alerte spécifique */}
      {alert && <p className="mt-3 text-xs text-red-600 italic">{alert}</p>}
    </div>
  );
};

export default BudgetCard;
