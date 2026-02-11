import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import TransactionList from '../TransactionList';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import React from 'react';

// Données fictives pour le test
const MOCK_TRANSACTIONS = [
    { date: '2026-01-01', label: 'Cinéma', amount: 12.5, category: 'Loisirs', type: 'DEPENSE' },
    { date: '2026-01-02', label: 'Salaire', amount: 2000, category: 'Travail', type: 'REVENU' },
    { date: '2026-01-03', label: 'Courses', amount: 50, category: 'Alimentation', type: 'DEPENSE' }
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
});