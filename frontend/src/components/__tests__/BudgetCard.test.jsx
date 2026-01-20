import { render, screen } from "@testing-library/react";
import BudgetCard from "../BudgetCard"; // Vérifie que le chemin est bon
import { describe, it, expect } from "vitest";
import React from "react";

describe("BudgetCard Component", () => {
  // Cas 1 : Affichage normal
  it("affiche correctement les montants et le reste", () => {
    render(
      <BudgetCard
        category="Courses"
        amount={100}
        spent={50}
        percent={50}
        alert={null}
      />,
    );

    // Vérifie que le titre est là
    expect(screen.getByText("Courses")).toBeInTheDocument();
    // Vérifie le calcul du reste (100 - 50 = 50)
    expect(screen.getByText("Reste : 50.00€")).toBeInTheDocument();
    // Vérifie le pourcentage
    expect(screen.getByText("50.0% consommé")).toBeInTheDocument();
  });

  // Cas 2 : Budget dépassé (Logique visuelle importante)
  it('affiche "DÉPASSÉ" quand le pourcentage dépasse 100%', () => {
    render(
      <BudgetCard
        category="Loisirs"
        amount={100}
        spent={120}
        percent={120}
        alert="Attention"
      />,
    );

    // On cherche le texte spécifique "DÉPASSÉ"
    expect(screen.getByText("DÉPASSÉ")).toBeInTheDocument();
    // On vérifie que le texte "Reste" N'EST PAS là
    expect(screen.queryByText(/Reste :/)).not.toBeInTheDocument();
  });

  // Cas 3 : Alerte
  it("affiche le message d'alerte si présent", () => {
    render(
      <BudgetCard
        category="Transport"
        amount={100}
        spent={90}
        percent={90}
        alert="Attention seuil critique"
      />,
    );

    expect(screen.getByText("Attention seuil critique")).toBeInTheDocument();
    // Vérifie la présence du petit badge jaune/rouge
    expect(screen.getByText("⚠️ Attention")).toBeInTheDocument();
  });
});
