import React, { useState, useEffect } from 'react';
import '../styles/CyberAlert.css';
import localAlertsData from '../data/CyberAlert.json';

export default function CyberAlert({ compact = false }) {
    const [chatOpen, setChatOpen] = useState(false);
    const [chatMessages, setChatMessages] = useState([]);
    const [chatInput, setChatInput] = useState('');
    const [chatLoading, setChatLoading] = useState(false);

    const [alertsData, setAlertsData] = useState(localAlertsData); // ✅ Local-First Initialization

    const GEMINI_API_KEY = import.meta.env.VITE_GEMINI_API_KEY;

    // ... inside component:
    useEffect(() => {
        // Use newsdata.io API or fallback to our local data if the key is broken
        const API_BASE_URL = "http://localhost:5000";
        const fetchUrl = `${API_BASE_URL}/user/alerts/news`;

        if (!fetchUrl) {
            setAlertsData(localAlertsData);
            return;
        }

        fetch(fetchUrl)
            .then(res => res.json())
            .then(data => {
                // Handle the backend relay response which now matches NewsData structure
                if (!data || data.status === 'error' || !data.results) {
                    console.error("News Relay Error or No Results:", data?.results?.message || "Check Backend Logs");
                    // Keep existing localAlertsData initialization
                    return;
                }

                // STRICT Client-Side filtering to drop irrelevant news (e.g. general arrests, politics)
                const validKeywords = ['cyber', 'hacker', 'phishing', 'malware', 'scam', 'fraud', 'breach', 'ransomware', 'digital arrest', 'otp', 'online', 'deepfake'];
                const filteredResults = data.results.filter(article => {
                    const text = ((article.title || "") + " " + (article.description || "")).toLowerCase();
                    return validKeywords.some(kw => text.includes(kw));
                });

                const formatted = filteredResults.slice(0, 8).map((article, index) => {
                    const text = ((article.title || "") + " " + (article.description || "")).toLowerCase();
                    
                    let score = 4 + Math.floor(Math.random() * 2); // base 4-5
                    let domains = [];
                    let riskFactors = [];

                    if (text.includes("phishing") || text.includes("link") || text.includes("spoof") || text.includes("fake website") || text.includes("impersonat")) {
                        score += 3;
                        domains.push({ name: "Phishing Frenzy", percent: 80 + Math.floor(Math.random() * 15) });
                        riskFactors.push({ factor: "Deceptive Links/Messages", points: "+3 Risk" });
                    }
                    if (text.includes("malware") || text.includes("virus") || text.includes("ransomware") || text.includes("trojan") || text.includes("spyware")) {
                        score += 4;
                        domains.push({ name: "Malware Mayhem", percent: 75 + Math.floor(Math.random() * 20) });
                        riskFactors.push({ factor: "Malicious Software", points: "+4 Risk" });
                    }
                    if (text.includes("password") || text.includes("breach") || text.includes("leak") || text.includes("hack") || text.includes("data loss")) {
                        score += 3;
                        domains.push({ name: "Password Protector", percent: 70 + Math.floor(Math.random() * 20) });
                        riskFactors.push({ factor: "Data/Credential Compromise", points: "+3 Risk" });
                    }
                    if (text.includes("scam") || text.includes("fraud") || text.includes("financial") || text.includes("steal") || text.includes("cyber cell")) {
                        score += 2;
                        domains.push({ name: "Scam Spotter", percent: 85 + Math.floor(Math.random() * 10) });
                        riskFactors.push({ factor: "Cyber Identity/Financial Fraud", points: "+2 Risk" });
                    }

                    if (domains.length === 0) {
                        domains.push({ name: "Firewall Defender", percent: 60 + Math.floor(Math.random() * 20) });
                        riskFactors.push({ factor: "General Cyber Threat", points: "+1 Risk" });
                    }

                    score = Math.min(10, score);
                    let riskLevel = "medium";
                    if (score >= 8) riskLevel = "high";
                    else if (score >= 5) riskLevel = "medium";
                    else riskLevel = "low";

                    // Smart Date Logic for Tactical Feel
                    const rawDate = article.pubDate?.split(" ")[0] || new Date().toISOString().split("T")[0];
                    const todayStr = new Date().toISOString().split("T")[0];
                    const yesterday = new Date();
                    yesterday.setDate(yesterday.getDate() - 1);
                    const yesterdayStr = yesterday.toISOString().split("T")[0];

                    let displayDate = rawDate;
                    if (rawDate === todayStr) displayDate = "TODAY";
                    else if (rawDate === yesterdayStr) displayDate = "YESTERDAY";

                    return {
                        id: index,
                        date: displayDate,
                        rawDate: rawDate,
                        headline: article.title,
                        description: article.description || "Click the article link for more information about this cyber alert.",
                        riskLevel: riskLevel,
                        riskMeter: score,
                        riskFactors: riskFactors,
                        domains: domains
                    };
                });
                // If it returned empty array, use local
                if (formatted.length === 0) {
                    setAlertsData(localAlertsData);
                } else {
                    setAlertsData(formatted);
                }
            })
            .catch(err => {
                console.log("Fetch failed, using local data", err);
                setAlertsData(localAlertsData);
            });
    }, []);

    const handleAskAIClick = () => {
        setChatOpen(true);
    };

    const handleChatSend = async () => {
        if (!chatInput.trim() || chatLoading) return;
        const userMsg = { role: 'user', text: chatInput };
        setChatMessages(prev => [...prev, userMsg]);
        const currentQuestion = chatInput;
        setChatInput('');
        setChatLoading(true);
        try {
            const response = await fetch(
                `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${GEMINI_API_KEY}`,
                {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        contents: [{
                            parts: [{
                                text: `You are an expert AI assistant specializing in cybersecurity and cyber attacks. The user asks: "${currentQuestion}". Give a helpful, accurate, and concise answer in 2-4 sentences maximum.`
                            }]
                        }]
                    })
                }
            );
            const data = await response.json();
            if (data.candidates && data.candidates[0] && data.candidates[0].content) {
                const reply = data.candidates[0].content.parts[0].text;
                setChatMessages(prev => [...prev, { role: 'ai', text: reply }]);
            } else if (data.error) {
                setChatMessages(prev => [...prev, { role: 'ai', text: `Error: ${data.error.message}` }]);
            } else {
                setChatMessages(prev => [...prev, { role: 'ai', text: 'Sorry, I could not get a response. Please try again.' }]);
            }
        } catch (err) {
            setChatMessages(prev => [...prev, { role: 'ai', text: 'Sorry, I could not connect. Please check your internet connection.' }]);
        }
        setChatLoading(false);
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
        const latest = alertsData[0];
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

            {chatOpen && (
                <div className="gs-modal-overlay" onClick={() => setChatOpen(false)} style={{ position: 'fixed', top: 0, left: 0, width: '100%', height: '100%', background: 'rgba(0,0,0,0.8)', display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 9999 }}>
                    <div className="gs-modal-content" style={{ width: '600px', maxHeight: '80vh', height: '600px', display: 'flex', flexDirection: 'column', background: '#0a0a1a', padding: '30px', borderRadius: '15px', border: '1px solid #00FF9D' }} onClick={e => e.stopPropagation()}>
                        <h3 style={{ color: '#00FF9D', margin: '0 0 20px 0', fontSize: '1.8rem', textAlign: 'center' }}>🤖 CyberSec AI Assistant</h3>
                        <div style={{ flex: 1, overflowY: 'auto', marginBottom: '15px', padding: '15px', background: 'rgba(0,0,0,0.5)', borderRadius: '8px' }}>
                            {chatMessages.length === 0 && (
                                <p style={{ color: 'rgba(255,255,255,0.5)', textAlign: 'center', fontSize: '1.1rem', marginTop: '20px' }}>Ask me anything about cybersecurity, threats, or the latest alerts!</p>
                            )}
                            {chatMessages.map((msg, i) => (
                                <div key={i} style={{ marginBottom: '10px', textAlign: msg.role === 'user' ? 'right' : 'left' }}>
                                    <span style={{
                                        background: msg.role === 'user' ? '#00FF9D' : '#1a1a2e',
                                        color: msg.role === 'user' ? '#000' : '#fff',
                                        padding: '12px 18px',
                                        borderRadius: '12px',
                                        display: 'inline-block',
                                        maxWidth: '85%',
                                        fontSize: '1.1rem',
                                        lineHeight: '1.5',
                                        border: msg.role === 'ai' ? '1px solid rgba(0, 255, 157, 0.2)' : 'none'
                                    }}>{msg.text}</span>
                                </div>
                            ))}
                            {chatLoading && (
                                <div style={{ textAlign: 'left', marginTop: '10px' }}>
                                    <span style={{ color: '#00FF9D', fontSize: '1.1rem' }}>AI is analyzing threat data... ⏳</span>
                                </div>
                            )}
                        </div>
                        <div style={{ display: 'flex', gap: '10px', marginTop: '10px' }}>
                            <input
                                type="text"
                                value={chatInput}
                                onChange={e => setChatInput(e.target.value)}
                                onKeyDown={e => e.key === 'Enter' && handleChatSend()}
                                placeholder="Ask about phishing, malware..."
                                style={{ flex: 1, padding: '15px', borderRadius: '8px', border: '1px solid #00FF9D', background: '#0a0a1a', color: '#fff', fontSize: '1.1rem' }}
                            />
                            <button onClick={handleChatSend} disabled={chatLoading}
                                style={{ padding: '0 30px', background: chatLoading ? '#555' : '#00FF9D', color: '#000', border: 'none', borderRadius: '8px', cursor: chatLoading ? 'not-allowed' : 'pointer', fontWeight: 'bold', fontSize: '1.2rem' }}>
                                SEND
                            </button>
                        </div>
                        <button onClick={() => setChatOpen(false)} style={{ marginTop: '20px', padding: '15px', background: 'transparent', color: '#fff', border: '1px solid rgba(255,255,255,0.3)', borderRadius: '8px', cursor: 'pointer', transition: '0.3s', fontSize: '1.1rem' }}>CLOSE</button>
                    </div>
                </div>
            )}
        </div>
    );
}