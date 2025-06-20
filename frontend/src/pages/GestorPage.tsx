import React from 'react';
import { MapContainer, TileLayer } from 'react-leaflet';
import { useAlertas } from '../hooks/useAlertas';
import Header from '../components/Header';
import AlertaMarker from '../components/AlertaMarker';
import Spinner from '../components/common/Spinner';
import '../styles/GestorPage.css';

const GestorPage = ({ onNavigate }) => {
    const { alertas, loading, error } = useAlertas();
    const position = [-23.5505, -46.6333]; // Centro do mapa

    return (
        <div className="page-container gestor-page">
            <Header onNavigate={onNavigate} />
            <main className="gestor-content">
                {loading && alertas.length === 0 && <div className="loading-overlay"><Spinner /></div>}
                {error && <div className="error-overlay">{error}</div>}
                <MapContainer center={position} zoom={12} scrollWheelZoom={true}>
                    <TileLayer
                        attribution='© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    />
                    {alertas.map(alerta => (
                        <AlertaMarker key={alerta.id} alerta={alerta} />
                    ))}
                </MapContainer>
            </main>
        </div>
    );
};

export default GestorPage;