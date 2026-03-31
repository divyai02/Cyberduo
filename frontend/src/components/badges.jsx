import React, { useState, useEffect } from 'react';
import '../styles/badges.css';
import badgesData from '../data/badges.json';

const Badges = () => {
    const [earnedBadges, setEarnedBadges] = useState([]);

    useEffect(() => {
        const loadBadges = () => {
            const stored = localStorage.getItem('cyberduo_earned_badges');
            if (stored) {
                setEarnedBadges(JSON.parse(stored));
            }
        };

        loadBadges();
        window.addEventListener('badgeUnlocked', loadBadges);
        return () => window.removeEventListener('badgeUnlocked', loadBadges);
    }, []);

    const isEarned = (id) => earnedBadges.includes(id);

    return (
        <div className="badges-page-container">
            <header className="badges-page-header">
                <div className="badges-page-title-wrap">
                    <h1 className="badges-page-title">HALL OF ACHIEVEMENTS</h1>
                    <p className="badges-page-subtitle">Your journey through the CyberDuo Academy</p>
                </div>
                <div className="badges-page-stats">
                    <div className="badges-stat-card">
                        <span className="badges-stat-value">{earnedBadges.length}</span>
                        <span className="badges-stat-label">BADGES UNLOCKED</span>
                    </div>
                    <div className="badges-stat-card">
                        <span className="badges-stat-value">{Math.round((earnedBadges.length / badgesData.length) * 100)}%</span>
                        <span className="badges-stat-label">COMPLETION</span>
                    </div>
                </div>
            </header>
            
            <div className="badges-main-grid">
                {badgesData.map((badge) => (
                    <div className={`badge-card ${isEarned(badge.id) ? 'earned' : 'locked'}`} key={badge.id}>
                        <div className="badge-card-inner">
                            <div className="badge-card-front">
                                <div className="badge-icon-wrap">
                                    <span className="badge-emoji">{badge.icon}</span>
                                    {!isEarned(badge.id) && <div className="badge-lock-seal">🔒</div>}
                                </div>
                                <h3 className="badge-name">{badge.name}</h3>
                                <div className="badge-status-chip">
                                    {isEarned(badge.id) ? 'UNLOCKED' : 'CLASSIFIED'}
                                </div>
                            </div>
                            <div className="badge-card-back">
                                <h4 className="badge-back-title">{badge.name}</h4>
                                <p className="badge-back-desc">{badge.description}</p>
                                <div className="badge-condition">
                                    <span className="badge-condition-label">REQ:</span>
                                    <span className="badge-condition-text">{badge.conditionType.replace(/([A-Z])/g, ' $1').toUpperCase()} {badge.conditionValue}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Badges;
