import React from 'react';
import Button from '../components/common/Button';
import logo from '../assets/react.svg';
import '../styles/HomePage.css';

const HomePage = ({ onNavigate }) => {
    return (
        <div className="home-container">
            <img src={logo} alt="Logo SIGMA" className="home-logo" />
            <h1>Bem-vindo ao SIGMA</h1>
            <p>Inteligência colaborativa para cidades mais seguras.</p>
            <div className="button-group">
                <Button onClick={() => onNavigate('cidadao')}>Reportar Ocorrência</Button>
                <Button onClick={() => onNavigate('gestor')} variant="secondary">Painel do Gestor</Button>
            </div>
        </div>
    );
};

export default HomePage;