import { useState, useEffect, useCallback } from 'react';
import { getAlertas } from '../api/apiService';

export const useAlertas = () => {
    const [alertas, setAlertas] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchAlertas = useCallback(async () => {
        try {
            setLoading(true);
            setError(null);
            const response = await getAlertas();
            setAlertas(response.data.data || []);
        } catch (err) {
            setError('Não foi possível carregar os alertas.');
            console.error(err);
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchAlertas();
        const intervalId = setInterval(fetchAlertas, 5000); // Atualiza a cada 5s
        return () => clearInterval(intervalId);
    }, [fetchAlertas]);

    return { alertas, loading, error, refetch: fetchAlertas };
};