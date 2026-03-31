import React, { useState, useEffect } from 'react';
import '../styles/dailygoal.css';
import { getDailyStats } from '../utils/dailyprogress.js';

const DailyGoal = () => {
    const [stats, setStats] = useState(getDailyStats());

    useEffect(() => {
        const update = () => {
            const newStats = getDailyStats();
            setStats(newStats);
        };
        window.addEventListener('dailyGoalUpdated', update);
        window.addEventListener('xpUpdated', update);
        window.addEventListener('streakUpdated', update);
        return () => {
            window.removeEventListener('dailyGoalUpdated', update);
            window.removeEventListener('xpUpdated', update);
            window.removeEventListener('streakUpdated', update);
        };
    }, []);

    // Ensure we have a clean number for the progress
    const currentProgress = Number(stats.progress) || 0;
    const percentage = Math.round((currentProgress / 1) * 100);

    return (
        <div className="dg-page-container">
            <div className="dg-glass-layout">
                <header className="dg-page-header">
                    <div className="dg-title-block">
                        <h1 className="dg-main-title">DAILY MISSION LOG</h1>
                        <p className="dg-subtitle">OPERATIVE BASE // SECTOR 7-6</p>
                    </div>
                </header>

                <div className="dg-content-grid">
                    {/* Left Section: Gauge */}
                    <div className="dg-gauge-section">
                        <div className="dg-gauge-wrap">
                            <svg viewBox="0 0 100 100" className="dg-gauge-svg">
                                <circle className="dg-gauge-bg" cx="50" cy="50" r="45" fill="none" stroke="rgba(255,255,255,0.05)" strokeWidth="8" />
                                <circle 
                                    className="dg-gauge-path" 
                                    cx="50" cy="50" r="45" 
                                    fill="none"
                                    stroke="#00FF9D"
                                    strokeWidth="8"
                                    strokeLinecap="round"
                                    style={{ 
                                        strokeDasharray: '283',
                                        strokeDashoffset: Math.max(0, 283 - (283 * Math.min(percentage, 100)) / 100) 
                                    }}
                                />
                            </svg>
                            <div className="dg-gauge-info">
                                <div className="dg-gauge-top-val">{currentProgress}</div>
                                <div className="dg-gauge-bot-val">OF 1 LEVEL</div>
                            </div>
                        </div>
                    </div>

                    {/* Right Section: Objective Intel */}
                    <div className="dg-intel-section">
                        <div className="dg-intel-card">
                            <h3 className="dg-progress-desc">
                                Goal Status: {currentProgress} / 1 module completed
                            </h3>
                            
                            <div className="dg-reward-glow-panel">
                                <span className={`dg-reward-text ${stats.isReached ? 'claimed' : 'pending'}`}>
                                    {stats.isReached ? "REWARD CLAIMED" : "+20 XP BONUS PENDING"}
                                </span>
                            </div>

                            <div className="dg-progress-lane">
                                <div className="dg-lane-fill" style={{ width: `${Math.min(percentage, 100)}%` }}></div>
                            </div>

                            <button className="dg-btn-action" onClick={() => window.location.hash = '#home'}>
                                LAUNCH MISSION PATH
                            </button>
                        </div>

                        <footer className="dg-footer-stats">
                            <div className="dg-footer-stat">
                                <span className="dg-fstat-val">{stats.streak} DAYS</span>
                                <span className="dg-fstat-lbl">STREAK</span>
                            </div>
                            <div className="dg-footer-stat">
                                <span className="dg-fstat-val">+{stats.totalXP} TOTAL XP</span>
                            </div>
                        </footer>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default DailyGoal;
