import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import storyData from '../data/story_main.json';
import '../styles/StoryPlayer.css';

const Typewriter = ({ text, onComplete }) => {
  const [displayedText, setDisplayedText] = useState('');
  
  useEffect(() => {
    const sourceText = String(text || '');
    setDisplayedText('');
    
    let ticker = 0;
    const interval = setInterval(() => {
      ticker++;
      setDisplayedText(sourceText.slice(0, ticker));
      if (ticker >= sourceText.length) {
        clearInterval(interval);
        if (onComplete) onComplete();
      }
    }, 30);
    
    return () => clearInterval(interval);
  }, [text]);

  return <span className="dialogue-render">{displayedText}</span>;
};

export default function StoryPlayer({ onBack, userId }) {
  const [isStoryStarted, setIsStoryStarted] = useState(false);
  const [story] = useState(storyData);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [showChoices, setShowChoices] = useState(false);
  const [selectedChoice, setSelectedChoice] = useState(null);
  const [feedback, setFeedback] = useState(null);
  const [isTyping, setIsTyping] = useState(true);
  const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:5000";

  if (!story || !story.scenes) return <div style={{ color: 'white', padding: '100px', textAlign: 'center' }}>[SYSTEM ERROR] FAILED TO LOAD NARRATIVE DATA.</div>;

  const currentScene = story.scenes[currentIndex];
  const isQuestion = currentScene.type === 'question';
  const progress = ((currentIndex + 1) / story.scenes.length) * 100;

  // Cloud & Local XP Synchronization
  const addXP = (amount) => {
    const currentXP = parseInt(localStorage.getItem("userXP") || "0");
    const newXP = currentXP + amount;
    localStorage.setItem("userXP", newXP.toString());
    
    window.dispatchEvent(new Event('xpUpdated'));
    window.dispatchEvent(new Event('storage'));
    window.dispatchEvent(new Event('leaderboardRefresh'));

    if (userId) {
      fetch(`${API_BASE_URL}/game/save-result`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          game_key: "interactive_story",
          level: "any",
          xp_earned: amount,
          score: amount > 0 ? amount : 0, 
          is_single_question: true
        })
      }).catch(e => console.error("Cloud XP sync failed", e));
    }
  };

  const handleNext = () => {
    if (isTyping) {
      setIsTyping(false);
      return;
    }
    if (isQuestion && selectedChoice === null) return;
    
    addXP(10);

    if (currentIndex < story.scenes.length - 1) {
      setCurrentIndex(prev => prev + 1);
      setSelectedChoice(null);
      setShowChoices(false);
      setFeedback(null);
      setIsTyping(true);
    } else {
      addXP(150);
      onBack();
    }
  };

  const handleChoice = (index, isCorrect) => {
    setSelectedChoice(index);
    setFeedback(currentScene.options[index].feedback);
    
    if (isCorrect) {
      addXP(50);
    } else {
      addXP(-20);
    }

    setTimeout(() => {
      setShowChoices(false);
    }, 2000);
  };

  const bgImages = {
    college: '/images/library.png',
    cafe: '/images/cafe.png'
  };

  if (!isStoryStarted) {
    return (
      <div className="story-player-outer">
        <motion.div 
          className="featured-story-hero"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
        >
          <div className="hero-content-grid">
            <div className="hero-poster" onClick={() => setIsStoryStarted(true)}>
              <img src="/images/poster.jpg" alt="Story Poster" className="poster-bg" />
              <div className="poster-overlay">
                <div className="character-hints">
                  <div className="hint-pill">
                    <img src="/images/arjun.png" alt="Arjun" className="hint-avatar" />
                    <span>Arjun</span>
                  </div>
                  <div className="hint-pill">
                    <img src="/images/riya.png" alt="Riya" className="hint-avatar" />
                    <span>Riya</span>
                  </div>
                </div>
                <div className="play-hint">
                  <div className="play-button-circle">▶</div>
                </div>
              </div>
            </div>

            <div className="hero-details">
              <div className="episode-tag">FEATURED EPISODE</div>
              <h1 className="hero-title">The Day Everything Almost Broke</h1>
              <p className="hero-description">
                Arjun and Riya are hours away from their career-defining hackathon demo. 
                But as they scramble to finish, a chain of subtle digital threats begins to pull at the threads of their reality.
              </p>

              <div className="topics-list">
                <span className="topic-chip">📧 Phishing</span>
                <span className="topic-chip">🔑 Passwords</span>
                <span className="topic-chip">🦠 Malware</span>
                <span className="topic-chip">📡 Network</span>
                <span className="topic-chip">🚨 Scams</span>
              </div>

              <motion.button 
                className="start-mission-btn"
                whileHover={{ scale: 1.05, boxShadow: '0 0 20px rgba(99, 102, 241, 0.5)' }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setIsStoryStarted(true)}
              >
                START INTERACTIVE EXPERIENCE
              </motion.button>

              <div className="mission-meta">
                <span>⏱ 3-5 MINS</span>
                <span>⭐ 500 XP</span>
                <span>🔥 IMMERSIVE</span>
              </div>
            </div>
          </div>
          <button className="back-to-hub-mini" onClick={onBack}>✖ BACK</button>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="story-player-outer">
      <div className="story-player-container">
        <div className="story-background">
          <img 
            src={bgImages[currentScene.background] || bgImages.college} 
            alt="Background" 
            className="background-hq-img"
            loading="eager"
            onError={(e) => { e.target.src = '/images/library.png'; }}
          />
          <div className="story-overlay"></div>
        </div>

        <div className="progress-bar">
          <div className="progress-fill" style={{ width: `${progress}%` }}></div>
        </div>

        <button className="back-to-hub" onClick={onBack}>✖ EXIT STORY</button>

        <AnimatePresence mode="wait">
          <motion.div 
            key={currentIndex}
            className={`dialogue-box-container 
              ${isQuestion ? 'is-question' : (currentScene.active_side === 'left' ? 'side-left' : 'side-right')} 
              ${selectedChoice !== null && !currentScene.options[selectedChoice].isCorrect ? 'shake' : ''}`}
            initial={{ y: 50, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            onClick={handleNext}
            style={{ cursor: 'pointer', pointerEvents: 'auto' }}
          >
            <div 
              className="speaker-label" 
              style={{ 
                background: currentScene.speaker === 'Arjun' ? '#00f3ff' : '#a855f7',
                color: '#000',
                letterSpacing: '2px',
                fontWeight: '900'
              }}
            >
              {String(currentScene.speaker).toUpperCase()}
            </div>

            <div className="dialogue-text">
              <Typewriter 
                key={currentScene.dialogue}
                text={currentScene.dialogue} 
                onComplete={() => {
                  setIsTyping(false);
                  if (isQuestion) setShowChoices(true);
                }} 
              />
              {!isTyping && !isQuestion && (
                <motion.span 
                  animate={{ opacity: [0, 1, 0] }} 
                  transition={{ repeat: Infinity, duration: 1 }}
                  style={{ marginLeft: '10px', fontSize: '1rem', verticalAlign: 'middle' }}
                >
                  ▼
                </motion.span>
              )}
            </div>

            {isQuestion && showChoices && (
              <div className="choices-container">
                {currentScene.options.map((option, idx) => (
                  <motion.button
                    key={idx}
                    className={`choice-button ${selectedChoice === idx ? (option.isCorrect ? 'correct' : 'wrong') : ''}`}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={(e) => {
                      e.stopPropagation();
                      handleChoice(idx, option.isCorrect);
                    }}
                    disabled={selectedChoice !== null}
                  >
                    {option.text}
                  </motion.button>
                ))}
              </div>
            )}

            {feedback && (
              <motion.div 
                className={`feedback-box ${selectedChoice !== null && currentScene.options[selectedChoice].isCorrect ? 'success' : 'error'}`}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                style={{ color: currentScene.options[selectedChoice].isCorrect ? '#10b981' : '#f87171', fontWeight: 'bold' }}
              >
                {currentScene.options[selectedChoice].isCorrect ? '✨ CORRECT: ' : '⚠️ CRITICAL ERROR: '}
                {feedback}
                <div style={{ marginTop: '5px', fontSize: '0.8rem', color: '#fff', opacity: 0.6 }}>
                  Click dialogue box to proceed.
                </div>
              </motion.div>
            )}
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
}
