import React from 'react';
import logo from '../assets/react.svg';
import '../styles/Header.css';

const Header = ({ onNavigate }) => {
    return (
        <header className="app-header">
            <div className="header-content">
                <img src={logo} alt="SIGMA Logo" className="header-logo" onClick={() => onNavigate('home')} />
                <span className="header-title" onClick={() => onNavigate('home')}>SIGMA</span>
            </div>
        </header>
    );
};

export default Header;