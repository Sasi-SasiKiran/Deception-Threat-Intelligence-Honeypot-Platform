import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import Navbar from './components/Navbar';
import Overview from './pages/Overview';
import LiveEvents from './pages/LiveEvents';
import AttackAnalysis from './pages/AttackAnalysis';
import IPAnalysis from './pages/IPAnalysis';
import Settings from './pages/Settings';

export default function App() {
  const [currentPage, setCurrentPage] = useState('overview');

  const pageTitles = {
    overview: 'Threat Intelligence Overview',
    'live-events': 'Real-Time Intercepted Events Feed',
    analysis: 'Adversary Behavior & Attack Vector Analysis',
    'ip-analysis': 'Attacker IP Intelligence & Indicators',
    settings: 'Platform Operations & Settings'
  };

  const renderPage = () => {
    switch (currentPage) {
      case 'overview':
        return <Overview />;
      case 'live-events':
        return <LiveEvents />;
      case 'analysis':
        return <AttackAnalysis />;
      case 'ip-analysis':
        return <IPAnalysis />;
      case 'settings':
        return <Settings />;
      default:
        return <Overview />;
    }
  };

  return (
    <div className="app-container">
      <Sidebar currentPage={currentPage} onNavigate={setCurrentPage} />
      <div className="main-content">
        <Navbar title={pageTitles[currentPage] || 'SOC Dashboard'} />
        <main className="page-wrapper">
          {renderPage()}
        </main>
      </div>
    </div>
  );
}
