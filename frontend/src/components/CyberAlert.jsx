import React from 'react';
import '../styles/CyberAlert.css';
import alertsData from '../data/CyberAlert.json';

export default function CyberAlert({ compact = false }) {
    const handleAskAIClick = (headline) => {
        alert("AI Chat coming soon. Backend integration in progress.");
    };

    const getRiskColorClass = (level) => {
        switch (level.toLowerCase()) {
            case 'high': return 'ca-high-risk';
            case 'medium': return 'ca-medium-risk';
            case 'low': return 'ca-low-risk';
            default: return 'ca-medium-risk';
        }
    };

    const renderFancyMeter = (score, level) => {
        const blocks = [];
        const colorClass = getRiskColorClass(level);
        for (let i = 1; i <= 10; i++) {
            const isActive = i <= score;
            blocks.push(
                <div 
                    key={i} 
                    className={`ca-meter-segment ${isActive ? 'active ' + colorClass : ''}`}
                ></div>
            );
        }
        return blocks;
    };

    const renderDomainCircle = (name, percent) => {
        const radius = 32;
        const circumference = 2 * Math.PI * radius;
        const strokeDashoffset = circumference - (percent / 100) * circumference;
        return (
            <div className="ca-domain-circle-wrap" key={name}>
                <svg className="ca-domain-svg" width="76" height="76">
                    <circle className="ca-domain-bg" cx="38" cy="38" r={radius} />
                    <circle 
                        className="ca-domain-progress" 
                        cx="38" cy="38" r={radius} 
                        strokeDasharray={circumference} 
                        strokeDashoffset={strokeDashoffset} 
                    />
                </svg>
                <div className="ca-domain-percent">{percent}%</div>
                <div className="ca-domain-name">{name}</div>
            </div>
        );
    };

    if (compact) {
        const latest = alertsData[0]; // Assume first is most recent
        if (!latest) return null;
        return (
            <div className="ca-card compact">
                <div className="ca-card-header">
                    <span className="ca-date">{latest.date}</span>
                    <div className={`ca-risk-label ${getRiskColorClass(latest.riskLevel)}`}>
                        {latest.riskLevel.toUpperCase()} RISK
                    </div>
                </div>
                <h2 className="ca-headline" style={{ fontSize: '0.9rem' }}>📰 {latest.headline}</h2>
                <div className="ca-rm-fancy-bar" style={{ marginTop: '10px' }}>
                    {renderFancyMeter(latest.riskMeter, latest.riskLevel)}
                </div>
            </div>
        );
    }

    return (
        <div className="ca-container">
            <div className="ca-header">
                <h1 className="ca-main-title">CYBER ALERTS</h1>
                <p className="ca-subtitle">Real India News with Risk Meter Analysis</p>
            </div>

            <div className="ca-list-wrapper">
                {alertsData.map((alert, index) => (
                    <div className="ca-card" key={alert.id || index}>
                        
                        <div className="ca-card-header">
                            <span className="ca-date">{alert.date}</span>
                            <div className={`ca-risk-label ${getRiskColorClass(alert.riskLevel)}`}>
                                {alert.riskLevel.toUpperCase()} RISK
                            </div>
                        </div>

                        <h2 className="ca-headline">📰 {alert.headline}</h2>
                        <p className="ca-description">{alert.description}</p>

                        <div className="ca-risk-section">
                            <div className="ca-risk-meter-container">
                                <div className="ca-rm-header">
                                    <span className="ca-rm-title">Risk Level Analysis:</span>
                                    <span className={`ca-rm-score ${getRiskColorClass(alert.riskLevel)}`}>
                                        {alert.riskMeter}/10
                                    </span>
                                </div>
                                <div className="ca-rm-fancy-bar">
                                    {renderFancyMeter(alert.riskMeter, alert.riskLevel)}
                                </div>
                            </div>

                            {alert.riskFactors && alert.riskFactors.length > 0 && (
                                <div className="ca-factors">
                                    <span className="ca-factors-title">Risk Factors:</span>
                                    <ul className="ca-factors-list">
                                        {alert.riskFactors.map((rf, idx) => (
                                            <li key={idx}>
                                                <span className="ca-factor-text">{rf.factor}</span>
                                                <span className="ca-factor-points">{rf.points}</span>
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            )}

                            {alert.domains && alert.domains.length > 0 && (
                                <div className="ca-domains-section">
                                    <span className="ca-factors-title">Game Domains Involved:</span>
                                    <div className="ca-domains-row">
                                        {alert.domains.map(d => renderDomainCircle(d.name, d.percent))}
                                    </div>
                                </div>
                            )}
                        </div>

                    </div>
                ))}
            </div>
            
            <button className="ca-floating-ai-btn" onClick={() => handleAskAIClick('General')}>
                <div className="ca-ai-icon">💬</div>
                <span>Ask AI Assistant</span>
                <div className="ca-ai-pulse"></div>
            </button>
        </div>
    );
}
