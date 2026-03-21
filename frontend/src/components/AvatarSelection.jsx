import { useState, useEffect, useRef } from "react";
import { initBackground } from "./background.js";

/* ── Canvas (reuses existing background.js) ─────── */
function GameZoneCanvas() {
    const ref = useRef();
    useEffect(() => {
        const cleanup = initBackground(ref.current);
        return cleanup;
    }, []);
    return <canvas ref={ref} className="bg-canvas" />;
}

/* ── Avatar data (5 in a row as requested) ──────── */
const AVATARS = [
    { id: "hacker", emoji: "🦸", name: "Hacker Hero", role: "Offensive Expert" },
    { id: "agent", emoji: "🦹", name: "Cyber Agent", role: "Stealth Operative" },
    { id: "cat", emoji: "🐱", name: "Cyber Cat", role: "Reconnaissance" },
    { id: "bot", emoji: "🤖", name: "AI Bot", role: "Machine Learning" },
    { id: "ninja", emoji: "👩‍💻", name: "Code Ninja", role: "Zero-Day Hunter" },
];

export { AVATARS };

/* ── Scanline ticker at top ─────────────────────── */
function ScanTicker() {
    const msgs = [
        "IDENTITY VERIFICATION REQUIRED",
        "SELECT YOUR OPERATIVE PROFILE",
        "CYBERDUO TRAINING ACADEMY — SECURE SESSION ACTIVE",
        "ALL SYSTEMS NOMINAL",
    ];
    const [idx, setIdx] = useState(0);
    useEffect(() => {
        const iv = setInterval(() => setIdx(i => (i + 1) % msgs.length), 2800);
        return () => clearInterval(iv);
    }, []);
    return (
        <div className="av-ticker">
            <span className="av-ticker-dot" />
            <span className="av-ticker-text">{msgs[idx]}</span>
        </div>
    );
}

/* ── Animated "particles" ring around selected card */
function SelectRing() {
    return (
        <div className="av-select-ring" aria-hidden>
            {[...Array(8)].map((_, i) => (
                <div key={i} className="av-ring-dot" style={{ "--i": i }} />
            ))}
        </div>
    );
}

/* ── Single avatar card ─────────────────────────── */
function AvatarCard({ av, selected, onClick }) {
    const [hovered, setHovered] = useState(false);
    const isSelected = selected === av.id;

    return (
        <div
            className={`av-card ${isSelected ? "av-card--selected" : ""} ${hovered && !isSelected ? "av-card--hovered" : ""}`}
            onClick={onClick}
            onMouseEnter={() => setHovered(true)}
            onMouseLeave={() => setHovered(false)}
            role="button"
            aria-pressed={isSelected}
        >
            {/* Glow layer */}
            {isSelected && <div className="av-card-glow" />}

            {/* Corner brackets (selected only) */}
            {isSelected && (
                <>
                    <div className="av-bracket av-bracket--tl" />
                    <div className="av-bracket av-bracket--tr" />
                    <div className="av-bracket av-bracket--bl" />
                    <div className="av-bracket av-bracket--br" />
                </>
            )}

            {/* Orbiting ring */}
            {isSelected && <SelectRing />}

            {/* Content */}
            <div className="av-card-inner">
                <div className="av-emoji">{av.emoji}</div>
                <div className="av-name">{av.name}</div>
                <div className="av-role">{av.role}</div>

                {/* Selected badge */}
                <div className={`av-badge ${isSelected ? "av-badge--on" : ""}`}>
                    {isSelected ? "✓ SELECTED" : "SELECT"}
                </div>
            </div>
        </div>
    );
}

/* ── Main component ──────────────────────────────── */
export default function AvatarSelection({ onContinue }) {
    const [selected, setSelected] = useState("hacker");
    const [confirmed, setConfirmed] = useState(false);
    const [mounted, setMounted] = useState(false);

    // Entrance animation trigger
    useEffect(() => {
        const t = setTimeout(() => setMounted(true), 80);
        return () => clearTimeout(t);
    }, []);

    const sel = AVATARS.find(a => a.id === selected);

    const handleContinue = (id) => {
        const chosen = AVATARS.find(a => a.id === id);
        console.log("Avatar saved:", chosen.name);
        setConfirmed(true);
        setTimeout(() => onContinue(id), 900);
    };

    return (
        <div className="av-screen">
            {/* Animated background (reuses login bg) */}
            <GameZoneCanvas />

            {/* Top scan ticker */}
            <ScanTicker />

            {/* HUD corner label */}
            <div className="av-hud-label">AGENT PROFILE SETUP</div>

            {/* Main card */}
            <div className={`av-card-wrap ${mounted ? "av-card-wrap--visible" : ""}`}>

                {/* Header */}
                <div className="av-header">
                    <div className="av-step-tag">STEP 1 OF 2</div>
                    <h1 className="av-title">CHOOSE YOUR CYBER PERSONA</h1>
                    <p className="av-subtitle">Your identity defines your path through the Academy</p>
                </div>

                {/* Avatar row — 5 in a row */}
                <div className="av-row">
                    {AVATARS.map(av => (
                        <AvatarCard
                            key={av.id}
                            av={av}
                            selected={selected}
                            onClick={() => setSelected(av.id)}
                        />
                    ))}
                </div>

                {/* Selected label */}
                <div className="av-selected-label">
                    <span className="av-selected-emoji">{sel.emoji}</span>
                    <span className="av-selected-text">
                        Operative: <strong>{sel.name}</strong>
                    </span>
                    <span className="av-selected-role">— {sel.role}</span>
                </div>

                {/* Action buttons */}
                <div className="av-actions">
                    <button
                        type="button"
                        className="av-btn-skip"
                        onClick={() => handleContinue("hacker")}
                        disabled={confirmed}
                    >
                        SKIP
                    </button>
                    <button
                        type="button"
                        className={`av-btn-continue ${confirmed ? "av-btn-continue--done" : ""}`}
                        onClick={() => handleContinue(selected)}
                        disabled={confirmed}
                    >
                        {confirmed
                            ? `✓ ${sel.name} LOCKED IN`
                            : "CONFIRM IDENTITY →"}
                    </button>
                </div>

                {/* Fine print */}
                <p className="av-footnote">
                    You can change your persona later in Profile Settings
                </p>
            </div>
        </div>
    );
}