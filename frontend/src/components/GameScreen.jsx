import React, { useState, useEffect } from 'react';
import '../styles/gamescreen.css';
// import gameData from '../data/GameQuestions.json'; // Now fetching from DB
import { updateStreak } from '../utils/gameProgress.js';
import { incrementDailyProgress } from '../utils/dailyprogress.js';

export default function GameScreen({ gameKey = "phishing", gameName, level, onComplete, onProgressUpdate, onBack, userId }) {
    const [questions, setQuestions] = useState([]);
    const API_BASE_URL = "http://localhost:5000";

    // ✅ ALL STATE HOOKS MUST BE DECLARED BEFORE ANY EARLY RETURNS (React rules)
    const [loadingError, setLoadingError] = useState(false);

    // Restore progress from localStorage
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

    const GEMINI_API_KEY = import.meta.env.VITE_GEMINI_API_KEY;

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
                `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${GEMINI_API_KEY}`,
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

    const isPaused = modal.show || chatOpen;

    useEffect(() => {
        if (hasAnswered || currentIndex >= questions.length || !currentQ || isPaused) return;
        if (timeLeft <= 0) {
            handleTimeUp();
            return;
        }
        const timerId = setInterval(() => {
            setTimeLeft(prev => prev - 1);
        }, 1000);
        return () => clearInterval(timerId);
    }, [timeLeft, hasAnswered, currentIndex, currentQ, questions.length, isPaused]);

    // ✅ FETCH QUESTIONS FROM DB — hook must appear here, before any conditional returns
    useEffect(() => {
        async function fetchQuestions() {
            setLoadingError(false);
            try {
                const res = await fetch(`${API_BASE_URL}/game/questions/${gameKey}/${level}`);
                if (!res.ok) throw new Error("Failed to fetch");
                const data = await res.json();
                if (Array.isArray(data) && data.length > 0) {
                    setQuestions(data);
                } else {
                    setLoadingError(true);
                }
            } catch (e) {
                console.error("Failed to fetch questions from DB", e);
                setLoadingError(true);
            }
        }
        fetchQuestions();
    }, [gameKey, level]);

    // ✅ COMPLETION SCREEN — placed after all hook declarations
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
                    <button className="gs-btn-primary" onClick={() => {
                        try { onComplete(xp, score); } catch(e) { console.error(e); onBack?.(); }
                    }}>CONTINUE TO DASHBOARD</button>
                </div>
            </div>
        );
    }

    if (loadingError) {
        return (
            <div className="gs-container">
                <div className="gs-completion-screen">
                    <h1 className="gs-neon-title" style={{ color: '#ff6b6b' }}>Link Failed</h1>
                    <p>Intel for {gameKey} ({level}) could not be retrieved from the mainframe.</p>
                    <button className="gs-btn-primary" onClick={onBack}>RETURN TO BASE</button>
                </div>
            </div>
        );
    }

    if (questions.length === 0) {
        return (
            <div className="gs-container">
                <div className="gs-completion-screen">
                    <h1 className="gs-neon-title">Establishing Link...</h1>
                    <p>Accessing the CyberDuo secure database. Stand by, operative.</p>
                </div>
            </div>
        );
    }

    if (!currentQ && questions.length > 0) return (
        <div className="gs-container">
            <div className="gs-completion-screen">
                <h1 className="gs-neon-title">Analysis Complete</h1>
                <p>All available intel for this sector has been processed.</p>
                <button className="gs-btn-primary" onClick={() => onComplete(xp, score)}>RETURN TO BASE</button>
            </div>
        </div>
    );

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
            incrementDailyProgress(); // Update local storage
            
            // ✅ PERSIST TO DB IN REAL-TIME
            if (userId) {
                // Sync Streak
                fetch(`${API_BASE_URL}/user/update-streak`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ user_id: userId })
                }).catch(e => console.error("Streak sync failed", e));

                // Sync Question Progress
                fetch(`${API_BASE_URL}/game/save-result`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        user_id: userId,
                        game_key: gameKey,
                        level: level,
                        xp_earned: 20,
                        score: score + 20, // Use actual current score
                        is_single_question: true,
                        question_index: currentIndex // Pass current question index
                    })
                })
                .then(res => res.json())
                .then((data) => {
                    // ✅ Sync local XP EXACTLY with what the backend calculated
                    if (data.new_xp !== undefined) {
                        localStorage.setItem('userXP', data.new_xp.toString());
                    }
                    // ✅ Trigger UI to refresh XP and Leaderboard
                    window.dispatchEvent(new Event('xpUpdated'));
                    window.dispatchEvent(new Event('leaderboardRefresh'));
                }).catch(e => console.error("DB Sync failed", e));

                // ✅ Sync Daily Mission Counter (Real-Time)
                const dailyData = JSON.parse(localStorage.getItem('cyberduo_daily_progress') || '{"count": 0}');
                fetch(`${API_BASE_URL}/user/sync-daily`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        user_id: userId,
                        count: dailyData.count
                    })
                }).catch(e => console.error("Daily mission sync failed", e));
            }
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
        // Adaptive Inbox custom state
        if (currentQ?.format === 'adaptive_inbox') {
            setBuildAnswers({ currentIndex: 0 }); // reuse buildAnswers for local state if needed, or just add adaptiveIndex
        }
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
        
        let isInputMissing = false;
        // ✅ VALIDATION FEEDBACK
        if (currentQ.format === 'spot_fake' || currentQ.format === 'decision_simulator' || currentQ.format === 'chat_sim' || currentQ.format === 'spot_weak' || currentQ.format === 'scenario_mcq' || currentQ.format === 'link_inspector' || currentQ.format === 'file_inspector' || currentQ.format === 'quishing_drills' || currentQ.format === 'deepfake_detection' || currentQ.format === 'spot_the_difference' || currentQ.format === 'digital_whodunnit' || currentQ.format === 'branching_narratives' || currentQ.format === 'resource_management' || currentQ.format === 'the_imposter' || currentQ.format === 'cyber_snakes_ladders' || currentQ.format === 'phish_a_friend' || currentQ.format === 'adversary_roleplay' || currentQ.format === 'kc7_log_hunt' || currentQ.format === 'kahoot_trivia') {
            if (!selectedOption) isInputMissing = true;
        } else if (currentQ.format === 'escape_rooms') {
            if (!chatInput) isInputMissing = true;
        } else if (currentQ.format === 'svg_code_inspection') {
            if (!selectedOption) isInputMissing = true;
        } else if (currentQ.format === 'omni_threat_chains') {
            if (!selectedOption) isInputMissing = true;
        } else if (currentQ.format === 'password_builder' || currentQ.format === 'drag_flags' || currentQ.format === 'authenticator_sim' || currentQ.format === 'threat_router') {
            if (droppedFlags.length === 0) isInputMissing = true;
        } else if (currentQ.format === 'case_study' || currentQ.format === 'select_all' || currentQ.format === 'click_flags' || currentQ.format === 'omni_threat_chain' || currentQ.format === 'scavenger_hunt' || currentQ.format === 'adversary_roleplay') {
            if (checkedFlags.length === 0) isInputMissing = true;
        } else if (currentQ.format === 'inbox_triage' || currentQ.format === 'file_triage' || currentQ.format === 'traffic_triage' || currentQ.format === 'password_triage' || currentQ.format === 'adaptive_inbox') {
            if (Object.keys(triageAnswers).length < (currentQ.emails?.length || currentQ.files?.length || currentQ.passwords?.length)) isInputMissing = true;
        } else if (currentQ.format === 'build_phish') {
            if (!buildAnswers.lure || !buildAnswers.urgency) isInputMissing = true;
        }

        if (isInputMissing) {
            // Allow submitting with no answer — just treat it as wrong
            handleAnswerEval(false);
            return;
        }

        let isCorrect = false;
        if (currentQ.format === 'spot_fake' || currentQ.format === 'decision_simulator' || currentQ.format === 'chat_sim' || currentQ.format === 'spot_weak' || currentQ.format === 'scenario_mcq' || currentQ.format === 'deepfake_detection' || currentQ.format === 'spot_the_difference' || currentQ.format === 'digital_whodunnit' || currentQ.format === 'branching_narratives' || currentQ.format === 'resource_management' || currentQ.format === 'the_imposter' || currentQ.format === 'cyber_snakes_ladders' || currentQ.format === 'phish_a_friend' || currentQ.format === 'quishing_drills' || currentQ.format === 'quishing_drill' || currentQ.format === 'kc7_log_hunt' || currentQ.format === 'kahoot_trivia') {
            isCorrect = selectedOption === currentQ.correctAnswer;
        } else if (currentQ.format === 'adversary_roleplay') {
            // Check if multiple flags were used or single selection
            if (currentQ.assets && checkedFlags.length > 0) {
                 const totalCost = checkedFlags.reduce((sum, id) => sum + (currentQ.assets.find(a => a.id === id)?.cost || 0), 0);
                 const totalVal = checkedFlags.reduce((sum, id) => sum + (currentQ.assets.find(a => a.id === id)?.value || 0), 0);
                 isCorrect = totalCost <= currentQ.budget && totalVal >= currentQ.targetValue;
            } else {
                 const asset = currentQ.assets.find(a => a.name === selectedOption);
                 isCorrect = asset && asset.value >= currentQ.targetValue;
            }
        } else if (currentQ.format === 'omni_threat_chains' || currentQ.format === 'omni_threat_chain') {
            isCorrect = selectedOption === currentQ.correctAnswer;
        } else if (currentQ.format === 'escape_rooms') {
            isCorrect = chatInput.trim().toUpperCase() === currentQ.correctAnswer.toUpperCase();
        } else if (currentQ.format === 'svg_code_inspection') {
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
        } else if (currentQ.format === 'link_inspector' || currentQ.format === 'file_inspector' || currentQ.format === 'quishing_drill') {
            isCorrect = selectedOption === currentQ.correctAnswer;
        } else if (currentQ.format === 'case_study' || currentQ.format === 'select_all') {
            const correctSet = new Set(currentQ.correctFlags);
            const userSet = new Set(checkedFlags);
            isCorrect = correctSet.size > 0 && correctSet.size === userSet.size && [...correctSet].every(flag => userSet.has(flag));
        } else if (currentQ.format === 'click_flags') {
            const correctFlags = currentQ.emailParts.filter(p => p.isFlag);
            isCorrect = checkedFlags.length === correctFlags.length && checkedFlags.every(id => currentQ.emailParts.find(p => p.id === id)?.isFlag);
        } else if (currentQ.format === 'omni_threat_chain' || currentQ.format === 'omni_threat_chains' && checkedFlags.length > 0) {
            const correctFlags = currentQ.channels.flatMap(c => c.parts).filter(p => p.isFlag);
            isCorrect = checkedFlags.length === correctFlags.length && checkedFlags.every(id => currentQ.channels.flatMap(c => c.parts).find(p => p.id === id)?.isFlag);
        } else if (currentQ.format === 'scavenger_hunt' || currentQ.format === 'capture_the_flag') {
            const correctFlags = currentQ.objects.filter(o => o.isRedFlag || o.isFlag);
            isCorrect = checkedFlags.length === correctFlags.length && checkedFlags.every(id => {
                const found = currentQ.objects.find(o => o.id === (id.id || id) || o.id === id);
                return found && (found.isRedFlag || found.isFlag);
            });
        } else if (currentQ.format === 'inbox_triage' || currentQ.format === 'adaptive_inbox') {
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
                        {currentQ.options.map((opt, i) => {
                            const isSelected = selectedOption === opt;
                            const isWrong = hasAnswered && isSelected && !isCorrectResult;
                            const isCorrect = hasAnswered && opt === currentQ.correctAnswer;
                            const statusClass = isCorrect ? 'correct-answer' : (isWrong ? 'wrong-answer' : '');
                            return (
                                <button key={i} className={`gs-mcq-card ${isSelected ? 'selected' : ''} ${statusClass}`} onClick={() => !hasAnswered && setSelectedOption(opt)}>
                                    <div className="gs-option-letter">{String.fromCharCode(65 + i)}</div>
                                    <div className="gs-option-text">{opt}</div>
                                </button>
                            );
                        })}
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
            case 'omni_threat_chain':
                return (
                    <div className="gs-format gs-omni-chain" style={{ display: 'flex', gap: '20px' }}>
                        {currentQ.channels.map((channel, cIdx) => (
                            <div key={cIdx} className="gs-channel-box" style={{ flex: 1, background: 'rgba(255,255,255,0.05)', borderRadius: '10px', padding: '15px', border: '1px solid rgba(0, 255, 157, 0.2)' }}>
                                <div style={{ fontSize: '1.2rem', marginBottom: '10px', color: '#00FF9D', borderBottom: '1px solid rgba(0,255,157,0.3)', paddingBottom: '5px' }}>{channel.type.toUpperCase()}</div>
                                <div className="gs-channel-content">
                                    {channel.parts.map((part, pIdx) => (
                                        <span key={pIdx} className={`gs-channel-part ${checkedFlags.includes(part.id) ? 'highlighted' : ''}`}
                                            style={{ cursor: 'pointer', padding: '2px 5px', borderRadius: '4px', backgroundColor: checkedFlags.includes(part.id) ? 'rgba(255,107,107,0.4)' : 'transparent' }}
                                            onClick={() => {
                                                if (checkedFlags.includes(part.id)) setCheckedFlags(checkedFlags.filter(id => id !== part.id));
                                                else setCheckedFlags([...checkedFlags, part.id]);
                                            }}>
                                            {part.text}{' '}
                                        </span>
                                    ))}
                                </div>
                            </div>
                        ))}
                    </div>
                );
            case 'scavenger_hunt':
                return (
                    <div className="gs-format gs-scavenger-hunt">
                        <div style={{ position: 'relative', width: '100%', height: '300px', background: '#111', border: '1px solid #444', borderRadius: '10px', overflow: 'hidden' }}>
                            {currentQ.objects && currentQ.objects.length > 0 ? currentQ.objects.map((obj, i) => (
                                <div key={obj.id} 
                                    className={`gs-hunt-obj ${checkedFlags.includes(obj.id) ? 'highlighted' : ''}`}
                                    style={{ position: 'absolute', top: obj.top, left: obj.left, padding: '10px', background: checkedFlags.includes(obj.id) ? 'rgba(255,107,107,0.9)' : 'rgba(34,34,34,0.9)', border: '2px dashed', borderColor: checkedFlags.includes(obj.id) ? '#ff6b6b' : '#00FF9D', borderRadius: '8px', cursor: 'pointer', color: '#fff', zIndex: 10, display: 'flex', alignItems: 'center', gap: '8px', minWidth: '100px', boxShadow: '0 4px 6px rgba(0,0,0,0.3)' }}
                                    onClick={() => {
                                        if (checkedFlags.includes(obj.id)) setCheckedFlags(checkedFlags.filter(id => id !== obj.id));
                                        else setCheckedFlags([...checkedFlags, obj.id]);
                                    }}>
                                    <span style={{ fontSize: '1.5rem' }}>{obj.icon}</span> 
                                    <span style={{ fontWeight: 'bold' }}>{obj.label}</span>
                                </div>
                            )) : <div style={{ color: '#ff6b6b', padding: '20px' }}>Loading environment targets...</div>}
                        </div>
                    </div>
                );
            case 'adversary_roleplay':
                const spent = checkedFlags.reduce((sum, id) => sum + (currentQ.assets.find(a => a.id === id)?.cost || 0), 0);
                const val = checkedFlags.reduce((sum, id) => sum + (currentQ.assets.find(a => a.id === id)?.value || 0), 0);
                return (
                    <div className="gs-format gs-roleplay">
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '20px', padding: '15px', background: 'rgba(255,107,107,0.1)', border: '1px solid #ff6b6b', borderRadius: '10px' }}>
                            <div style={{ color: '#ff6b6b' }}><strong>Attacker Budget:</strong> {currentQ.budget - spent} / {currentQ.budget}</div>
                            <div style={{ color: '#00FF9D' }}><strong>Threat Value:</strong> {val} / {currentQ.targetValue} Target</div>
                        </div>
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px' }}>
                            {currentQ.assets.map(asset => (
                                <div key={asset.id} 
                                    style={{ padding: '15px', border: checkedFlags.includes(asset.id) ? '2px solid #ff6b6b' : '1px solid #444', borderRadius: '8px', cursor: 'pointer', opacity: (spent + asset.cost > currentQ.budget && !checkedFlags.includes(asset.id)) ? 0.5 : 1 }}
                                    onClick={() => {
                                        if (checkedFlags.includes(asset.id)) setCheckedFlags(checkedFlags.filter(id => id !== asset.id));
                                        else if (spent + asset.cost <= currentQ.budget) setCheckedFlags([...checkedFlags, asset.id]);
                                    }}>
                                    <div style={{ fontWeight: 'bold' }}>{asset.name}</div>
                                    <div style={{ fontSize: '0.9rem', color: '#888' }}>Cost: {asset.cost} | Value: {asset.value}</div>
                                </div>
                            ))}
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
            case 'adaptive_inbox':
                const activeEmailIdx = Object.keys(triageAnswers).length;
                const activeEmail = currentQ.emails[activeEmailIdx];
                return (
                    <div className="gs-format gs-adaptive-inbox">
                        {activeEmail ? (
                            <div className="gs-inbox-card" style={{ maxWidth: '400px', margin: '0 auto', background: '#222', padding: '20px', borderRadius: '15px', border: '1px solid #444', textAlign: 'center' }}>
                                <div style={{ fontSize: '0.9rem', color: '#888', marginBottom: '15px' }}>Email {activeEmailIdx + 1} of {currentQ.emails.length}</div>
                                <div style={{ fontSize: '1.2rem', fontWeight: 'bold' }}>{activeEmail.subject}</div>
                                <div style={{ margin: '10px 0', padding: '10px', background: '#111', borderRadius: '8px' }}>From: {activeEmail.sender}</div>
                                
                                <div style={{ display: 'flex', gap: '15px', marginTop: '20px', justifyContent: 'center' }}>
                                    <button className="gs-btn-keep" onClick={() => setTriageAnswers({ ...triageAnswers, [activeEmail.id]: false })} style={{ flex: 1, padding: '15px', fontSize: '1.2rem', border: '2px solid #00FF9D', background: 'transparent', color: '#00FF9D', borderRadius: '8px', cursor: 'pointer' }}>SAFE</button>
                                    <button className="gs-btn-delete" onClick={() => setTriageAnswers({ ...triageAnswers, [activeEmail.id]: true })} style={{ flex: 1, padding: '15px', fontSize: '1.2rem', border: '2px solid #ff6b6b', background: 'transparent', color: '#ff6b6b', borderRadius: '8px', cursor: 'pointer' }}>PHISH</button>
                                </div>
                            </div>
                        ) : (
                            <div style={{ textAlign: 'center', color: '#00FF9D', fontSize: '1.2rem' }}>Inbox cleared! Submit your report.</div>
                        )}
                        <div style={{ marginTop: '20px', display: 'flex', gap: '5px', justifyContent: 'center' }}>
                            {currentQ.emails.map((e, i) => (
                                <div key={e.id} style={{ width: '20px', height: '6px', backgroundColor: triageAnswers[e.id] !== undefined ? '#555' : '#222', borderRadius: '3px' }}></div>
                            ))}
                        </div>
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
            case 'quishing_drill':
                return (
                    <div className="gs-format gs-link-inspector gs-quishing">
                        <div className="gs-quishing-object" style={{ textAlign: 'center', padding: '20px', border: '1px solid #444', borderRadius: '15px', background: '#222', maxWidth: '300px', margin: '0 auto 20px' }}>
                            <div style={{ fontSize: '1.2rem', marginBottom: '15px' }}>{currentQ.qrObject}</div>
                            <div className="gs-qr-mockup" style={{ width: '150px', height: '150px', margin: '0 auto', background: `radial-gradient(circle, #fff 20%, transparent 20%), radial-gradient(circle, transparent 20%, #fff 20%, transparent 30%), radial-gradient(circle, #fff 15%, transparent 15%), linear-gradient(#111 2px, transparent 2px), linear-gradient(90deg, #111 2px, transparent 2px)`, backgroundSize: '15px 15px', border: '10px solid #fff', borderRadius: '5px' }}></div>
                            <button onClick={() => setShowHover(true)} style={{ marginTop: '15px', padding: '10px 20px', background: '#00FF9D', color: '#111', border: 'none', borderRadius: '5px', fontWeight: 'bold', cursor: 'pointer' }}>SCAN QR CODE</button>
                        </div>
                        
                        {showHover && (
                            <div style={{ textAlign: 'center', margin: '20px 0' }}>
                                <div style={{ color: '#00FF9D', marginBottom: '5px' }}>Scanner Output:</div>
                                <div style={{ fontSize: '1.1rem', background: '#111', padding: '10px', borderRadius: '5px', wordBreak: 'break-all' }}>{currentQ.decodedURL}</div>
                            </div>
                        )}
                        
                        <div className="gs-inspector-actions" style={{ opacity: showHover ? 1 : 0.8 }}>
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
                                    <strong style={{ fontFamily: 'monospace', letterSpacing: '2px', fontSize: '1.2rem' }}>{pw.text}</strong>
                                </div>
                                <div className="gs-triage-actions">
                                    <button className={`gs-btn-keep ${triageAnswers[pw.id] === true ? 'selected' : ''}`} onClick={() => setTriageAnswers({ ...triageAnswers, [pw.id]: true })}>STRONG 🛡️</button>
                                    <button className={`gs-btn-delete ${triageAnswers[pw.id] === false ? 'selected' : ''}`} style={{ borderColor: 'rgba(255, 107, 107, 0.3)' }} onClick={() => setTriageAnswers({ ...triageAnswers, [pw.id]: false })}>WEAK ⚠️</button>
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
            case 'quishing_drills':
                return (
                    <div className="gs-format gs-quishing">
                        <div className="gs-phone-mockup">
                            <div className="gs-qr-scanner">
                                <div className="gs-qr-code-placeholder">
                                    <div className="gs-qr-overlay"></div>
                                </div>
                                <div className="gs-scanned-result">
                                    <span className="gs-res-label">SCANNED URL:</span>
                                    <code className="gs-decoded-url">{currentQ.decodedURL}</code>
                                </div>
                            </div>
                        </div>
                        <div className="gs-mcq-grid" style={{ marginTop: '20px' }}>
                            {(currentQ.options || ['Safe', 'Phishing']).map((opt, i) => (
                                <button key={i} className={`gs-mcq-card ${selectedOption === opt ? 'selected' : ''}`} onClick={() => setSelectedOption(opt)}>
                                    {opt}
                                </button>
                            ))}
                        </div>
                    </div>
                );

            case 'omni_threat_chains':
                return (
                    <div className="gs-format gs-threat-chain">
                        <div className="gs-chain-visual">
                            {currentQ.channels.map((ch, idx) => (
                                <div key={idx} className="gs-chain-channel">
                                    <div className="gs-channel-type">{ch.type} ATTACK</div>
                                    <div className="gs-channel-bubble">
                                        {ch.parts.map(p => (
                                            <span 
                                                key={p.id} 
                                                className={`gs-chain-part ${selectedOption === p.text ? 'selected' : ''} ${p.isFlag && hasAnswered ? (isCorrect ? 'correct' : 'malicious') : ''}`}
                                                onClick={() => setSelectedOption(p.text)}
                                            >
                                                {p.text}
                                            </span>
                                        ))}
                                    </div>
                                    {idx < currentQ.channels.length - 1 && <div className="gs-chain-link">➔</div>}
                                </div>
                            ))}
                        </div>
                        <p className="gs-instruction-mini">Identify the malicious payload in the multi-channel attack chain.</p>
                    </div>
                );
            case 'deepfake_detection':
                return (
                    <div className="gs-format gs-deepfake">
                        <div className="gs-deepfake-visual">
                            <div className="gs-video-placeholder">
                                <div className="gs-audio-wave">
                                    {[...Array(20)].map((_, i) => (
                                        <div key={i} className="gs-wave-bar" style={{ animationDelay: `${i * 0.1}s` }}></div>
                                    ))}
                                </div>
                                <div className="gs-glitch-overlay"></div>
                                <p>ENCRYPTED CEO FEED</p>
                            </div>
                        </div>
                        <div className="gs-transcript">
                            <strong>Transcript:</strong> "{currentQ.audioTranscript}"
                        </div>
                        <div className="gs-mcq-grid">
                            {currentQ.options.map((opt, i) => (
                                <button key={i} className={`gs-mcq-card ${selectedOption === opt ? 'selected' : ''}`} onClick={() => setSelectedOption(opt)}>
                                    {opt}
                                </button>
                            ))}
                        </div>
                    </div>
                );
            case 'svg_code_inspection':
                return (
                    <div className="gs-format gs-svg-inspection">
                        <div className="gs-code-block">
                            <pre>
                                {currentQ.codeLines.map((line) => (
                                    <div 
                                        key={line.id} 
                                        className={`gs-code-line ${selectedOption === line.id ? 'highlighted' : ''}`}
                                        onClick={() => setSelectedOption(line.id)}
                                    >
                                        <span className="gs-line-num">{line.id}</span>
                                        <code>{line.text}</code>
                                    </div>
                                ))}
                            </pre>
                        </div>
                        <p className="gs-instruction-mini">Click the line containing the malicious payload.</p>
                    </div>
                );
            case 'spot_the_difference':
                return (
                    <div className="gs-format gs-spot-diff">
                        <div className="gs-diff-cards">
                            <div className="gs-diff-card">
                                <div className="gs-card-header">Target Brand: {currentQ.brandName}</div>
                                <div className="gs-card-url">URL: {currentQ.urlReal}</div>
                                <div className="gs-login-form-mock">
                                    <div className="gs-input-mock">Username</div>
                                    <div className="gs-input-mock">Password</div>
                                    <div className="gs-btn-mock">Sign In</div>
                                </div>
                            </div>
                            <div className="gs-diff-card">
                                <div className="gs-card-header">Target Brand: {currentQ.brandName}</div>
                                <div className="gs-card-url" style={{ color: '#ffb020' }}>URL: {currentQ.urlFake}</div>
                                <div className="gs-login-form-mock">
                                    <div className="gs-input-mock">Username</div>
                                    <div className="gs-input-mock">Password</div>
                                    <div className="gs-btn-mock">Sign In</div>
                                </div>
                            </div>
                        </div>
                        <div className="gs-mcq-grid" style={{ marginTop: '20px' }}>
                            {currentQ.options.map((opt, i) => {
                                const isSelected = selectedOption === opt;
                                const isWrong = hasAnswered && isSelected && !isCorrectResult;
                                const isCorrect = hasAnswered && opt === currentQ.correctAnswer;
                                const statusClass = isCorrect ? 'correct-answer' : (isWrong ? 'wrong-answer' : '');
                                return (
                                    <button key={i} className={`gs-mcq-card ${isSelected ? 'selected' : ''} ${statusClass}`} onClick={() => !hasAnswered && setSelectedOption(opt)}>
                                        <div className="gs-option-letter">{String.fromCharCode(65 + i)}</div>
                                        <div className="gs-option-text">{opt}</div>
                                    </button>
                                );
                            })}
                        </div>
                    </div>
                );
            case 'digital_whodunnit':
                return (
                    <div className="gs-format gs-whodunnit">
                        <div className="gs-header-table">
                            <div className="gs-table-head">
                                <span>FROM</span>
                                <span>SPF</span>
                                <span>DKIM</span>
                            </div>
                            {currentQ.emails.map(email => (
                                <div key={email.id} className={`gs-table-row ${selectedOption === email.from ? 'selected' : ''}`} onClick={() => setSelectedOption(email.from)}>
                                    <span>{email.from}</span>
                                    <span style={{ color: email.spf === 'PASS' ? '#00FF9D' : '#ff6b6b' }}>{email.spf}</span>
                                    <span style={{ color: email.dkim === 'PASS' ? '#00FF9D' : '#ff6b6b' }}>{email.dkim}</span>
                                </div>
                            ))}
                        </div>
                        <p className="gs-instruction-mini">Select the imposter email based on header evidence.</p>
                    </div>
                );
            case 'escape_rooms':
                return (
                    <div className="gs-format gs-escape-room">
                        <div className="gs-cipher-box">
                            <div className="gs-cipher-display">{currentQ.cipherText}</div>
                            <div className="gs-cipher-tip">HINT: CAESAR SHIFT +3 (A→D)</div>
                        </div>
                        <div className="gs-terminal-input">
                            <span className="gs-prompt">{'>'}</span>
                            <input 
                                type="text" 
                                value={chatInput} 
                                onChange={(e) => setChatInput(e.target.value)} 
                                placeholder="ENTER DECODED FLAG..."
                                className="gs-terminal-field"
                            />
                        </div>
                    </div>
                );
            case 'branching_narratives':
            case 'resource_management':
            case 'the_imposter':
            case 'cyber_snakes_ladders':
            case 'phish_a_friend':
                return (
                    <div className="gs-format gs-mcq-grid">
                        {currentQ.scenario && <div className="gs-scenario-text">{currentQ.scenario}</div>}
                        {currentQ.messages && (
                            <div className="gs-imposter-chat">
                                {currentQ.messages.map((msg, i) => (
                                    <div key={i} className={`gs-chat-bubble ${selectedOption === msg.sender ? 'selected' : ''}`} onClick={() => setSelectedOption(msg.sender)}>
                                        <strong>{msg.sender}:</strong> {msg.text}
                                    </div>
                                ))}
                            </div>
                        )}
                        <div className="gs-options-list" style={{ width: '100%' }}>
                            {(currentQ.options || []).map((opt, i) => (
                                <button key={i} className={`gs-mcq-card ${selectedOption === opt ? 'selected' : ''}`} onClick={() => setSelectedOption(opt)}>
                                    {opt}
                                </button>
                            ))}
                        </div>
                    </div>
                );
            case 'capture_the_flag':
                return (
                    <div className="gs-format gs-scavenger-hunt">
                        <div style={{ position: 'relative', width: '100%', height: '300px', background: '#111', border: '1px solid #444', borderRadius: '10px', overflow: 'hidden' }}>
                            {currentQ.objects.map((obj) => (
                                <div key={obj.id} 
                                    className={`gs-hunt-obj ${checkedFlags.includes(obj.id) ? 'highlighted' : ''}`}
                                    style={{ position: 'absolute', top: obj.top, left: obj.left, padding: '10px', background: checkedFlags.includes(obj.id) ? 'rgba(255,107,107,0.9)' : 'rgba(34,34,34,0.9)', border: '2px dashed', borderColor: checkedFlags.includes(obj.id) ? '#ff6b6b' : '#00FF9D', borderRadius: '8px', cursor: 'pointer', color: '#fff', zIndex: 10, display: 'flex', alignItems: 'center', gap: '8px', minWidth: '100px', boxShadow: '0 4px 6px rgba(0,0,0,0.3)' }}
                                    onClick={() => {
                                        if (checkedFlags.includes(obj.id)) setCheckedFlags(checkedFlags.filter(id => id !== obj.id));
                                        else setCheckedFlags([...checkedFlags, obj.id]);
                                    }}>
                                    <span style={{ fontSize: '1.5rem' }}>{obj.icon}</span> 
                                    <span style={{ fontWeight: 'bold' }}>{obj.label}</span>
                                </div>
                            ))}
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
                                <div key={portal.id} style={{ cursor: 'pointer' }} className={`gs-portal ${droppedFlags.includes(portal.id) ? 'active' : ''}`} onClick={() => handleTogglePortal(portal.id)}>
                                    <div className="gs-portal-glow"></div>
                                    <span>{portal.text}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                );
            case 'escape_rooms':
                return (
                    <div className="gs-format gs-terminal">
                        <div className="gs-terminal-header" style={{background: '#333', color: '#ccc', padding: '5px 10px', fontSize: '0.8rem', fontFamily: 'monospace', borderRadius: '8px 8px 0 0'}}>root@cyberduo:~#</div>
                        <div className="gs-terminal-body" style={{background: '#0a0a0a', padding: '15px', color: '#00FF9D', fontFamily: '"Share Tech Mono", monospace', minHeight: '200px', borderRadius: '0 0 8px 8px', border: '1px solid #333'}}>
                            {currentQ.terminalOutput && currentQ.terminalOutput.map((line, i) => <div key={i} style={{marginBottom: '5px'}}>{line}</div>)}
                            <div className="gs-terminal-input-row" style={{display: 'flex', gap: '10px', marginTop: '15px'}}>
                                <span>$&gt;</span>
                                <input type="text" value={chatInput} onChange={e => setChatInput(e.target.value)} disabled={hasAnswered} style={{background: 'transparent', border: 'none', color: '#fff', flex: 1, fontFamily: 'inherit', outline: 'none', fontSize: '1rem'}} autoFocus={!hasAnswered} />
                            </div>
                        </div>
                    </div>
                );
            case 'kc7_log_hunt':
                return (
                    <div className="gs-format gs-whodunnit">
                        <div className="gs-header-table">
                            <div className="gs-table-head" style={{gridTemplateColumns: '1fr 1.5fr 2fr 1fr'}}>
                                <span>TIME</span>
                                <span>IP ADDR</span>
                                <span>EVENT</span>
                                <span>STATUS</span>
                            </div>
                            {currentQ.logs && currentQ.logs.map(log => (
                                <div key={log.id} className={`gs-table-row ${selectedOption === log.id ? 'selected' : ''}`} style={{gridTemplateColumns: '1fr 1.5fr 2fr 1fr'}} onClick={() => !hasAnswered && setSelectedOption(log.id)}>
                                    <span>{log.time}</span>
                                    <span style={{fontFamily: 'monospace'}}>{log.ip}</span>
                                    <span>{log.event}</span>
                                    <span style={{ color: log.status === 'DENIED' ? '#ff6b6b' : '#00FF9D' }}>{log.status}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                );
            case 'traffic_triage':
                return (
                    <div className="gs-format gs-inbox-triage">
                        {currentQ.files && currentQ.files.map((file, i) => (
                            <div key={i} className="gs-triage-row">
                                <div className="gs-triage-info">
                                    <strong style={{fontFamily: 'monospace', fontSize: '1.2rem'}}>{file.name}</strong>
                                    <span>{file.desc}</span>
                                </div>
                                <div className="gs-triage-actions" style={{display: 'flex', gap: '10px'}}>
                                    <button className={`gs-btn-keep ${triageAnswers[file.id] === false ? 'selected' : ''}`} onClick={() => !hasAnswered && setTriageAnswers({ ...triageAnswers, [file.id]: false })} style={{padding: '8px 20px', borderRadius: '5px', background: 'transparent', border: '2px solid #00FF9D', color: '#00FF9D', cursor: 'pointer'}}>ALLOW</button>
                                    <button className={`gs-btn-delete ${triageAnswers[file.id] === true ? 'selected' : ''}`} onClick={() => !hasAnswered && setTriageAnswers({ ...triageAnswers, [file.id]: true })} style={{padding: '8px 20px', borderRadius: '5px', background: 'transparent', border: '2px solid #ff6b6b', color: '#ff6b6b', cursor: 'pointer'}}>BLOCK</button>
                                </div>
                            </div>
                        ))}
                    </div>
                );
            case 'kahoot_trivia':
                const colors = ['#e21b3c', '#1368ce', '#d89e00', '#26890c'];
                const shapes = ['▲', '◆', '●', '■'];
                return (
                    <div className="gs-format gs-kahoot" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px' }}>
                        {currentQ.options.map((opt, i) => (
                            <button key={i} className={`gs-kahoot-btn ${selectedOption === opt ? 'selected' : ''}`} 
                                style={{
                                    backgroundColor: selectedOption === opt ? '#fff' : colors[i%4], 
                                    color: selectedOption === opt ? '#000' : '#fff',
                                    border: selectedOption === opt ? `4px solid ${colors[i%4]}` : 'none',
                                    padding: '25px', 
                                    borderRadius: '8px', 
                                    fontSize: '1.2rem', 
                                    fontWeight: 'bold', 
                                    display: 'flex', 
                                    alignItems: 'center', 
                                    gap: '15px', 
                                    cursor: 'pointer',
                                    boxShadow: '0 4px 0 rgba(0,0,0,0.2)',
                                    transform: selectedOption === opt ? 'translateY(2px)' : 'none'
                                }} 
                                onClick={() => !hasAnswered && setSelectedOption(opt)}>
                                <span style={{ fontSize: '2rem' }}>{shapes[i%4]}</span>
                                <span style={{ textAlign: 'left', lineHeight: '1.3' }}>{opt}</span>
                            </button>
                        ))}
                    </div>
                );
            default:
                // This prevents blank screens if a DB format has no dedicated render case
                if (currentQ.options && currentQ.options.length > 0) {
                    return (
                        <div className="gs-format gs-mcq-grid">
                            {currentQ.scenario && <div className="gs-scenario-text">{currentQ.scenario}</div>}
                            {currentQ.options.map((opt, i) => {
                                const isSelected = selectedOption === opt;
                                const isWrong = hasAnswered && isSelected && !isCorrectResult;
                                const isCorrect = hasAnswered && opt === currentQ.correctAnswer;
                                const statusClass = isCorrect ? 'correct-answer' : (isWrong ? 'wrong-answer' : '');
                                return (
                                    <button key={i} className={`gs-mcq-card ${isSelected ? 'selected' : ''} ${statusClass}`} onClick={() => !hasAnswered && setSelectedOption(opt)}>
                                        <div className="gs-option-letter">{String.fromCharCode(65 + i)}</div>
                                        <div className="gs-option-text">{opt}</div>
                                    </button>
                                );
                            })}
                        </div>
                    );
                }
                return <div className="gs-feedback error" style={{margin:'20px 0'}}>⚠ Question format '{currentQ.format}' is not yet supported in this version.</div>;

        }
    };

    const getFormatInfo = (format) => {
        const mapping = {
            spot_fake: { icon: '🔍', label: 'Spot The Fake', color: 'phishing' },
            decision_simulator: { icon: '⚖️', label: 'Decision Simulator', color: 'decision' },
            scenario_mcq: { icon: '🧠', label: 'Scenario Analysis', color: 'analysis' },
            drag_flags: { icon: '🚩', label: 'Red Flag Discovery', color: 'investigate' },
            inbox_triage: { icon: '📥', label: 'Inbox Triage', color: 'sort' },
            file_triage: { icon: '📁', label: 'File Analysis', color: 'scan' },
            password_builder: { icon: '🛡️', label: 'Password Builder', color: 'build' },
            sequence_builder: { icon: '🔢', label: 'Timeline Builder', color: 'build' },
            case_study: { icon: '🔎', label: 'Case Study Audit', color: 'investigate' },
            link_inspector: { icon: '🔗', label: 'Link Inspector', color: 'scan' },
            omni_threat_chains: { icon: '⛓️', label: 'Threat Chain', color: 'phishing' },
            scavenger_hunt: { icon: '🕵️', label: 'Scavenger Hunt', color: 'scan' },
            digital_whodunnit: { icon: '🕵️', label: 'Digital Whodunnit', color: 'investigate' },
            select_all: { icon: '✅', label: 'Select All', color: 'decision' },
            spot_the_difference: { icon: '👀', label: 'Visual Analysis', color: 'investigate' },
            quishing_drill: { icon: '📱', label: 'QR Code Analysis', color: 'scan' },
            the_imposter: { icon: '🎭', label: 'Imposter Detection', color: 'phishing' },
            branching_narratives: { icon: '🛤️', label: 'Branching Narrative', color: 'decision' },
            traffic_triage: { icon: '🚦', label: 'Traffic Analysis', color: 'sort' },
            adaptive_inbox: { icon: '📨', label: 'Live Inbox Sim', color: 'sort' },
            file_inspector: { icon: '📄', label: 'Malware Inspector', color: 'scan' },
            escape_rooms: { icon: '💻', label: 'Terminal Escape', color: 'investigate' },
            kc7_log_hunt: { icon: '📊', label: 'Log Hunting', color: 'scan' },
            kahoot_trivia: { icon: '🎮', label: 'Cyber Trivia', color: 'analysis' }
        };
        return mapping[format] || { icon: '💻', label: 'Cyber Challenge', color: 'analysis' };
    };

    const formatInfo = currentQ ? getFormatInfo(currentQ.format) : null;
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
                <div className="gs-stats" style={{ display: 'flex', gap: '15px', alignItems: 'center' }}>
                    <div className="gs-timer-badge" style={{ 
                        color: isPaused ? '#888' : (timeLeft <= 10 ? '#ff6b6b' : '#00FF9D'),
                        border: isPaused ? '1px solid #444' : '1px solid currentColor'
                    }}>
                        {isPaused ? "⏸ PAUSED" : `⏱ ${timeLeft}s`}
                    </div>
                    <span className="gs-xp-badge">⚡ {xp} XP</span>
                </div>
            </div>

            <div className="gs-question-card">
                {currentQ.concept && (
                    <div className="gs-concept-tag">🎯 {currentQ.concept}</div>
                )}
                
                {formatInfo && (
                    <div className={`gs-format-banner gs-banner--${currentQ.level_name === 'hard' ? 'hard-elite' : (currentQ.game_key === 'scams' ? 'scam' : formatInfo.color)}`}>
                        <div className="gs-banner-icon">{currentQ.level_name === 'hard' ? '⚜️' : (currentQ.game_key === 'scams' ? '🕵️' : formatInfo.icon)}</div>
                        <div className="gs-banner-label">{currentQ.level_name === 'hard' ? 'Elite Mission' : (currentQ.game_key === 'scams' ? 'Scam Spotter' : formatInfo.label)}</div>
                        <div className="gs-banner-tag">{currentQ.level_name.toUpperCase()}</div>
                    </div>
                )}
                
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
                                <button className="gs-btn-reveal-answer"
                                    onClick={() => {
                                        let solutionDisplay;
                                        if (currentQ.format === 'sequence_builder') {
                                            const ordered = [...(currentQ.steps || [])].sort((a, b) => a.correctOrder - b.correctOrder);
                                            solutionDisplay = (
                                                <>
                                                    <div style={{ color: '#00FF9D', fontSize: '1.1rem', fontWeight: 'bold', marginBottom: '14px', borderBottom: '1px solid rgba(0,255,157,0.3)', paddingBottom: '10px' }}>CORRECT ORDER:</div>
                                                    <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', marginBottom: '14px' }}>
                                                        {ordered.map((step, idx) => (
                                                            <div key={step.id} style={{ display: 'flex', alignItems: 'center', gap: '12px', padding: '10px 14px', background: 'rgba(0,255,157,0.08)', border: '1px solid rgba(0,255,157,0.25)', borderRadius: '8px' }}>
                                                                <span style={{ background: '#00FF9D', color: '#000', borderRadius: '50%', width: '24px', height: '24px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold', fontSize: '0.85rem', flexShrink: 0 }}>{idx + 1}</span>
                                                                <span>{step.text}</span>
                                                            </div>
                                                        ))}
                                                    </div>
                                                    <div style={{ lineHeight: '1.6', color: 'rgba(255,255,255,0.8)' }}>{currentQ.reveal || currentQ.explain}</div>
                                                </>
                                            );
                                        } else if (currentQ.format === 'click_flags') {
                                            const correctItems = currentQ.emailParts?.filter(p => currentQ.correctFlags?.includes(p.id)).map(p => p.text) || [];
                                            solutionDisplay = (
                                                <>
                                                    <div style={{ color: '#00FF9D', fontSize: '1.1rem', fontWeight: 'bold', marginBottom: '12px', borderBottom: '1px solid rgba(0,255,157,0.3)', paddingBottom: '10px' }}>RED FLAGS TO FIND:</div>
                                                    {correctItems.map((item, i) => (<div key={i} style={{ padding: '8px 12px', background: 'rgba(255,107,107,0.1)', border: '1px solid rgba(255,107,107,0.4)', borderRadius: '6px', marginBottom: '8px' }}>🚩 {item}</div>))}
                                                    <div style={{ lineHeight: '1.6', marginTop: '12px', color: 'rgba(255,255,255,0.8)' }}>{currentQ.reveal || currentQ.explain}</div>
                                                </>
                                            );
                                        } else if (currentQ.format === 'scavenger_hunt' || currentQ.format === 'capture_the_flag') {
                                            const correctItems = currentQ.objects?.filter(o => o.isRedFlag || o.isFlag).map(o => o.label) || [];
                                            solutionDisplay = (
                                                <>
                                                    <div style={{ color: '#00FF9D', fontSize: '1.1rem', fontWeight: 'bold', marginBottom: '12px', borderBottom: '1px solid rgba(0,255,157,0.3)', paddingBottom: '10px' }}>ITEMS TO FLAG:</div>
                                                    {correctItems.map((item, i) => (<div key={i} style={{ padding: '8px 12px', background: 'rgba(255,107,107,0.1)', border: '1px solid rgba(255,107,107,0.4)', borderRadius: '6px', marginBottom: '8px' }}>🚩 {item}</div>))}
                                                    <div style={{ lineHeight: '1.6', marginTop: '12px', color: 'rgba(255,255,255,0.8)' }}>{currentQ.reveal || currentQ.explain}</div>
                                                </>
                                            );
                                        } else if (currentQ.format === 'traffic_triage' || currentQ.format === 'file_triage') {
                                            const badFiles = currentQ.files?.filter(f => f.isMalware) || [];
                                            solutionDisplay = (
                                                <>
                                                    <div style={{ color: '#ff6b6b', fontSize: '1.1rem', fontWeight: 'bold', marginBottom: '12px', borderBottom: '1px solid rgba(255,107,107,0.3)', paddingBottom: '10px' }}>MALICIOUS FILES TO BLOCK:</div>
                                                    {badFiles.map((f, i) => (<div key={i} style={{ padding: '10px', background: 'rgba(255,107,107,0.1)', border: '1px solid rgba(255,107,107,0.4)', borderRadius: '8px', marginBottom: '8px', fontFamily: 'monospace' }}>⛔ {f.name}</div>))}
                                                    <div style={{ lineHeight: '1.6', marginTop: '15px', color: 'rgba(255,255,255,0.8)' }}>{currentQ.reveal || currentQ.explain}</div>
                                                </>
                                            );
                                        } else if (currentQ.format === 'inbox_triage') {
                                            const badEmails = currentQ.emails?.filter(e => e.isPhish) || [];
                                            solutionDisplay = (
                                                <>
                                                    <div style={{ color: '#ff6b6b', fontSize: '1.1rem', fontWeight: 'bold', marginBottom: '12px', borderBottom: '1px solid rgba(255,107,107,0.3)', paddingBottom: '10px' }}>PHISHING EMAILS TO BLOCK:</div>
                                                    {badEmails.map((e, i) => (<div key={i} style={{ padding: '10px', background: 'rgba(255,107,107,0.1)', border: '1px solid rgba(255,107,107,0.4)', borderRadius: '8px', marginBottom: '8px' }}>🎣 {e.subject} (from {e.sender})</div>))}
                                                    <div style={{ lineHeight: '1.6', marginTop: '15px', color: 'rgba(255,255,255,0.8)' }}>{currentQ.reveal || currentQ.explain}</div>
                                                </>
                                            );
                                        } else if (currentQ.format === 'kc7_log_hunt') {
                                            const badLogs = currentQ.logs?.filter(l => l.status === 'MALICIOUS' || l.status === 'ATTACK') || [];
                                            solutionDisplay = (
                                                <>
                                                    <div style={{ color: '#ff6b6b', fontSize: '1.1rem', fontWeight: 'bold', marginBottom: '12px', borderBottom: '1px solid rgba(255,107,107,0.3)', paddingBottom: '10px' }}>INDICATORS OF COMPROMISE (IOC):</div>
                                                    {badLogs.map((l, i) => (<div key={i} style={{ padding: '10px', background: 'rgba(255,107,107,0.1)', border: '1px solid rgba(255,107,107,0.4)', borderRadius: '8px', marginBottom: '8px', fontFamily: 'monospace' }}>⚠️ [{l.time}] {l.ip} - {l.event}</div>))}
                                                    <div style={{ lineHeight: '1.6', marginTop: '15px', color: 'rgba(255,255,255,0.8)' }}>{currentQ.reveal || currentQ.explain}</div>
                                                </>
                                            );
                                        } else {
                                            const answer = currentQ.correctAnswer || currentQ.correctFlags?.join(', ') || currentQ.correctCode || 'Check mission logs for details.';
                                            solutionDisplay = (
                                                <>
                                                    <div style={{ color: '#00FF9D', fontSize: '1.1rem', fontWeight: 'bold', marginBottom: '14px', borderBottom: '1px solid rgba(0,255,157,0.3)', paddingBottom: '10px' }}>CORE SOLUTION:</div>
                                                    <div style={{ padding: '15px', background: 'rgba(0,255,157,0.08)', border: '1px solid rgba(0,255,157,0.3)', borderRadius: '8px', marginBottom: '15px', fontSize: '1.2rem', color: '#00FF9D' }}>{answer}</div>
                                                    <div style={{ lineHeight: '1.6', color: 'rgba(255,255,255,0.8)' }}>{currentQ.reveal || currentQ.explain}</div>
                                                </>
                                            );
                                        }
                                        showModal('Security Intel', solutionDisplay);
                                    }}>
                                    {'\uD83D\uDC41\uFE0F'} SHOW SOLUTION
                                </button>
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
                    <div className="gs-modal-content" style={{ width: '600px', maxHeight: '80vh', height: '600px', display: 'flex', flexDirection: 'column', padding: '30px' }} onClick={e => e.stopPropagation()}>
                        <h3 style={{ fontSize: '1.8rem', marginBottom: '20px' }}>🤖 AI Agent Chat</h3>
                        <div style={{ flex: 1, overflowY: 'auto', marginBottom: '15px', padding: '15px', background: 'rgba(0,0,0,0.3)', borderRadius: '8px' }}>
                            {chatMessages.length === 0 && (
                                <p style={{ color: 'rgba(255,255,255,0.5)', textAlign: 'center', fontSize: '1.1rem' }}>Ask me anything about this question!</p>
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
                                        lineHeight: '1.5'
                                    }}>{msg.text}</span>
                                </div>
                            ))}
                            {chatLoading && (
                                <div style={{ textAlign: 'left', marginTop: '10px' }}>
                                    <span style={{ color: '#00FF9D', fontSize: '1.1rem' }}>AI is thinking... ⏳</span>
                                </div>
                            )}
                        </div>
                        <div style={{ display: 'flex', gap: '10px', marginTop: '10px' }}>
                            <input
                                type="text"
                                value={chatInput}
                                onChange={e => setChatInput(e.target.value)}
                                onKeyDown={e => e.key === 'Enter' && handleChatSend()}
                                placeholder="Ask a question..."
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

            {modal.show && (
                <div className="gs-modal-overlay" onClick={() => setModal({ ...modal, show: false })}>
                    <div className="gs-modal-content" onClick={e => e.stopPropagation()}>
                        <h3>{modal.title}</h3>
                        <div style={{ lineHeight: '1.7', fontSize: '1.05rem' }}>{modal.content}</div>
                        <button onClick={() => setModal({ ...modal, show: false })}>CLOSE</button>
                    </div>
                </div>
            )}
        </div>
    );
}