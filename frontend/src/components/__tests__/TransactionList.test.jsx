import { render, screen, fireEvent, waitFor, within } from '@testing-library/react';
import TransactionList from '../TransactionList';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import React from 'react';

// Données fictives pour le test
const MOCK_TRANSACTIONS = [
    { id: 1, date: '2026-01-01', label: 'Cinéma', amount: 12.5, category: 'Loisirs', type: 'DEPENSE' },
    { id: 2, date: '2026-01-02', label: 'Salaire', amount: 2000, category: 'Travail', type: 'REVENU' },
    { id: 3, date: '2026-01-03', label: 'Courses', amount: 50, category: 'Alimentation', type: 'DEPENSE' }
];

// Mock de fetch
global.fetch = vi.fn();

describe('TransactionList Component', () => {

    beforeEach(() => {
        vi.clearAllMocks();
        
        global.fetch.mockResolvedValue({
            ok: true,
            json: async () => MOCK_TRANSACTIONS,
        });
    });

    it('affiche la liste des transactions après chargement', async () => {
        render(<TransactionList />);

        // Attendre que "Cinéma" apparaisse (preuve que le chargement est fini)
        await waitFor(() => {
            expect(screen.getByText('Cinéma')).toBeInTheDocument();
        });

        // Vérifier les autres éléments
        expect(screen.getByText('Salaire')).toBeInTheDocument();
        expect(screen.getByText('Alimentation')).toBeInTheDocument();
        // Vérifier le formatage du montant (ex: + 2000 € ou - 12.5 €)
        expect(screen.getByText(/2000/)).toBeInTheDocument();
    });

    it('filtre les transactions par catégorie', async () => {
        render(<TransactionList />);

        // 1. Attendre le chargement
        await waitFor(() => expect(screen.getByText('Cinéma')).toBeInTheDocument());

        // 2. Saisir "Loisirs" dans le filtre
        const filterInput = screen.getByPlaceholderText('Filtrer par catégorie...');
        fireEvent.change(filterInput, { target: { value: 'Loisirs' } });

        // 3. Vérifier que "Cinéma" (Loisirs) est toujours là
        expect(screen.getByText('Cinéma')).toBeInTheDocument();

        // 4. Vérifier que "Salaire" (Travail) a DISPARU
        expect(screen.queryByText('Salaire')).not.toBeInTheDocument();
    });

    it('affiche un message si aucune transaction', async () => {
        // Cas particulier : API renvoie liste vide
        global.fetch.mockResolvedValueOnce({
            ok: true,
            json: async () => [],
        });

        render(<TransactionList />);

        await waitFor(() => {
            expect(screen.getByText('Aucune transaction trouvée')).toBeInTheDocument();
        });
    });

    it('supprime une transaction et recharge la liste', async () => {
        global.fetch
            .mockResolvedValueOnce({
                ok: true,
                json: async () => MOCK_TRANSACTIONS,
            })
            .mockResolvedValueOnce({
                ok: true,
            })
            .mockResolvedValueOnce({
                ok: true,
                json: async () => MOCK_TRANSACTIONS,
            });

        render(<TransactionList />);

        await waitFor(() => {
            expect(screen.getByText('Cinéma')).toBeInTheDocument();
        });

        const cinemaRow = screen.getByText('Cinéma').closest('tr');
        const deleteButton = within(cinemaRow).getByRole('button', { name: 'Supprimer' });
        fireEvent.click(deleteButton);

        await waitFor(() => {
            expect(global.fetch).toHaveBeenCalledWith(
                'http://127.0.0.1:8000/transactions/1/',
                expect.objectContaining({ method: 'DELETE' })
            );
        });

        expect(global.fetch).toHaveBeenCalledWith('http://127.0.0.1:8000/transactions/');
        expect(global.fetch).toHaveBeenCalledTimes(3);
    });
});