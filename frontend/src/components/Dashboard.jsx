// ============================================
// CYBERDUO DASHBOARD
// Dashboard.jsx
// ============================================
import { useEffect, useRef, useState } from "react";
import { initBackground } from "./background.js";
import { getGameProgress, checkUnlockStatus, updateGameProgress } from "../utils/gameProgress.js";
import GameScreen from "./GameScreen.jsx";
import "../styles/dashboard.css";
import "../styles/home.css";

// ---- Avatar map (matches AvatarSelection.jsx IDs exactly) ----
const AVATAR_MAP = {
    "hacker": { emoji: "🦸", label: "Hacker Hero" },
    "agent": { emoji: "🦹", label: "Cyber Agent" },
    "cat": { emoji: "🐱", label: "Cyber Cat" },
    "bot": { emoji: "🤖", label: "AI Bot" },
    "ninja": { emoji: "👩‍💻", label: "Code Ninja" },
};

const DEFAULT_AVATAR = { emoji: "🛡️", label: "Operative" };

// ---- Sidebar nav items ----
const NAV_ITEMS = [
    { id: "home", icon: "🏠", label: "Home" },
    { id: "streak", icon: "🔥", label: "Streak" },
    { id: "radar", icon: "📊", label: "Skill Radar" },
    { id: "alerts", icon: "⚠️", label: "Cyber Alert News" },
    { id: "leaderboard", icon: "🏆", label: "Leaderboard" },
    { id: "badges", icon: "🎖️", label: "Badges" },
    { id: "recommend", icon: "🎯", label: "Recommended" },
    { id: "dailygoal", icon: "📅", label: "Daily Goal" },
];

// ---- Feature placeholder descriptions ----
const FEATURE_META = {
    streak: { title: "Streak Tracker", desc: "Track your daily learning streaks and maintain momentum." },
    radar: { title: "Skill Radar", desc: "Visualize your cybersecurity skill coverage across domains." },
    alerts: { title: "Cyber Alert News", desc: "Stay updated with the latest threats and security advisories." },
    leaderboard: { title: "Leaderboard", desc: "See how you rank against other operatives in the academy." },
    badges: { title: "Badge Collection", desc: "Unlock achievement badges as you complete challenges." },
    recommend: { title: "Recommended Games", desc: "AI-curated game suggestions based on your skill gaps." },
    dailygoal: { title: "Daily Mission", desc: "Complete daily goals to earn XP and maintain your streak." },
};

// ---- Stats for home ----
const HOME_STATS = [
    { icon: "⚡", value: "0", label: "XP EARNED" },
    { icon: "🔥", value: "0", label: "DAY STREAK" },
    { icon: "🎖️", value: "0", label: "BADGES" },
    { icon: "🏆", value: "—", label: "RANK" },
];

const GAME_PLACEHOLDERS = [
    "🔐", "🕵️", "🛡️", "🔍", "💻", "🧩", "⚙️", "🔒"
];

const BRIEFING_TEXTS = {
    phishing: "Identify deceptive emails and malicious links designed to steal classified data. Watch out for urgent requests and unmatched URLs.",
    password: "Learn to crack weak credentials and build impenetrable defense protocols using entropy analysis.",
    malware: "Analyze and neutralize virus payloads before system corruption spreads entirely through the network.",
    firewall: "Configure rapid network defenses and access control lists to block unauthorized infiltration attempts.",
    scams: "Detect social engineering tactics and psychological manipulation used by modern cybercriminals."
};

// ============================================
export default function Dashboard({ avatarId, username, email, mode, onLogout }) {
    const canvasRef = useRef(null);
    const bgEngineRef = useRef(null);

    const [sidebarExpanded, setSidebarExpanded] = useState(false);
    const [activeNav, setActiveNav] = useState("home");
    const [dropdownOpen, setDropdownOpen] = useState(false);
    const [themeLight, setThemeLight] = useState(false);
    const [activeGame, setActiveGame] = useState(null);
    const [progress, setProgress] = useState(null);
    const [selectedMission, setSelectedMission] = useState(null);

    useEffect(() => {
        setProgress(getGameProgress());
    }, []);

    const avatar = AVATAR_MAP[avatarId] || DEFAULT_AVATAR;
    const displayName = username || "Operative";
    const displayEmail = email || "classified@cyberduo.io";
    const modeLabel = mode === "free" ? "FREE MODE" : "PATH MODE";

    // ---- Mount canvas background (reuses background.js) ----
    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const cleanup = initBackground(canvas);
        return cleanup;
    }, []);

    // Close dropdown on outside click
    useEffect(() => {
        if (!dropdownOpen) return;
        const handler = (e) => {
            if (!e.target.closest(".db-profile-wrap")) setDropdownOpen(false);
        };
        document.addEventListener("mousedown", handler);
        return () => document.removeEventListener("mousedown", handler);
    }, [dropdownOpen]);

    const handleNavClick = (id) => {
        setActiveNav(id);
        if (id === "home") {
            setActiveGame(null);
        }
        setSidebarExpanded(false);
    };

    // ---- Render main content ----
    const renderMain = () => {
        if (activeGame) {
            return (
                <GameScreen 
                    gameKey={activeGame.key}
                    gameName={activeGame.name} 
                    level={activeGame.level} 
                    onComplete={() => {
                        const newProg = updateGameProgress(activeGame.level, activeGame.key, activeGame.totalQuestions);
                        setProgress(newProg);
                        setActiveGame(null);
                        setSelectedMission(null);
                    }}
                    onProgressUpdate={(completedQuestions) => {
                        const newProg = updateGameProgress(activeGame.level, activeGame.key, completedQuestions);
                        setProgress(newProg);
                    }}
                    onBack={() => setActiveGame(null)} 
                />
            );
        }
        if (activeNav === "home") return renderHome();
        const meta = FEATURE_META[activeNav];
        const nav = NAV_ITEMS.find(n => n.id === activeNav);
        return (
            <div className="db-feature-placeholder">
                <div className="db-fp-icon">{nav?.icon}</div>
                <div className="db-fp-title">{meta?.title}</div>
                <div className="db-fp-badge">⚙ COMING SOON</div>
                <div className="db-fp-desc">{meta?.desc}</div>
            </div>
        );
    };

    const renderGameCircle = (levelStr, gameKey, gameData, index) => {
        if (!progress) return null;
        
        const isLocked = !checkUnlockStatus(mode, progress, levelStr, gameKey);
        const { questionsDone, totalQuestions, name, icon } = gameData;
        const progressPercent = (questionsDone / totalQuestions) * 100;
        
        const radius = 65;
        const circumference = 2 * Math.PI * radius;
        const strokeDashoffset = circumference - (progressPercent / 100) * circumference;

        const handleGameClick = () => {
            if (isLocked) {
                if (mode === "free") {
                    alert("Complete at least 3 games from previous level to unlock for Free Mode.");
                } else {
                    alert("Complete all previous games first for Path Mode.");
                }
                return;
            }
            setSelectedMission({ name, level: levelStr, difficulty: levelStr, key: gameKey, questionsDone, totalQuestions });
        };

        return (
            <div 
                className={`db-game-circle-wrapper db-node-${index} ${isLocked ? "locked" : ""}`} 
                key={gameKey}
                onClick={handleGameClick}
                title={name}
            >
                <div className="db-game-circle">
                    <svg className="db-progress-ring">
                        <circle className="db-progress-ring-bg" cx="75" cy="75" r={radius} />
                        <circle 
                            className="db-progress-ring-path" 
                            cx="75" cy="75" r={radius}
                            strokeDasharray={circumference}
                            strokeDashoffset={strokeDashoffset}
                        />
                    </svg>
                    <div className="db-game-icon">{icon}</div>
                    {isLocked && <div className="db-lock-overlay">🔒</div>}
                </div>
                <div className="db-game-info">
                    <div className="db-game-name">{name}</div>
                    <div className="db-game-progress-text">{questionsDone} / {totalQuestions}</div>
                </div>
            </div>
        );
    };

    const renderHome = () => (
        <div className="db-home">
            <div className="db-home-left">
                {/* Welcome */}
                <div className="db-welcome-row">
                    <div className="db-welcome-text">
                        <div className="db-welcome-sup">// OPERATIVE STATUS: ONLINE</div>
                        <div className="db-welcome-heading">
                            Welcome back,<br /><span>{displayName}</span>
                        </div>
                        <div className="db-welcome-sub">
                            Your cybersecurity training continues. Stay sharp, stay secure.
                        </div>
                    </div>
                    <div className="db-mode-chip">
                        {mode === "free" ? "🎮" : "🗺️"} &nbsp;{modeLabel}
                    </div>
                </div>

                {/* Game Circles Layout */}
                <div className="db-games-section">
                    <div className="db-section-header">
                        <div className="db-section-title">MISSION PATH</div>
                    </div>
                    {progress ? (
                        <div className="db-levels-container">
                            {["beginner", "medium", "hard"].map((levelStr) => (
                                <div className="db-level-section" key={levelStr}>
                                    <div className="db-level-title">{levelStr.toUpperCase()} LEVEL</div>
                                    <div className="db-circles-row">
                                        <div className="db-path-line"></div>
                                        {Object.entries(progress[levelStr]).map(([gameKey, gameData], index) => 
                                            renderGameCircle(levelStr, gameKey, gameData, index)
                                        )}
                                    </div>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <div className="db-coming-soon-grid" style={{ color: '#00FF9D' }}>
                            Loading Progress...
                        </div>
                    )}
                </div>
            </div>

            <div className="db-home-right">
                {selectedMission ? (
                    <div className="db-briefing-panel">
                        <div className="db-bp-header">
                            <span className="db-bp-label">TARGET ACQUIRED</span>
                            <span className="db-bp-level">{selectedMission.level.toUpperCase()}</span>
                        </div>
                        <div className="db-bp-title">{selectedMission.name}</div>
                        <div className="db-bp-desc">
                            {BRIEFING_TEXTS[selectedMission.key] || "Classified mission parameters. Prepare for deployment."}
                        </div>
                        
                        <div className="db-bp-progress">
                            <div className="db-bp-prog-text">
                                MISSION PROGRESS <span>{selectedMission.questionsDone} / {selectedMission.totalQuestions}</span>
                            </div>
                            <div className="db-bp-prog-bar">
                                <div className="db-bp-prog-fill" style={{ width: `${(selectedMission.questionsDone / Math.max(selectedMission.totalQuestions, 1)) * 100}%` }}></div>
                            </div>
                        </div>

                        <button className="db-btn-engage" onClick={() => setActiveGame(selectedMission)}>
                            [ ENGAGE MISSION ]
                        </button>
                    </div>
                ) : (
                    <div className="db-briefing-panel empty">
                        <div className="db-avatar-welcome">
                            <div className="db-aw-emoji">{avatar.emoji}</div>
                        </div>
                        <div className="db-aw-speech">
                            <div className="db-aw-title">STATUS: STANDING BY</div>
                            Welcome to the CyberDuo Training Grounds! Your mission is to master all security domains. Click on an available mission node to view target intel.
                        </div>
                    </div>
                )}
            </div>
        </div>
    );

    // ============================================
    return (
        <div className="db-root">
            {/* Animated background */}
            <canvas className="db-bg-canvas" ref={canvasRef} />

            {/* Top Bar */}
            <div className="db-topbar">
                <div className="db-topbar-left">
                    <div className="db-logo-icon">
                        <svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg" width="32" height="32">
                            <path d="M16 2L4 8v8c0 7.18 5.15 13.88 12 15.47C22.85 29.88 28 23.18 28 16V8L16 2z"
                                stroke="#00FF9D" strokeWidth="1.5" fill="rgba(0,255,157,0.08)" />
                            <text x="16" y="20" textAnchor="middle" fontSize="9"
                                fontFamily="Orbitron" fill="#00FF9D" fontWeight="700">CD</text>
                        </svg>
                    </div>
                    <div className="db-logo-text">CYBERDUO</div>
                </div>

                <div className="db-topbar-right">
                    <div className="db-hud-status">
                        ● SYSTEM: ONLINE<br />
                        THREAT LVL: MINIMAL
                    </div>

                    {/* Profile */}
                    <div className="db-profile-wrap">
                        <button
                            className="db-profile-btn"
                            onClick={() => setDropdownOpen(o => !o)}
                            aria-label="Profile menu"
                        >
                            {avatar.emoji}
                        </button>

                        {dropdownOpen && (
                            <div className="db-dropdown">
                                {/* Header */}
                                <div className="db-dd-header">
                                    <div className="db-dd-avatar">{avatar.emoji}</div>
                                    <div className="db-dd-info">
                                        <div className="db-dd-name">{displayName}</div>
                                        <div className="db-dd-email">{displayEmail}</div>
                                        <div className="db-dd-mode-badge">
                                            {mode === "free" ? "🎮" : "🗺️"} {modeLabel}
                                        </div>
                                    </div>
                                </div>

                                {/* Items */}
                                <div className="db-dd-items">
                                    <button className="db-dd-item" onClick={() => setDropdownOpen(false)}>
                                        <span className="db-dd-item-icon">👤</span> Edit Profile
                                    </button>

                                    {/* Theme toggle */}
                                    <div className="db-dd-theme-row">
                                        <div className="db-dd-theme-label">
                                            <span className="db-dd-item-icon">🌙</span>
                                            <span style={{ fontSize: 16, color: "rgba(224,224,224,0.75)" }}>
                                                {themeLight ? "Light Mode" : "Dark Mode"}
                                            </span>
                                        </div>
                                        <label className="db-theme-toggle">
                                            <input
                                                type="checkbox"
                                                checked={themeLight}
                                                onChange={e => setThemeLight(e.target.checked)}
                                            />
                                            <span className="db-theme-slider" />
                                        </label>
                                    </div>

                                    <button className="db-dd-item" onClick={() => setDropdownOpen(false)}>
                                        <span className="db-dd-item-icon">⚙️</span> Settings
                                    </button>

                                    <div className="db-dd-divider" />

                                    <button
                                        className="db-dd-item logout"
                                        onClick={() => { setDropdownOpen(false); onLogout?.(); }}
                                    >
                                        <span className="db-dd-item-icon">🚪</span> Logout
                                    </button>
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            </div>

            {/* Body */}
            <div className="db-body">
                {/* Sidebar */}
                <nav className={`db-sidebar${sidebarExpanded ? " expanded" : ""}`}>
                    {/* Toggle arrow */}
                    <div
                        className="db-sidebar-toggle"
                        onClick={() => setSidebarExpanded(e => !e)}
                        title={sidebarExpanded ? "Collapse" : "Expand"}
                    >
                        <svg viewBox="0 0 24 24" fill="none" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                            {sidebarExpanded ? (
                                <polyline points="15 18 9 12 15 6" />
                            ) : (
                                <>
                                    <line x1="4" y1="12" x2="20" y2="12" />
                                    <line x1="4" y1="6" x2="20" y2="6" />
                                    <line x1="4" y1="18" x2="20" y2="18" />
                                </>
                            )}
                        </svg>
                    </div>

                    {/* Nav items */}
                    <div className="db-sidebar-nav">
                        {NAV_ITEMS.map(item => (
                            <div
                                key={item.id}
                                className={`db-nav-item${activeNav === item.id ? " active" : ""}`}
                                onClick={() => handleNavClick(item.id)}
                                title={!sidebarExpanded ? item.label : undefined}
                            >
                                <span className="db-nav-icon">{item.icon}</span>
                                <span className="db-nav-label">{item.label}</span>
                            </div>
                        ))}
                    </div>
                </nav>

                {/* Main */}
                <main className="db-main">
                    {renderMain()}
                </main>
            </div>
        </div>
    );
}
