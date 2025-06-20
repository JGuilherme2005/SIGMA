import axios from 'axios';

const API_URL = 'http://localhost:3000'; // URL do backend do seu colega
const USE_MOCK_DATA = false; // <<< MUDE PARA 'false' PARA USAR O BACKEND REAL

let mockAlertas = [
    { id: 1, tipo: 'Infraestrutura', descricao: 'Buraco gigante na Av. Faria Lima', latitude: -23.5779, longitude: -46.6853, prioridade: 'Média', equipe_sugerida: 'Prefeitura - Obras', timestamp: new Date().toISOString() },
    { id: 2, tipo: 'Risco', descricao: 'Fio de alta tensão solto perto da escola', latitude: -23.5505, longitude: -46.6333, prioridade: 'Crítica', equipe_sugerida: 'Defesa Civil + Eletropaulo', timestamp: new Date().toISOString() }
];

const api = axios.create({
    baseURL: API_URL,
});

export const getAlertas = () => {
    if (USE_MOCK_DATA) {
        console.warn("Usando dados FALSOS (mock) para alertas.");
        return Promise.resolve({ data: { data: mockAlertas } });
    }
    return api.get('/alertas');
};

export const createAlerta = (alertaData) => {
    if (USE_MOCK_DATA) {
        console.warn("Criando alerta FALSO (mock).");
        const newId = mockAlertas.length > 0 ? Math.max(...mockAlertas.map(a => a.id)) + 1 : 1;
        const newAlerta = {
            ...alertaData,
            id: newId,
            prioridade: 'Pendente',
            equipe_sugerida: 'IA Analisando...',
            timestamp: new Date().toISOString()
        };
        mockAlertas.push(newAlerta);
        return Promise.resolve({ data: { data: newAlerta } });
    }
    return api.post('/alertas', alertaData);
};