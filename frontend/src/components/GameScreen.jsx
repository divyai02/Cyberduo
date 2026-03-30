import React from 'react';

export default function GameScreen({ gameName, level, difficulty, onBack }) {
    return (
        <div style={{ padding: '40px', textAlign: 'center', color: '#fff', fontFamily: '"Exo 2", sans-serif' }}>
            <h1 style={{ color: '#00FF9D', fontSize: '48px', marginBottom: '10px', fontFamily: 'Orbitron, sans-serif' }}>
                {gameName}
            </h1>
            <h2 style={{ color: 'rgba(255,255,255,0.7)', fontSize: '24px', marginBottom: '40px', fontFamily: '"Share Tech Mono", monospace' }}>
                LEVEL: {level.toUpperCase()} | DIFFICULTY: {difficulty.toUpperCase()}
            </h2>
            
            <div style={{ 
                border: '2px dashed rgba(0,255,157,0.5)', 
                borderRadius: '24px', 
                padding: '60px', 
                background: 'rgba(0,255,157,0.1)',
                display: 'inline-block',
                backdropFilter: 'blur(10px)'
            }}>
                <div style={{ fontSize: '64px', marginBottom: '20px' }}>🚧</div>
                <h3 style={{ fontSize: '28px', color: '#00FF9D', letterSpacing: '2px', fontFamily: 'Orbitron, sans-serif' }}>COMING SOON</h3>
                <p style={{ marginTop: '16px', color: 'rgba(255,255,255,0.6)', maxWidth: '400px' }}>
                    This module is currently under development. Check back later to test your cybersecurity skills!
                </p>
                
                {onBack && (
                    <button 
                        onClick={onBack}
                        style={{
                            marginTop: '32px',
                            padding: '12px 24px',
                            background: '#00FF9D',
                            color: '#0A0F1F',
                            border: 'none',
                            borderRadius: '8px',
                            cursor: 'pointer',
                            fontFamily: 'Orbitron, sans-serif',
                            fontWeight: 'bold',
                            fontSize: '16px',
                            transition: 'transform 0.2s, boxShadow 0.2s',
                        }}
                        onMouseOver={(e) => { e.target.style.transform = 'scale(1.05)'; e.target.style.boxShadow = '0 0 15px rgba(0,255,157,0.5)'; }}
                        onMouseOut={(e) => { e.target.style.transform = 'scale(1)'; e.target.style.boxShadow = 'none'; }}
                    >
                        BACK TO DASHBOARD
                    </button>
                )}
            </div>
        </div>
    );
}
