// ============================================
// CYBERDUO DASHBOARD
// Dashboard.jsx
// ============================================
import { useEffect, useRef, useState } from "react";
import { initBackground } from "./background.js";
import "../styles/dashboard.css";

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

// ============================================
export default function Dashboard({ avatarId, username, email, mode, onLogout }) {
    const canvasRef = useRef(null);
    const bgEngineRef = useRef(null);

    const [sidebarExpanded, setSidebarExpanded] = useState(false);
    const [activeNav, setActiveNav] = useState("home");
    const [dropdownOpen, setDropdownOpen] = useState(false);
    const [themeLight, setThemeLight] = useState(false);

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
        setSidebarExpanded(false);
    };

    // ---- Render main content ----
    const renderMain = () => {
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

    const renderHome = () => (
        <div className="db-home">
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

            {/* Stats */}
            <div className="db-stats-row">
                {HOME_STATS.map(s => (
                    <div className="db-stat-card" key={s.label}>
                        <div className="db-stat-icon">{s.icon}</div>
                        <div className="db-stat-value">{s.value}</div>
                        <div className="db-stat-label">{s.label}</div>
                    </div>
                ))}
            </div>

            {/* Games placeholder */}
            <div className="db-games-section">
                <div className="db-section-header">
                    <div className="db-section-title">GAME LIBRARY</div>
                </div>
                <div className="db-coming-soon-grid">
                    {GAME_PLACEHOLDERS.map((icon, i) => (
                        <div className="db-game-placeholder" key={i}>
                            <div className="db-game-placeholder-icon">{icon}</div>
                            LOADING...
                        </div>
                    ))}
                </div>
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
