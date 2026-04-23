import React, { useRef, useEffect, useState } from 'react';
import './CertificateModal.css';

const DOMAINS = [
    { icon: '🎣', label: 'Phishing Frenzy' },
    { icon: '🔑', label: 'Password Protector' },
    { icon: '🦠', label: 'Malware Mayhem' },
    { icon: '🛡️', label: 'Firewall Defender' },
    { icon: '🕵️', label: 'Scam Spotter' },
];

export default function CertificateModal({ isOpen, onClose, userName, date, userId }) {
    const certificateRef = useRef(null);
    const [revealed, setRevealed] = useState(false);

    // Animate on open + auto-save to DB
    useEffect(() => {
        if (isOpen) {
            setRevealed(false);
            const t = setTimeout(() => setRevealed(true), 100);

            // Save certificate to user's MongoDB profile
            if (userId) {
                const seed = (userName || '') + (date || '');
                let hash = 0;
                for (let i = 0; i < seed.length; i++) {
                    hash = ((hash << 5) - hash) + seed.charCodeAt(i);
                    hash |= 0;
                }
                const certId = `CD-CERT-${Math.abs(hash).toString(16).toUpperCase()}-${new Date().getFullYear()}`;
                const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:5000";
                fetch(`${API_BASE_URL}/user/save-certificate`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ user_id: userId, certificate_id: certId, issue_date: date || new Date().toLocaleDateString() })
                }).catch(e => console.error('Certificate save failed', e));
            }

            return () => clearTimeout(t);
        }
    }, [isOpen, userId, userName, date]);

    const handlePrint = () => window.print();

    const handleShare = () => {
        const text = `🏆 I just earned my CyberDuo Certified Operative certificate! I completed 375 elite missions across 5 cybersecurity domains. #CyberDuo #CyberSecurity`;
        if (navigator.share) {
            navigator.share({ title: 'CyberDuo Certificate', text });
        } else {
            navigator.clipboard.writeText(text);
            alert('Share text copied to clipboard!');
        }
    };

    if (!isOpen) return null;

    // Generate a unique Certificate ID based on name + date
    const generateCID = () => {
        const seed = (userName || '') + (date || '');
        let hash = 0;
        for (let i = 0; i < seed.length; i++) {
            hash = ((hash << 5) - hash) + seed.charCodeAt(i);
            hash |= 0;
        }
        return `CD-CERT-${Math.abs(hash).toString(16).toUpperCase()}-${new Date().getFullYear()}`;
    };

    const certId = generateCID();

    return (
        <div className="cert-overlay" onClick={onClose}>
            <div className={`cert-modal-content ${revealed ? 'cert-revealed' : ''}`} onClick={e => e.stopPropagation()}>
                <button className="cert-close-btn" onClick={onClose}>✕</button>

                <div id="printable-certificate" className="cert-frame" ref={certificateRef}>
                    {/* Corner decorations */}
                    <div className="cert-corner cert-corner-tl" />
                    <div className="cert-corner cert-corner-tr" />
                    <div className="cert-corner cert-corner-bl" />
                    <div className="cert-corner cert-corner-br" />

                    <div className="cert-inner-border">
                        <div className="cert-content">
                            {/* Header */}
                            <div className="cert-header">
                                <div className="cert-logo-container">
                                    <svg viewBox="0 0 32 32" fill="none" className="cert-logo">
                                        <path d="M16 2L4 8v8c0 7.18 5.15 13.88 12 15.47C22.85 29.88 28 23.18 28 16V8L16 2z"
                                            stroke="#00FF9D" strokeWidth="1.5" fill="rgba(0,255,157,0.05)" />
                                        <text x="16" y="20" textAnchor="middle" fontSize="9"
                                            fontFamily="Orbitron" fill="#00FF9D" fontWeight="700">CD</text>
                                    </svg>
                                </div>
                                <div className="cert-academy-name">CYBERDUO ACADEMY</div>
                                <div className="cert-division">COMMAND &amp; OPERATIONAL SECURITY DIVISION</div>
                            </div>

                            {/* Title */}
                            <div className="cert-title-container">
                                <h1 className="cert-main-title">OPERATIVE COMMENDATION</h1>
                                <h2 className="cert-sub-title">CERTIFICATE OF MASTERY</h2>
                            </div>

                            {/* Body */}
                            <div className="cert-body">
                                <p className="cert-intro">THIS DOCUMENT OFFICIALLY RECOGNIZES THAT</p>
                                <div className="cert-user-name">{userName || 'RECRUIT #99'}</div>
                                <p className="cert-accomplishment">
                                    Has successfully completed all <strong>375 elite missions</strong> spanning
                                    <strong> 5 cybersecurity domains</strong> across Beginner, Intermediate, and Elite Hard tiers.
                                    By demonstrating mastery in threat detection, digital forensics, and cyber defense strategy,
                                    this operative is hereby granted the title of:
                                </p>

                                {/* Domain Badges */}
                                <div className="cert-domains">
                                    {DOMAINS.map(d => (
                                        <div key={d.label} className="cert-domain-badge">
                                            <span>{d.icon}</span>
                                            <span>{d.label}</span>
                                        </div>
                                    ))}
                                </div>

                                <div className="cert-rank">⚜️ CYBERDUO CERTIFIED ELITE OPERATIVE ⚜️</div>
                            </div>

                            {/* Footer */}
                            <div className="cert-footer">
                                <div className="cert-signature-row">
                                    <div className="cert-sig-box">
                                        <div className="cert-sig-handwriting">C.D. Cyber</div>
                                        <div className="cert-sig-line" />
                                        <div className="cert-sig-label">ACADEMY DIRECTOR</div>
                                    </div>
                                    <div className="cert-seal">
                                        <div className="cert-seal-outer">
                                            <div className="cert-seal-inner">
                                                <span>VERIFIED</span>
                                            </div>
                                        </div>
                                    </div>
                                    <div className="cert-sig-box cert-sig-box--right">
                                        <div className="cert-date">{date || new Date().toLocaleDateString()}</div>
                                        <div className="cert-sig-line" />
                                        <div className="cert-sig-label">DATE OF ISSUE</div>
                                    </div>
                                </div>

                                <div className="cert-id-badge">
                                    CERTIFICATE ID: <span className="cert-id-value">{certId}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Action Buttons */}
                <div className="cert-actions">
                    <button className="cert-btn-print" onClick={handlePrint}>
                        🖨️ DOWNLOAD / PRINT
                    </button>
                    <button className="cert-btn-share" onClick={handleShare}>
                        🔗 SHARE ACHIEVEMENT
                    </button>
                </div>
                <p className="cert-hint">Tip: Set "Layout: Landscape" and "Background Graphics: ON" in print settings for the best result.</p>
            </div>
        </div>
    );
}
