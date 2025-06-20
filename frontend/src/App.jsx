import React, { useState } from 'react';
import HomePage from './pages/HomePage';
import CidadaoPage from './pages/CidadaoPage';
import GestorPage from './pages/GestorPage';
import './styles/App.css';

function App() {
  const [currentPage, setCurrentPage] = useState('home');

  const renderPage = () => {
    switch (currentPage) {
      case 'cidadao':
        return <CidadaoPage onNavigate={setCurrentPage} />;
      case 'gestor':
        return <GestorPage onNavigate={setCurrentPage} />;
      default:
        return <HomePage onNavigate={setCurrentPage} />;
    }
  };

  return <div className="App">{renderPage()}</div>;
}

export default App;