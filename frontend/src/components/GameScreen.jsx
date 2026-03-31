import React, { useState, useEffect } from 'react';
import '../styles/gamescreen.css';
import gameData from '../data/GameQuestions.json';
import { updateStreak } from '../utils/gameProgress.js';

export default function GameScreen({ gameKey = "phishing", gameName, level, onComplete, onProgressUpdate, onBack }) {
    const questions = gameData[gameKey]?.[level] || [];
    
    const [currentIndex, setCurrentIndex] = useState(() => {
        const saved = localStorage.getItem(`cyberduo_inprogress_${gameKey}_${level}`);
        return saved ? JSON.parse(saved).currentIndex : 0;
    });
    const [score, setScore] = useState(() => {
        const saved = localStorage.getItem(`cyberduo_inprogress_${gameKey}_${level}`);
        return saved ? JSON.parse(saved).score : 0;
    });
    const [xp, setXp] = useState(() => {
        const saved = localStorage.getItem(`cyberduo_inprogress_${gameKey}_${level}`);
        return saved ? JSON.parse(saved).xp : 0;
    });
    const [highestCompletedIndex, setHighestCompletedIndex] = useState(() => {
        const saved = localStorage.getItem(`cyberduo_inprogress_${gameKey}_${level}`);
        if (!saved) return -1;
        const parsed = JSON.parse(saved);
        return parsed.highestCompletedIndex !== undefined ? parsed.highestCompletedIndex : parsed.currentIndex - 1;
    });
    const [feedback, setFeedback] = useState(null);
    
    useEffect(() => {
        if (currentIndex > 0 || score > 0 || xp > 0 || highestCompletedIndex > -1) {
            localStorage.setItem(`cyberduo_inprogress_${gameKey}_${level}`, JSON.stringify({
                currentIndex, score, xp, highestCompletedIndex
            }));
        }
        if (onProgressUpdate) {
            onProgressUpdate(highestCompletedIndex + 1);
        }
    }, [currentIndex, score, xp, highestCompletedIndex, gameKey, level]);
    
    const [timeLeft, setTimeLeft] = useState(45);
    const [hasAnswered, setHasAnswered] = useState(false);
    const [isCorrectResult, setIsCorrectResult] = useState(null);
    
    const [selectedOption, setSelectedOption] = useState(null);
    const [droppedFlags, setDroppedFlags] = useState([]);
    const [checkedFlags, setCheckedFlags] = useState([]);
    const [showHover, setShowHover] = useState(false);
    const [triageAnswers, setTriageAnswers] = useState({});
    const [buildAnswers, setBuildAnswers] = useState({ lure: null, urgency: null });
    const [switchActive, setSwitchActive] = useState(false);
    const [sequenceList, setSequenceList] = useState([]);

    const [modal, setModal] = useState({ show: false, title: '', content: '' });

    // ✅ AI CHAT STATES
    const [chatOpen, setChatOpen] = useState(false);
    const [chatMessages, setChatMessages] = useState([]);
    const [chatInput, setChatInput] = useState('');
    const [chatLoading, setChatLoading] = useState(false);

    const GEMINI_API_KEY = "AIzaSyAfAUhkJSnr7eUo90DV_xITKl8gFqEB5E0";

    // ✅ AI CHAT FUNCTION
    const handleChatSend = async () => {
        if (!chatInput.trim() || chatLoading) return;
        const userMsg = { role: 'user', text: chatInput };
        setChatMessages(prev => [...prev, userMsg]);
        const currentQuestion = chatInput;
        setChatInput('');
        setChatLoading(true);
        try {
            const response = await fetch(
                `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent?key=${GEMINI_API_KEY}`,
                {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        contents: [{
                            parts: [{
                                text: `You are a friendly cybersecurity tutor in a game called CyberDuo. The current game question is about: "${currentQ?.questionText}". The student asks: "${currentQuestion}". Give a helpful, simple answer in 2-3 sentences maximum.`
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

    const currentQ = questions[currentIndex];
    
    useEffect(() => {
        if (currentQ?.format === 'sequence_builder' && currentQ.steps && sequenceList.length === 0 && !hasAnswered) {
            setSequenceList([...currentQ.steps].sort(() => Math.random() - 0.5));
        }
    }, [currentQ, sequenceList.length, hasAnswered]);

    useEffect(() => {
        if (hasAnswered || currentIndex >= questions.length || !currentQ) return;
        if (timeLeft <= 0) {
            handleTimeUp();
            return;
        }
        const timerId = setInterval(() => {
            setTimeLeft(prev => prev - 1);
        }, 1000);
        return () => clearInterval(timerId);
    }, [timeLeft, hasAnswered, currentIndex, currentQ, questions.length]);

    if (currentIndex >= questions.length && questions.length > 0) {
        localStorage.removeItem(`cyberduo_inprogress_${gameKey}_${level}`);
        return (
            <div className="gs-container">
                <div className="gs-completion-screen">
                    <h1 className="gs-neon-title">Mission Complete!</h1>
                    <div className="gs-stats-box">
                        <p>SCORE: {score} / 100</p>
                        <p>XP EARNED: {xp}</p>
                    </div>
                    <button className="gs-btn-primary" onClick={() => onComplete(xp)}>CONTINUE TO DASHBOARD</button>
                </div>
            </div>
        );
    }

    if (!currentQ) {
        return (
            <div className="gs-container">
                {onBack && <button className="gs-btn-back" onClick={onBack}>← ABORT MISSION</button>}
                <div className="gs-completion-screen">
                    <h1 className="gs-neon-title" style={{color: '#ff6b6b'}}>No Intel Found</h1>
                    <p style={{color: 'rgba(255,255,255,0.7)', marginTop: '20px'}}>Mission parameters for {gameName || gameKey} ({level}) could not be loaded.</p>
                </div>
            </div>
        );
    }

    const handleAnswerEval = (isCorrect) => {
        setHasAnswered(true);
        setIsCorrectResult(isCorrect);
        if (currentIndex > highestCompletedIndex) {
            setHighestCompletedIndex(currentIndex);
        }
        if (isCorrect) {
            setFeedback({ type: 'success', message: 'Correct! (+20 XP)' });
            setScore(prev => prev + 20);
            setXp(prev => prev + 20);
            updateStreak();
        } else {
            setFeedback({ type: 'error', message: currentQ.explain });
            setXp(prev => Math.max(0, prev - 10));
        }
    };

    const handleTimeUp = () => {
        setFeedback({ type: 'error', message: "Time's up! You took too long to analyze the threat." });
        handleAnswerEval(false);
    };

    const resetQuestionState = () => {
        setFeedback(null);
        setSelectedOption(null);
        setDroppedFlags([]);
        setCheckedFlags([]);
        setShowHover(false);
        setTriageAnswers({});
        setBuildAnswers({ lure: null, urgency: null });
        setSwitchActive(false);
        setSequenceList([]);
        setHasAnswered(false);
        setIsCorrectResult(null);
        setTimeLeft(45);
    };

    const handleNextQuestion = () => {
        resetQuestionState();
        setCurrentIndex(currentIndex + 1);
    };

    const handlePrevQuestion = () => {
        if (currentIndex > 0) {
            resetQuestionState();
            setCurrentIndex(currentIndex - 1);
        }
    };

    const handleSubmit = () => {
        if (hasAnswered) return;
        let isCorrect = false;

        if (currentQ.format === 'spot_fake' || currentQ.format === 'decision_simulator' || currentQ.format === 'chat_sim' || currentQ.format === 'spot_weak' || currentQ.format === 'scenario_mcq') {
            if (!selectedOption) return;
            isCorrect = selectedOption === currentQ.correctAnswer;
        } else if (currentQ.format === 'password_builder') {
            const pwd = droppedFlags.map(fId => currentQ.pieces.find(p => p.id === fId)?.text).join('');
            const hasUpper = /[A-Z]/.test(pwd);
            const hasLower = /[a-z]/.test(pwd);
            const hasNumber = /[0-9]/.test(pwd);
            const hasSymbol = /[^A-Za-z0-9]/.test(pwd);
            const hasPI = droppedFlags.some(fId => currentQ.pieces.find(p => p.id === fId)?.isPersonalInfo);
            isCorrect = pwd.length >= 8 && hasUpper && hasLower && hasNumber && hasSymbol && !hasPI;
        } else if (currentQ.format === 'drag_flags') {
            const correctSet = new Set(currentQ.correctFlags);
            const userSet = new Set(droppedFlags);
            isCorrect = correctSet.size > 0 && correctSet.size === userSet.size && [...correctSet].every(flag => userSet.has(flag));
        } else if (currentQ.format === 'link_inspector' || currentQ.format === 'file_inspector') {
            if (!selectedOption) return;
            isCorrect = selectedOption === currentQ.correctAnswer;
        } else if (currentQ.format === 'case_study' || currentQ.format === 'select_all') {
            const correctSet = new Set(currentQ.correctFlags);
            const userSet = new Set(checkedFlags);
            isCorrect = correctSet.size > 0 && correctSet.size === userSet.size && [...correctSet].every(flag => userSet.has(flag));
        } else if (currentQ.format === 'click_flags') {
            const correctFlags = currentQ.emailParts.filter(p => p.isFlag);
            isCorrect = checkedFlags.length === correctFlags.length && checkedFlags.every(id => currentQ.emailParts.find(p => p.id === id)?.isFlag);
        } else if (currentQ.format === 'inbox_triage') {
            isCorrect = Object.keys(triageAnswers).length === currentQ.emails.length && currentQ.emails.every(e => triageAnswers[e.id] === e.isPhish);
        } else if (currentQ.format === 'file_triage' || currentQ.format === 'traffic_triage') {
            isCorrect = Object.keys(triageAnswers).length === currentQ.files.length && currentQ.files.every(f => triageAnswers[f.id] === f.isMalware);
        } else if (currentQ.format === 'password_triage') {
            isCorrect = Object.keys(triageAnswers).length === currentQ.passwords.length && currentQ.passwords.every(p => triageAnswers[p.id] === p.isStrong);
        } else if (currentQ.format === 'authenticator_sim') {
            isCorrect = droppedFlags[0] === currentQ.correctCode;
        } else if (currentQ.format === 'sequence_builder') {
            isCorrect = sequenceList.every((step, idx) => step.correctOrder === idx);
        } else if (currentQ.format === 'threat_router') {
            const correctPortals = currentQ.portals.filter(p => p.isCorrect).map(p => p.id);
            isCorrect = droppedFlags.length === correctPortals.length && correctPortals.every(p => droppedFlags.includes(p));
        } else if (currentQ.format === 'build_phish') {
            if (!buildAnswers.lure || !buildAnswers.urgency) return;
            isCorrect = buildAnswers.lure.correct && buildAnswers.urgency.correct;
        }

        handleAnswerEval(isCorrect);
    };

    const showModal = (title, content) => setModal({ show: true, title, content });

    const renderQuestionFormat = () => {
        switch (currentQ.format) {
            case 'spot_fake':
                return (
                    <div className="gs-format gs-spot-fake">
                        {currentQ.options.map((opt, i) => (
                            <div key={i} className={`gs-option-card ${selectedOption === opt ? 'selected' : ''}`} onClick={() => setSelectedOption(opt)}>
                                <span className="gs-sender-icon">👤</span> {opt}
                            </div>
                        ))}
                    </div>
                );
            case 'decision_simulator':
            case 'spot_weak':
            case 'scenario_mcq':
                return (
                    <div className="gs-format gs-mcq-grid">
                        {currentQ.options.map((opt, i) => (
                            <button key={i} className={`gs-mcq-card ${selectedOption === opt ? 'selected' : ''}`} onClick={() => setSelectedOption(opt)}>
                                {opt}
                            </button>
                        ))}
                    </div>
                );
            case 'chat_sim':
                return (
                    <div className="gs-format gs-chat-sim">
                        <div className="gs-chat-window">
                            <div className="gs-chat-header">
                                <span className="gs-chat-icon">💬</span>
                                <h4>{currentQ.questionText}</h4>
                            </div>
                            <div className="gs-chat-history">
                                {currentQ.chatHistory.map((msg, i) => (
                                    <div key={i} className="gs-chat-bubble scammer">
                                        <div className="gs-chat-sender">{msg.sender}</div>
                                        {msg.message}
                                    </div>
                                ))}
                            </div>
                            <div className="gs-chat-replies">
                                <h5>Choose your reply:</h5>
                                {currentQ.options.map((opt, i) => (
                                    <button key={i} className={`gs-chat-reply-btn ${selectedOption === opt ? 'selected' : ''}`} onClick={() => setSelectedOption(opt)}>
                                        {opt}
                                    </button>
                                ))}
                            </div>
                        </div>
                    </div>
                );
            case 'drag_flags':
                const handleDragStart = (e, flag) => e.dataTransfer.setData('flag', flag);
                const handleDrop = (e) => {
                    e.preventDefault();
                    const flag = e.dataTransfer.getData('flag');
                    if (flag && !droppedFlags.includes(flag)) setDroppedFlags([...droppedFlags, flag]);
                };
                const handleDragOver = (e) => e.preventDefault();
                return (
                    <div className="gs-format gs-drag-flags">
                        <div className="gs-email-mockup" style={{ whiteSpace: 'pre-wrap' }}>{currentQ.emailContent}</div>
                        <div className="gs-drag-area">
                            <div className="gs-flags-source">
                                <h4>Available Flags</h4>
                                {currentQ.redFlags.filter(f => !droppedFlags.includes(f)).map((flag, i) => (
                                    <div key={i} draggable onDragStart={(e) => handleDragStart(e, flag)} className="gs-draggable-flag">
                                        🚩 {flag}
                                    </div>
                                ))}
                            </div>
                            <div className="gs-drop-zone" onDrop={handleDrop} onDragOver={handleDragOver}>
                                <h4>DROP SUSPICIOUS FLAGS HERE</h4>
                                {droppedFlags.map((flag, i) => (
                                    <div key={i} className="gs-dropped-flag" onClick={() => setDroppedFlags(droppedFlags.filter(f => f !== flag))}>
                                        <span>🚩 {flag}</span> <span className="gs-remove-flag">✕</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                );
            case 'click_flags':
                return (
                    <div className="gs-format gs-click-flags">
                        <div className="gs-email-mockup email-client-style delay-anim">
                            {currentQ.emailParts.map((part, i) => {
                                const rowClass = i <= 1 ? 'header-row' : 'body-row';
                                return (
                                    <div key={i} className={`gs-email-part ${rowClass} ${checkedFlags.includes(part.id) ? 'highlighted' : ''}`}
                                        onClick={() => {
                                            if (checkedFlags.includes(part.id)) setCheckedFlags(checkedFlags.filter(id => id !== part.id));
                                            else setCheckedFlags([...checkedFlags, part.id]);
                                        }}>
                                        {part.text}
                                    </div>
                                );
                            })}
                        </div>
                    </div>
                );
            case 'inbox_triage':
                return (
                    <div className="gs-format gs-inbox-triage">
                        {currentQ.emails.map((email, i) => (
                            <div key={i} className="gs-triage-row">
                                <div className="gs-triage-info">
                                    <strong>{email.subject}</strong>
                                    <span>{email.sender}</span>
                                </div>
                                <div className="gs-triage-actions">
                                    <button className={`gs-btn-keep ${triageAnswers[email.id] === false ? 'selected' : ''}`} onClick={() => setTriageAnswers({ ...triageAnswers, [email.id]: false })}>KEEP</button>
                                    <button className={`gs-btn-delete ${triageAnswers[email.id] === true ? 'selected' : ''}`} onClick={() => setTriageAnswers({ ...triageAnswers, [email.id]: true })}>DELETE</button>
                                </div>
                            </div>
                        ))}
                    </div>
                );
            case 'file_triage':
            case 'traffic_triage':
                return (
                    <div className="gs-format gs-inbox-triage gs-file-triage">
                        {currentQ.files.map((file, i) => (
                            <div key={i} className="gs-triage-row">
                                <div className="gs-triage-info" style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
                                    <span style={{ fontSize: '2rem' }}>{file.icon}</span>
                                    <strong>{file.name}</strong>
                                </div>
                                <div className="gs-triage-actions">
                                    <button className={`gs-btn-keep ${triageAnswers[file.id] === false ? 'selected' : ''}`} onClick={() => setTriageAnswers({ ...triageAnswers, [file.id]: false })}>{currentQ.format === 'traffic_triage' ? 'ALLOW' : 'SAFE (KEEP)'}</button>
                                    <button className={`gs-btn-delete ${triageAnswers[file.id] === true ? 'selected' : ''}`} onClick={() => setTriageAnswers({ ...triageAnswers, [file.id]: true })}>{currentQ.format === 'traffic_triage' ? 'BLOCK' : 'MALWARE (DEL)'}</button>
                                </div>
                            </div>
                        ))}
                    </div>
                );
            case 'build_phish':
                return (
                    <div className="gs-format gs-build-phish">
                        <div className="gs-build-section">
                            <h5>1. Select Attacker Lure</h5>
                            <div className="gs-build-options">
                                {currentQ.lures.map((lure, i) => (
                                    <button key={i} className={`gs-build-btn ${buildAnswers.lure?.text === lure.text ? 'selected' : ''}`} onClick={() => setBuildAnswers({ ...buildAnswers, lure })}>
                                        {lure.text}
                                    </button>
                                ))}
                            </div>
                        </div>
                        <div className="gs-build-section">
                            <h5>2. Select Urgency Tactic</h5>
                            <div className="gs-build-options">
                                {currentQ.urgencies.map((urgency, i) => (
                                    <button key={i} className={`gs-build-btn ${buildAnswers.urgency?.text === urgency.text ? 'selected' : ''}`} onClick={() => setBuildAnswers({ ...buildAnswers, urgency })}>
                                        {urgency.text}
                                    </button>
                                ))}
                            </div>
                        </div>
                    </div>
                );
            case 'link_inspector':
                return (
                    <div className="gs-format gs-link-inspector">
                        <div className="gs-link-container" onMouseEnter={() => setShowHover(true)} onMouseLeave={() => setShowHover(false)}>
                            <span className="gs-fake-link">{currentQ.displayedLink}</span>
                            {showHover && <div className="gs-hover-tooltip">{currentQ.actualDestination}</div>}
                        </div>
                        <div className="gs-inspector-actions">
                            <button className={`gs-btn-safe ${selectedOption === 'Safe' ? 'selected' : ''}`} onClick={() => setSelectedOption('Safe')}>✔ SAFE</button>
                            <button className={`gs-btn-phish ${selectedOption === 'Phishing' ? 'selected' : ''}`} onClick={() => setSelectedOption('Phishing')}>⚠ PHISHING</button>
                        </div>
                    </div>
                );
            case 'file_inspector':
                return (
                    <div className="gs-format gs-link-inspector gs-file-inspector">
                        <div className="gs-link-container" style={{ padding: '30px', border: '2px dashed #ffb020', borderRadius: '15px', background: 'rgba(20,20,30,0.8)' }}
                             onMouseEnter={() => setShowHover(true)} onMouseLeave={() => setShowHover(false)}>
                            <div style={{ fontSize: '3rem', marginBottom: '10px' }}>📎</div>
                            <span className="gs-fake-link" style={{ fontSize: '1.2rem', color: '#fff' }}>{currentQ.displayedName}</span>
                            {showHover && <div className="gs-hover-tooltip" style={{ bottom: '-60px' }}>{currentQ.actualDestination}</div>}
                        </div>
                        <div className="gs-inspector-actions">
                            <button className={`gs-btn-safe ${selectedOption === 'Safe' ? 'selected' : ''}`} onClick={() => setSelectedOption('Safe')}>✔ SAFE</button>
                            <button className={`gs-btn-delete ${selectedOption === 'Malware' ? 'selected' : ''}`} onClick={() => setSelectedOption('Malware')} style={{ padding: '15px 30px', fontSize: '1.2rem', fontWeight: 'bold' }}>⚠ MALWARE</button>
                        </div>
                    </div>
                );
            case 'select_all':
                return (
                    <div className="gs-format gs-mcq-grid">
                        {(currentQ.redFlags || currentQ.options).map((flag, i) => (
                            <label key={i} className={`gs-mcq-card checkbox-card ${checkedFlags.includes(flag) ? 'selected' : ''}`}>
                                <input type="checkbox" checked={checkedFlags.includes(flag)} onChange={(e) => {
                                    if (e.target.checked) setCheckedFlags([...checkedFlags, flag]);
                                    else setCheckedFlags(checkedFlags.filter(f => f !== flag));
                                }} />
                                <div className="gs-custom-checkbox"></div>
                                <span className="gs-checkbox-text">{flag}</span>
                            </label>
                        ))}
                    </div>
                );
            case 'case_study':
                return (
                    <div className="gs-format gs-case-study gs-select-all">
                        {currentQ.emailContent && (
                            <div className="gs-email-mockup" style={{ whiteSpace: 'pre-wrap' }}>{currentQ.emailContent}</div>
                        )}
                        <div className="gs-checklist">
                            {(currentQ.redFlags || currentQ.options).map((flag, i) => (
                                <label key={i} className="gs-checkbox-label">
                                    <input type="checkbox" checked={checkedFlags.includes(flag)} onChange={(e) => {
                                        if (e.target.checked) setCheckedFlags([...checkedFlags, flag]);
                                        else setCheckedFlags(checkedFlags.filter(f => f !== flag));
                                    }} />
                                    <span className="gs-custom-checkbox"></span>
                                    {flag}
                                </label>
                            ))}
                        </div>
                    </div>
                );
            case 'password_builder':
                const handleDragStartPB = (e, piece) => e.dataTransfer.setData('pieceId', piece.id);
                const handleDropPB = (e) => {
                    e.preventDefault();
                    const pieceId = e.dataTransfer.getData('pieceId');
                    if (pieceId && !droppedFlags.includes(pieceId)) setDroppedFlags([...droppedFlags, pieceId]);
                };
                const handleDragOverPB = (e) => e.preventDefault();
                const pwdStr = droppedFlags.map(fId => currentQ.pieces.find(p => p.id === fId)?.text).join('');
                let strScore = 0;
                if (pwdStr.length > 0) {
                    if (pwdStr.length >= 8) strScore += 25;
                    if (/[A-Z]/.test(pwdStr)) strScore += 25;
                    if (/[0-9]/.test(pwdStr)) strScore += 25;
                    if (/[^A-Za-z0-9]/.test(pwdStr)) strScore += 25;
                    if (droppedFlags.some(fId => currentQ.pieces.find(p => p.id === fId)?.isPersonalInfo)) strScore = Math.max(10, strScore - 40);
                }
                return (
                    <div className="gs-format gs-drag-flags gs-password-builder">
                        <div className="gs-strength-meter">
                            <span className="gs-strength-label">Password Strength:</span>
                            <div className="gs-strength-bar-bg">
                                <div className="gs-strength-bar-fill" style={{ width: `${strScore}%`, backgroundColor: strScore === 100 ? '#00FF9D' : strScore > 50 ? '#ffb020' : '#ff6b6b' }}></div>
                            </div>
                            <span className="gs-pwd-display">{pwdStr || "Drag pieces to build..."}</span>
                        </div>
                        <div className="gs-drag-area">
                            <div className="gs-flags-source">
                                <h4>Available Pieces</h4>
                                <div className="gs-pieces-container">
                                    {currentQ.pieces.filter(p => !droppedFlags.includes(p.id)).map((piece, i) => (
                                        <div key={i} draggable onDragStart={(e) => handleDragStartPB(e, piece)} className={`gs-draggable-flag gs-password-chip type-${piece.type}`}>
                                            {piece.text}
                                        </div>
                                    ))}
                                </div>
                            </div>
                            <div className="gs-drop-zone gs-password-dropzone" onDrop={handleDropPB} onDragOver={handleDragOverPB}>
                                <h4>YOUR PASSWORD SEQUENCE</h4>
                                <div className="gs-pieces-container">
                                    {droppedFlags.map((id, i) => {
                                        const piece = currentQ.pieces.find(p => p.id === id);
                                        if (!piece) return null;
                                        return (
                                            <div key={i} className={`gs-dropped-flag gs-password-chip type-${piece.type}`} onClick={() => setDroppedFlags(droppedFlags.filter(f => f !== id))}>
                                                <span>{piece.text}</span> <span className="gs-remove-flag">✕</span>
                                            </div>
                                        );
                                    })}
                                </div>
                            </div>
                        </div>
                    </div>
                );
            case 'password_triage':
                return (
                    <div className="gs-format gs-inbox-triage gs-password-triage">
                        {currentQ.passwords.map((pw, i) => (
                            <div key={i} className="gs-triage-row">
                                <div className="gs-triage-info">
                                    <strong style={{fontFamily: 'monospace', letterSpacing: '2px', fontSize: '1.2rem'}}>{pw.text}</strong>
                                </div>
                                <div className="gs-triage-actions">
                                    <button className={`gs-btn-keep ${triageAnswers[pw.id] === true ? 'selected' : ''}`} onClick={() => setTriageAnswers({ ...triageAnswers, [pw.id]: true })}>STRONG 🛡️</button>
                                    <button className={`gs-btn-delete ${triageAnswers[pw.id] === false ? 'selected' : ''}`} style={{borderColor: 'rgba(255, 107, 107, 0.3)'}} onClick={() => setTriageAnswers({ ...triageAnswers, [pw.id]: false })}>WEAK ⚠️</button>
                                </div>
                            </div>
                        ))}
                    </div>
                );
            case 'authenticator_sim':
                const handleDragStartAuth = (e, code) => e.dataTransfer.setData('authCode', code);
                const handleDropAuth = (e) => {
                    e.preventDefault();
                    const code = e.dataTransfer.getData('authCode');
                    if (code) setDroppedFlags([code]);
                };
                const handleDragOverAuth = (e) => e.preventDefault();
                return (
                    <div className="gs-format gs-authenticator-sim">
                        <div className="gs-phone-mockup">
                            <div className="gs-phone-header"><span>12:00</span><div>📱🔋</div></div>
                            <h4 className="gs-phone-title">Recent Messages</h4>
                            {currentQ.phoneScreen.map((sms, i) => (
                                <div key={i} className="gs-sms-bubble" draggable onDragStart={(e) => handleDragStartAuth(e, sms.code)}>
                                    <div className="gs-sms-service">{sms.service}</div>
                                    <div className="gs-sms-code">Code: <strong>{sms.code}</strong></div>
                                </div>
                            ))}
                        </div>
                        <div className="gs-login-screen">
                            <h4>{currentQ.gameName === 'password' ? "Bank Login" : "Secure Login"}</h4>
                            <p className="gs-login-status">Password Accepted.</p>
                            <p className="gs-login-prompt">Please enter the 2FA code sent to your device:</p>
                            <div className={`gs-2fa-input-box ${droppedFlags[0] ? 'filled' : ''}`} onDrop={handleDropAuth} onDragOver={handleDragOverAuth}>
                                {droppedFlags[0] ? droppedFlags[0] : "Drop Code Here"}
                            </div>
                            {droppedFlags[0] && !hasAnswered && <button className="gs-btn-reset-auth" onClick={() => setDroppedFlags([])}>Clear</button>}
                        </div>
                    </div>
                );
            case 'sequence_builder':
                const handleDragStartSeq = (e, index) => e.dataTransfer.setData('sourceIndex', index);
                const handleDropSeq = (e, targetIndex) => {
                    e.preventDefault();
                    const sourceIndex = parseInt(e.dataTransfer.getData('sourceIndex'), 10);
                    if (sourceIndex === targetIndex) return;
                    const newList = [...sequenceList];
                    const [draggedItem] = newList.splice(sourceIndex, 1);
                    newList.splice(targetIndex, 0, draggedItem);
                    setSequenceList(newList);
                };
                const handleDragOverSeq = (e) => e.preventDefault();
                return (
                    <div className="gs-format gs-sequence-builder">
                        <div className="gs-sequence-list">
                            {sequenceList.map((step, index) => (
                                <div key={step.id} className="gs-sequence-item" draggable onDragStart={(e) => handleDragStartSeq(e, index)} onDrop={(e) => handleDropSeq(e, index)} onDragOver={handleDragOverSeq}>
                                    <div className="gs-seq-handle">⋮⋮</div>
                                    <span className="gs-seq-text">{step.text}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                );
            case 'threat_router':
                const handleTogglePortal = (portalId) => {
                    if (droppedFlags.includes(portalId)) setDroppedFlags(droppedFlags.filter(id => id !== portalId));
                    else setDroppedFlags([...droppedFlags, portalId]);
                };
                return (
                    <div className="gs-format gs-threat-router">
                        <div className="gs-router-email">
                            <div className="gs-email-header">SUSPICIOUS MESSAGE</div>
                            <div className="gs-email-body">{currentQ.emailSnippet}</div>
                        </div>
                        <div className="gs-portals-container">
                            {currentQ.portals.map((portal) => (
                                <div key={portal.id} style={{cursor: 'pointer'}} className={`gs-portal ${droppedFlags.includes(portal.id) ? 'active' : ''}`} onClick={() => handleTogglePortal(portal.id)}>
                                    <div className="gs-portal-glow"></div>
                                    <span>{portal.text}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                );
            default:
                return <div>Format not supported</div>;
        }
    };

    const isAlreadyCompleted = currentIndex <= highestCompletedIndex && !hasAnswered;

    return (
        <div className="gs-container">
            {onBack && <button className="gs-btn-back" onClick={onBack}>← ABORT MISSION</button>}

            <div className="gs-header">
                <div className="gs-progress-wrapper">
                    <span className="gs-progress-text">Question {currentIndex + 1} of {questions.length}</span>
                    <div className="gs-progress-bar">
                        <div className="gs-progress-fill" style={{ width: `${((currentIndex) / questions.length) * 100}%` }}></div>
                    </div>
                </div>
                <div className="gs-stats" style={{display: 'flex', gap: '15px', alignItems: 'center'}}>
                    <div className="gs-timer-badge" style={{color: timeLeft <= 10 ? '#ff6b6b' : '#00FF9D'}}>⏱ {timeLeft}s</div>
                    <span className="gs-xp-badge">⚡ {xp} XP</span>
                </div>
            </div>

            <div className="gs-question-card">
                <h2 className="gs-question-text">{currentQ.questionText}</h2>
                <div className={`gs-format-container ${hasAnswered ? 'answered' : ''}`}>
                    {renderQuestionFormat()}
                </div>

                {isAlreadyCompleted && (
                    <div className="gs-feedback success" style={{ marginBottom: '15px' }}>
                        Mission Already Completed. Read-Only Mode.
                    </div>
                )}

                {feedback && <div className={`gs-feedback ${feedback.type}`}>{feedback.message}</div>}

                <div className="gs-actions-row">
                    {currentIndex > 0 && (
                        <button className="gs-btn-prev" onClick={handlePrevQuestion}>🡄 PREVIOUS</button>
                    )}
                    {(!hasAnswered && !isAlreadyCompleted) ? (
                        <button className="gs-btn-submit" style={{ margin: 0, minWidth: 'auto', padding: '15px 40px' }} onClick={handleSubmit}>SUBMIT ANSWER</button>
                    ) : (
                        <>
                            {(!isCorrectResult || isAlreadyCompleted) && (
                                <button className="gs-btn-reveal-answer" onClick={() => showModal('Correct Answer', currentQ.reveal || currentQ.explain)}>👁️ SHOW ANSWER</button>
                            )}
                            <button className="gs-btn-next" onClick={handleNextQuestion}>NEXT ➔</button>
                        </>
                    )}
                </div>
            </div>

            <div className="gs-ai-toolbar">
                <button onClick={() => showModal('Hint 💡', currentQ.hint)}>💡 Hint</button>
                <button onClick={() => showModal('Explain 📚', currentQ.explain)}>📚 Explain</button>
                <button onClick={() => setChatOpen(true)}>💬 Chat</button>
            </div>

            {/* ✅ AI CHAT WINDOW */}
            {chatOpen && (
                <div className="gs-modal-overlay" onClick={() => setChatOpen(false)}>
                    <div className="gs-modal-content" style={{width: '400px', maxHeight: '500px', display: 'flex', flexDirection: 'column'}} onClick={e => e.stopPropagation()}>
                        <h3>🤖 AI Agent Chat</h3>
                        <div style={{flex: 1, overflowY: 'auto', marginBottom: '10px', maxHeight: '300px', padding: '10px', background: 'rgba(0,0,0,0.3)', borderRadius: '8px'}}>
                            {chatMessages.length === 0 && (
                                <p style={{color: 'rgba(255,255,255,0.5)', textAlign: 'center', fontSize: '13px'}}>Ask me anything about this question!</p>
                            )}
                            {chatMessages.map((msg, i) => (
                                <div key={i} style={{marginBottom: '10px', textAlign: msg.role === 'user' ? 'right' : 'left'}}>
                                    <span style={{
                                        background: msg.role === 'user' ? '#00FF9D' : '#1a1a2e',
                                        color: msg.role === 'user' ? '#000' : '#fff',
                                        padding: '8px 12px',
                                        borderRadius: '12px',
                                        display: 'inline-block',
                                        maxWidth: '80%',
                                        fontSize: '13px'
                                    }}>{msg.text}</span>
                                </div>
                            ))}
                            {chatLoading && (
                                <div style={{textAlign: 'left'}}>
                                    <span style={{color: '#00FF9D', fontSize: '13px'}}>AI is thinking... ⏳</span>
                                </div>
                            )}
                        </div>
                        <div style={{display: 'flex', gap: '8px'}}>
                            <input
                                type="text"
                                value={chatInput}
                                onChange={e => setChatInput(e.target.value)}
                                onKeyDown={e => e.key === 'Enter' && handleChatSend()}
                                placeholder="Ask a question..."
                                style={{flex: 1, padding: '8px', borderRadius: '6px', border: '1px solid #00FF9D', background: '#0a0a1a', color: '#fff', fontSize: '13px'}}
                            />
                            <button onClick={handleChatSend} disabled={chatLoading}
                                style={{padding: '8px 16px', background: chatLoading ? '#555' : '#00FF9D', color: '#000', border: 'none', borderRadius: '6px', cursor: chatLoading ? 'not-allowed' : 'pointer', fontWeight: 'bold'}}>
                                SEND
                            </button>
                        </div>
                        <button onClick={() => setChatOpen(false)} style={{marginTop: '10px'}}>CLOSE</button>
                    </div>
                </div>
            )}

            {modal.show && (
                <div className="gs-modal-overlay" onClick={() => setModal({ ...modal, show: false })}>
                    <div className="gs-modal-content" onClick={e => e.stopPropagation()}>
                        <h3>{modal.title}</h3>
                        <p>{modal.content}</p>
                        <button onClick={() => setModal({ ...modal, show: false })}>CLOSE</button>
                    </div>
                </div>
            )}
        </div>
    );
}