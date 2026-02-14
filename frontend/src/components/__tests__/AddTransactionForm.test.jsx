import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import AddTransactionForm from '../AddTransactionForm';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import React from 'react';


global.fetch = vi.fn();

global.alert = vi.fn();

describe('AddTransactionForm Component', () => {
    
    // Avant chaque test, on nettoie les mocks pour partir de zéro
    beforeEach(() => {
        vi.clearAllMocks();
    });

    // Cas 1 : Vérifier que le formulaire s'affiche bien
    it('affiche tous les champs nécessaires', () => {
        render(<AddTransactionForm />);

        // On vérifie la présence des champs via leurs placeholders ou labels
        expect(screen.getByText('Libellé')).toBeInTheDocument();
        expect(screen.getByPlaceholderText('Ex: Courses Super U')).toBeInTheDocument();
        
        expect(screen.getByText(/Montant/)).toBeInTheDocument();
        expect(screen.getByPlaceholderText('0.00')).toBeInTheDocument();
        
        expect(screen.getByText('Catégorie')).toBeInTheDocument();
        
        // Vérifie le bouton
        expect(screen.getByRole('button', { name: /Ajouter/i })).toBeInTheDocument();
    });

    // Cas 2 : Vérifier la soumission du formulaire 
    it('appelle l\'API avec les bonnes données quand on valide', async () => {
        // On simule une réponse positive de l'API (200 OK)
        global.fetch.mockResolvedValueOnce({
            ok: true,
            json: async () => ({ message: "Succès" }),
        });

        const mockOnAdded = vi.fn(); // Une fausse fonction pour voir si elle est appelée

        render(<AddTransactionForm onTransactionAdded={mockOnAdded} />);

        // 1. L'utilisateur remplit les champs
        fireEvent.change(screen.getByPlaceholderText('Ex: Courses Super U'), { target: { value: 'Cinéma' } });
        fireEvent.change(screen.getByPlaceholderText('0.00'), { target: { value: '12.50' } });
        fireEvent.change(screen.getByPlaceholderText('Ex: Alimentation'), { target: { value: 'Loisirs' } });

        // 2. L'utilisateur clique sur Ajouter
        const button = screen.getByRole('button', { name: /Ajouter/i });
        fireEvent.click(button);

        // 3. On s'attend à ce que fetch ait été appelé
        await waitFor(() => {
            expect(global.fetch).toHaveBeenCalledTimes(1);
        });

        // 4. On vérifie que les données envoyées sont correctes
        expect(global.fetch).toHaveBeenCalledWith(
            'http://127.0.0.1:8000/transactions/',
            expect.objectContaining({
                method: 'POST',
                body: expect.stringContaining('"label":"Cinéma"'),
            })
        );
        
        // 5. On vérifie que le montant est bien dans le body (et bien converti)
        expect(global.fetch).toHaveBeenCalledWith(
            expect.any(String),
            expect.objectContaining({
                body: expect.stringContaining('12.5'),
            })
        );

        // 6. On vérifie que le callback parent a été appelé (pour rafraîchir la liste)
        expect(mockOnAdded).toHaveBeenCalled();
        
        // 7. On vérifie le message de succès
        expect(global.alert).toHaveBeenCalledWith("Transaction ajoutée avec succès !");
    });

    it('refuse un montant avec plus de 2 décimales', async () => {
        render(<AddTransactionForm />);

        fireEvent.change(screen.getByPlaceholderText('Ex: Courses Super U'), { target: { value: 'Cinéma' } });
        fireEvent.change(screen.getByPlaceholderText('0.00'), { target: { value: '13.589' } });
        fireEvent.change(screen.getByPlaceholderText('Ex: Alimentation'), { target: { value: 'Loisirs' } });

        const button = screen.getByRole('button', { name: /Ajouter/i });
        fireEvent.click(button);

        expect(global.fetch).not.toHaveBeenCalled();
        expect(global.alert).toHaveBeenCalledWith("Le montant doit avoir au maximum 2 décimales.");
    });
});