import React, { useState, useEffect } from 'react';
import '../styles/gamescreen.css';
import gameData from '../data/GameQuestions.json';

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
    const [feedback, setFeedback] = useState(null);
    const [resultSaved, setResultSaved] = useState(false);
    
    useEffect(() => {
        if (currentIndex > 0 || score > 0 || xp > 0) {
            localStorage.setItem(`cyberduo_inprogress_${gameKey}_${level}`, JSON.stringify({
                currentIndex, score, xp
            }));
        }
        if (onProgressUpdate) {
            onProgressUpdate(currentIndex);
        }
    }, [currentIndex, score, xp, gameKey, level]);
    
    const [timeLeft, setTimeLeft] = useState(45);
    const [hasAnswered, setHasAnswered] = useState(false);
    const [isCorrectResult, setIsCorrectResult] = useState(null);
    
    const [selectedOption, setSelectedOption] = useState(null);
    const [droppedFlags, setDroppedFlags] = useState([]);
    const [checkedFlags, setCheckedFlags] = useState([]);
    const [showHover, setShowHover] = useState(false);
    const [triageAnswers, setTriageAnswers] = useState({});
    const [buildAnswers, setBuildAnswers] = useState({ lure: null, urgency: null });

    const [modal, setModal] = useState({ show: false, title: '', content: '' });

    const [chatOpen, setChatOpen] = useState(false);
    const [chatMessages, setChatMessages] = useState([]);
    const [chatInput, setChatInput] = useState('');
    const [chatLoading, setChatLoading] = useState(false);

    const GEMINI_API_KEY = "AIzaSyAfAUhkJSnr7eUo90DV_xITKl8gFqEB5E0";

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
            console.log("Gemini response:", JSON.stringify(data));
            if (data.candidates && data.candidates[0] && data.candidates[0].content) {
                const reply = data.candidates[0].content.parts[0].text;
                setChatMessages(prev => [...prev, { role: 'ai', text: reply }]);
            } else if (data.error) {
                setChatMessages(prev => [...prev, { role: 'ai', text: `Error: ${data.error.message}` }]);
            } else {
                setChatMessages(prev => [...prev, { role: 'ai', text: 'Sorry, I could not get a response. Please try again.' }]);
            }
        } catch (err) {
            console.error("Gemini error:", err);
            setChatMessages(prev => [...prev, { role: 'ai', text: 'Sorry, I could not connect. Please check your internet connection.' }]);
        }
        setChatLoading(false);
    };

    const currentQ = questions[currentIndex];
    
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

    useEffect(() => {
        const saveResult = async () => {
            if (currentIndex >= questions.length && questions.length > 0 && !resultSaved) {
                setResultSaved(true);
                localStorage.removeItem(`cyberduo_inprogress_${gameKey}_${level}`);
                try {
                    const userId = localStorage.getItem("user_id");
                    if (userId) {
                        await fetch("http://localhost:8000/game/save-result", {
                            method: "POST",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({
                                user_id: userId,
                                game_key: gameKey,
                                level: level,
                                xp_earned: xp,
                                score: score
                            })
                        });
                    }
                } catch (err) {
                    console.error("Could not save game result:", err);
                }
            }
        };
        saveResult();
    }, [currentIndex, questions.length]);

    if (currentIndex >= questions.length && questions.length > 0) {
        return (
            <div className="gs-container">
                <div className="gs-completion-screen">
                    <h1 className="gs-neon-title">Mission Complete!</h1>
                    <div className="gs-stats-box">
                        <p>SCORE: {score} / 100</p>
                        <p>XP EARNED: {xp}</p>
                    </div>
                    <button className="gs-btn-primary" onClick={onComplete}>CONTINUE TO DASHBOARD</button>
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
        if (isCorrect) {
            setFeedback({ type: 'success', message: 'Correct! (+20 XP)' });
            setScore(prev => prev + 20);
            setXp(prev => prev + 20);
        } else {
            setFeedback({ type: 'error', message: currentQ.explain });
            setXp(prev => Math.max(0, prev - 10));
        }
    };

    const handleTimeUp = () => {
        setFeedback({ type: 'error', message: "Time's up! You took too long to analyze the threat." });
        handleAnswerEval(false);
    };

    const handleNextQuestion = () => {
        setFeedback(null);
        setSelectedOption(null);
        setDroppedFlags([]);
        setCheckedFlags([]);
        setShowHover(false);
        setTriageAnswers({});
        setBuildAnswers({ lure: null, urgency: null });
        setHasAnswered(false);
        setIsCorrectResult(null);
        setTimeLeft(45);
        const nextIndex = currentIndex + 1;
        setCurrentIndex(nextIndex);
    };

    const handleSubmit = () => {
        if (hasAnswered) return;
        let isCorrect = false;

        if (currentQ.format === 'spot_fake' || currentQ.format === 'decision_simulator' || currentQ.format === 'chat_sim') {
            if (!selectedOption) return;
            isCorrect = selectedOption === currentQ.correctAnswer;
        } else if (currentQ.format === 'drag_flags') {
            const correctSet = new Set(currentQ.correctFlags);
            const userSet = new Set(droppedFlags);
            isCorrect = correctSet.size > 0 && correctSet.size === userSet.size && [...correctSet].every(flag => userSet.has(flag));
        } else if (currentQ.format === 'link_inspector') {
            if (!selectedOption) return;
            isCorrect = selectedOption === currentQ.correctAnswer;
        } else if (currentQ.format === 'case_study') {
            const correctSet = new Set(currentQ.correctFlags);
            const userSet = new Set(checkedFlags);
            isCorrect = correctSet.size > 0 && correctSet.size === userSet.size && [...correctSet].every(flag => userSet.has(flag));
        } else if (currentQ.format === 'click_flags') {
            const correctFlags = currentQ.emailParts.filter(p => p.isFlag);
            isCorrect = checkedFlags.length === correctFlags.length && checkedFlags.every(id => currentQ.emailParts.find(p => p.id === id)?.isFlag);
        } else if (currentQ.format === 'inbox_triage') {
            isCorrect = Object.keys(triageAnswers).length === currentQ.emails.length && currentQ.emails.every(e => triageAnswers[e.id] === e.isPhish);
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
                return (
                    <div className="gs-format gs-decision-sim">
                        {currentQ.options.map((opt, i) => (
                            <button key={i} className={`gs-option-btn ${selectedOption === opt ? 'selected' : ''}`} onClick={() => setSelectedOption(opt)}>
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
            case 'case_study':
                return (
                    <div className="gs-format gs-case-study">
                        <div className="gs-email-mockup" style={{ whiteSpace: 'pre-wrap' }}>{currentQ.emailContent}</div>
                        <div className="gs-checklist">
                            {currentQ.redFlags.map((flag, i) => (
                                <label key={i} className="gs-checkbox-label">
                                    <input type="checkbox" checked={checkedFlags.includes(flag)}
                                        onChange={(e) => {
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
            default:
                return <div>Format not supported</div>;
        }
    };

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

                {feedback && <div className={`gs-feedback ${feedback.type}`}>{feedback.message}</div>}

                {!hasAnswered ? (
                    <button className="gs-btn-submit" onClick={handleSubmit}>SUBMIT ANSWER</button>
                ) : (
                    <div className="gs-actions-row">
                        {!isCorrectResult && (
                            <button className="gs-btn-reveal-answer" onClick={() => showModal('Correct Answer', currentQ.reveal || currentQ.explain)}>
                                👁️ SHOW ANSWER
                            </button>
                        )}
                        <button className="gs-btn-next" onClick={handleNextQuestion}>NEXT QUESTION ➔</button>
                    </div>
                )}
            </div>

            <div className="gs-ai-toolbar">
                <button onClick={() => showModal('Hint 💡', currentQ.hint)}>💡 Hint</button>
                <button onClick={() => showModal('Explain 📚', currentQ.explain)}>📚 Explain</button>
                <button onClick={() => setChatOpen(true)}>💬 Chat</button>
            </div>

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
                                    }}>
                                        {msg.text}
                                    </span>
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
                            <button
                                onClick={handleChatSend}
                                disabled={chatLoading}
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