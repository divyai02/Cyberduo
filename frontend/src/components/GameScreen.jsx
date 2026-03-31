import React, { useState, useEffect } from 'react';
import '../styles/gamescreen.css';
import gameData from '../data/GameQuestions.json';

export default function GameScreen({ gameKey = "phishing", gameName, level, onComplete, onProgressUpdate, onBack }) {
    const questions = gameData[gameKey]?.[level] || [];
    
    // State
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
    const [feedback, setFeedback] = useState(null); // { type: 'success' | 'error', message: string }
    
    // Save state on change and notify dashboard
    useEffect(() => {
        if (currentIndex > 0 || score > 0 || xp > 0 || highestCompletedIndex > -1) {
            localStorage.setItem(`cyberduo_inprogress_${gameKey}_${level}`, JSON.stringify({
                currentIndex, score, xp, highestCompletedIndex
            }));
        }
        // Force the dashboard to align its visual progress circle with the local game state (useful when explicitly replaying completed games)
        if (onProgressUpdate) {
            onProgressUpdate(highestCompletedIndex + 1);
        }
    }, [currentIndex, score, xp, highestCompletedIndex, gameKey, level]);
    
    const [timeLeft, setTimeLeft] = useState(45);
    const [hasAnswered, setHasAnswered] = useState(false);
    const [isCorrectResult, setIsCorrectResult] = useState(null);
    
    // Format-specific state
    const [selectedOption, setSelectedOption] = useState(null);
    const [droppedFlags, setDroppedFlags] = useState([]);
    const [checkedFlags, setCheckedFlags] = useState([]);
    const [showHover, setShowHover] = useState(false);
    const [triageAnswers, setTriageAnswers] = useState({});
    const [buildAnswers, setBuildAnswers] = useState({ lure: null, urgency: null });

    const [modal, setModal] = useState({ show: false, title: '', content: '' });

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

    // Check completion
    if (currentIndex >= questions.length && questions.length > 0) {
        // Clear saved progress on completion
        localStorage.removeItem(`cyberduo_inprogress_${gameKey}_${level}`);
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
        
        if (currentIndex > highestCompletedIndex) {
            setHighestCompletedIndex(currentIndex);
        }

        if (isCorrect) {
            setFeedback({ type: 'success', message: 'Correct! (+20 XP)' });
            setScore(prev => prev + 20);
            setXp(prev => prev + 20);
        } else {
            setFeedback({ type: 'error', message: currentQ.explain });
            // Deduct XP points
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

    // Submission logic
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

    // Render Question Formats
    const renderQuestionFormat = () => {
        switch (currentQ.format) {
            case 'spot_fake':
                return (
                    <div className="gs-format gs-spot-fake">
                        {currentQ.options.map((opt, i) => (
                            <div 
                                key={i} 
                                className={`gs-option-card ${selectedOption === opt ? 'selected' : ''}`}
                                onClick={() => setSelectedOption(opt)}
                            >
                                <span className="gs-sender-icon">👤</span> {opt}
                            </div>
                        ))}
                    </div>
                );
            case 'decision_simulator':
                return (
                    <div className="gs-format gs-decision-sim">
                        {currentQ.options.map((opt, i) => (
                            <button 
                                key={i} 
                                className={`gs-option-btn ${selectedOption === opt ? 'selected' : ''}`}
                                onClick={() => setSelectedOption(opt)}
                            >
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
                                    <button 
                                        key={i} 
                                        className={`gs-chat-reply-btn ${selectedOption === opt ? 'selected' : ''}`}
                                        onClick={() => setSelectedOption(opt)}
                                    >
                                        {opt}
                                    </button>
                                ))}
                            </div>
                        </div>
                    </div>
                );
            case 'drag_flags':
                const handleDragStart = (e, flag) => {
                    e.dataTransfer.setData('flag', flag);
                };
                const handleDrop = (e) => {
                    e.preventDefault();
                    const flag = e.dataTransfer.getData('flag');
                    if (flag && !droppedFlags.includes(flag)) {
                        setDroppedFlags([...droppedFlags, flag]);
                    }
                };
                const handleDragOver = (e) => e.preventDefault();

                return (
                    <div className="gs-format gs-drag-flags">
                        <div className="gs-email-mockup" style={{ whiteSpace: 'pre-wrap' }}>
                            {currentQ.emailContent}
                        </div>
                        <div className="gs-drag-area">
                            <div className="gs-flags-source">
                                <h4>Available Flags</h4>
                                {currentQ.redFlags.filter(f => !droppedFlags.includes(f)).map((flag, i) => (
                                    <div 
                                        key={i} 
                                        draggable 
                                        onDragStart={(e) => handleDragStart(e, flag)}
                                        className="gs-draggable-flag"
                                    >
                                        🚩 {flag}
                                    </div>
                                ))}
                            </div>
                            <div 
                                className="gs-drop-zone"
                                onDrop={handleDrop}
                                onDragOver={handleDragOver}
                            >
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
                                // First two parts are headers (sender, subject), rest are body
                                const rowClass = i <= 1 ? 'header-row' : 'body-row';
                                return (
                                    <div 
                                        key={i} 
                                        className={`gs-email-part ${rowClass} ${checkedFlags.includes(part.id) ? 'highlighted' : ''}`}
                                        onClick={() => {
                                            if (checkedFlags.includes(part.id)) {
                                                setCheckedFlags(checkedFlags.filter(id => id !== part.id));
                                            } else {
                                                setCheckedFlags([...checkedFlags, part.id]);
                                            }
                                        }}
                                    >
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
                                    <button 
                                        className={`gs-btn-keep ${triageAnswers[email.id] === false ? 'selected' : ''}`}
                                        onClick={() => setTriageAnswers({ ...triageAnswers, [email.id]: false })}
                                    >KEEP</button>
                                    <button 
                                        className={`gs-btn-delete ${triageAnswers[email.id] === true ? 'selected' : ''}`}
                                        onClick={() => setTriageAnswers({ ...triageAnswers, [email.id]: true })}
                                    >DELETE</button>
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
                                    <button 
                                        key={i} 
                                        className={`gs-build-btn ${buildAnswers.lure?.text === lure.text ? 'selected' : ''}`}
                                        onClick={() => setBuildAnswers({ ...buildAnswers, lure })}
                                    >
                                        {lure.text}
                                    </button>
                                ))}
                            </div>
                        </div>
                        <div className="gs-build-section">
                            <h5>2. Select Urgency Tactic</h5>
                            <div className="gs-build-options">
                                {currentQ.urgencies.map((urgency, i) => (
                                    <button 
                                        key={i} 
                                        className={`gs-build-btn ${buildAnswers.urgency?.text === urgency.text ? 'selected' : ''}`}
                                        onClick={() => setBuildAnswers({ ...buildAnswers, urgency })}
                                    >
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
                        <div className="gs-link-container" 
                             onMouseEnter={() => setShowHover(true)} 
                             onMouseLeave={() => setShowHover(false)}>
                            <span className="gs-fake-link">{currentQ.displayedLink}</span>
                            {showHover && (
                                <div className="gs-hover-tooltip">
                                    {currentQ.actualDestination}
                                </div>
                            )}
                        </div>
                        <div className="gs-inspector-actions">
                            <button 
                                className={`gs-btn-safe ${selectedOption === 'Safe' ? 'selected' : ''}`}
                                onClick={() => setSelectedOption('Safe')}
                            >
                                ✔ SAFE
                            </button>
                            <button 
                                className={`gs-btn-phish ${selectedOption === 'Phishing' ? 'selected' : ''}`}
                                onClick={() => setSelectedOption('Phishing')}
                            >
                                ⚠ PHISHING
                            </button>
                        </div>
                    </div>
                );
            case 'case_study':
                return (
                    <div className="gs-format gs-case-study">
                        <div className="gs-email-mockup" style={{ whiteSpace: 'pre-wrap' }}>
                            {currentQ.emailContent}
                        </div>
                        <div className="gs-checklist">
                            {currentQ.redFlags.map((flag, i) => (
                                <label key={i} className="gs-checkbox-label">
                                    <input 
                                        type="checkbox" 
                                        checked={checkedFlags.includes(flag)}
                                        onChange={(e) => {
                                            if (e.target.checked) setCheckedFlags([...checkedFlags, flag]);
                                            else setCheckedFlags(checkedFlags.filter(f => f !== flag));
                                        }}
                                    />
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
                    <div className="gs-timer-badge" style={{color: timeLeft <= 10 ? '#ff6b6b' : '#00FF9D'}}>
                        ⏱ {timeLeft}s
                    </div>
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
                
                {feedback && (
                    <div className={`gs-feedback ${feedback.type}`}>
                        {feedback.message}
                    </div>
                )}
                
                <div className="gs-actions-row">
                    {currentIndex > 0 && (
                        <button className="gs-btn-prev" onClick={handlePrevQuestion}>
                            🡄 PREVIOUS
                        </button>
                    )}
                    {(!hasAnswered && !isAlreadyCompleted) ? (
                        <button className="gs-btn-submit" style={{ margin: 0, minWidth: 'auto', padding: '15px 40px' }} onClick={handleSubmit}>
                            SUBMIT ANSWER
                        </button>
                    ) : (
                        <>
                            {(!isCorrectResult || isAlreadyCompleted) && (
                                <button className="gs-btn-reveal-answer" onClick={() => showModal('Correct Answer', currentQ.reveal || currentQ.explain)}>
                                    👁️ SHOW ANSWER
                                </button>
                            )}
                            <button className="gs-btn-next" onClick={handleNextQuestion}>
                                NEXT ➔
                            </button>
                        </>
                    )}
                </div>
            </div>

            <div className="gs-ai-toolbar">
                <button onClick={() => showModal('Hint 💡', currentQ.hint)}>💡 Hint</button>
                <button onClick={() => showModal('Explain 📚', currentQ.explain)}>📚 Explain</button>
                <button onClick={() => showModal('AI Agent Chat 💬', 'Agent Chat module is currently offline. Check back in a future update.')}>💬 Chat</button>
            </div>

            {/* AI Modal */}
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
