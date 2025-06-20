import React from 'react';
import { Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import './AlertaMarker.css';

// Ícones coloridos
const getIcon = (prioridade) => {
    const iconClass = `marker-icon-${prioridade ? prioridade.toLowerCase() : 'default'}`;
    return L.divIcon({
        className: `custom-div-icon`,
        html: `<div class='marker-pin ${iconClass}'></div><i class='material-icons'>place</i>`,
        iconSize: [30, 42],
        iconAnchor: [15, 42]
    });
};

const AlertaMarker = ({ alerta }) => {
    return (
        <Marker position={[alerta.latitude, alerta.longitude]} icon={getIcon(alerta.prioridade)}>
            <Popup>
                <div className="popup-content">
                    <h4>{alerta.tipo}</h4>
                    <p>{alerta.descricao}</p>
                    <div className="popup-details">
                        <span><strong>Prioridade:</strong> <span className={`prioridade-${alerta.prioridade?.toLowerCase()}`}>{alerta.prioridade}</span></span>
                        <span><strong>Equipe:</strong> {alerta.equipe_sugerida}</span>
                    </div>
                </div>
            </Popup>
        </Marker>
    );
};

export default AlertaMarker;