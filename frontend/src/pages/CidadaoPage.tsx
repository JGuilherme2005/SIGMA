import React, { useState } from 'react';
import { createAlerta } from '../api/apiService';
import Button from '../components/common/Button';
import Spinner from '../components/common/Spinner';
import Header from '../components/Header';
import '../styles/CidadaoPage.css';

const CidadaoPage = ({ onNavigate }) => {
    const [formData, setFormData] = useState({ tipo: 'Segurança', descricao: '' });
    const [status, setStatus] = useState({ loading: false, error: null, success: false });

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setStatus({ loading: true, error: null, success: false });

        // Pega a geolocalização do usuário (funcionalidade real!)
        navigator.geolocation.getCurrentPosition(
            async (position) => {
                const { latitude, longitude } = position.coords;
                const payload = { ...formData, latitude, longitude };

                try {
                    await createAlerta(payload);
                    setStatus({ loading: false, error: null, success: true });
                    setFormData({ tipo: 'Segurança', descricao: '' });
                    setTimeout(() => setStatus({ loading: false, error: null, success: false }), 3000); // Reseta a mensagem de sucesso
                } catch (err) {
                    setStatus({ loading: false, error: 'Falha ao enviar o alerta. Tente novamente.', success: false });
                }
            },
            (error) => {
                console.error("Erro de Geolocalização:", error);
                setStatus({ loading: false, error: 'Não foi possível obter sua localização. Por favor, habilite a permissão no navegador.', success: false });
            }
        );
    };

    return (
        <div className="page-container">
            <Header onNavigate={onNavigate} />
            <main className="cidadao-content">
                <form onSubmit={handleSubmit} className="alerta-form">
                    <h2>Reportar uma Nova Ocorrência</h2>
                    <p>Sua contribuição é anônima e segura.</p>

                    {status.error && <div className="message error">{status.error}</div>}
                    {status.success && <div className="message success">Alerta enviado com sucesso! Agradecemos sua colaboração.</div>}

                    <div className="form-group">
                        <label htmlFor="tipo">Tipo de Ocorrência</label>
                        <select id="tipo" name="tipo" value={formData.tipo} onChange={handleChange} required>
                            <option value="Segurança">Segurança (Assalto, Vandalismo)</option>
                            <option value="Infraestrutura">Infraestrutura (Buraco, Esgoto)</option>
                            <option value="Iluminação">Iluminação (Poste Queimado)</option>
                            <option value="Risco">Risco (Fio Solto, Desabamento)</option>
                        </select>
                    </div>
                    <div className="form-group">
                        <label htmlFor="descricao">Descreva em detalhes</label>
                        <textarea id="descricao" name="descricao" rows="5" value={formData.descricao} onChange={handleChange} placeholder="Ex: Há um poste com a lâmpada piscando e fios soltos na esquina da Rua Principal com a Av. Secundária." required />
                    </div>

                    <div className="form-actions">
                        {status.loading ? <Spinner /> : <Button type="submit" disabled={status.loading}>Enviar Alerta</Button>}
                    </div>
                </form>
            </main>
        </div>
    );
};

export default CidadaoPage;