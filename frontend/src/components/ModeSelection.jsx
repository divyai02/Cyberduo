import { useState, useEffect, useRef } from "react";
import { initBackground } from "./background.js";

/* ── Canvas ─────────────────────────────────────── */
function GameZoneCanvas() {
    const ref = useRef();
    useEffect(() => {
        const cleanup = initBackground(ref.current);
        return cleanup;
    }, []);
    return <canvas ref={ref} className="bg-canvas" />;
}

/* ── Mode data ──────────────────────────────────── */
const MODES = [
    {
        id: "path",
        icon: "🗺️",
        title: "PATH MODE",
        desc: "Guided Learning — Level by Level",
        features: [
            "Games unlock one by one",
            "Recommended for beginners",
            "Structured learning path",
        ],
        color: "#00FF9D",
        glow: "rgba(0,255,157,0.25)",
        gradFrom: "rgba(0,255,157,0.08)",
        gradTo: "rgba(0,255,157,0.02)",
        tag: "RECOMMENDED",
    },
    {
        id: "free",
        icon: "🎮",
        title: "FREE MODE",
        desc: "Play Anything — Full Freedom",
        features: [
            "All Easy games available from start",
            "Play in any order",
            "For curious learners",
        ],
        color: "#4D9EFF",
        glow: "rgba(77,158,255,0.25)",
        gradFrom: "rgba(77,158,255,0.08)",
        gradTo: "rgba(77,158,255,0.02)",
        tag: "EXPLORER",
    },
];

/* ── Single mode card ───────────────────────────── */
function ModeCard({ mode, selected, onClick }) {
    const [hov, setHov] = useState(false);
    const on = selected === mode.id;

    return (
        <div
            className={`ms-card ${on ? "ms-card--on" : ""} ${hov && !on ? "ms-card--hov" : ""}`}
            onClick={onClick}
            onMouseEnter={() => setHov(true)}
            onMouseLeave={() => setHov(false)}
            style={{
                "--mode-color": mode.color,
                "--mode-glow": mode.glow,
                "--grad-from": mode.gradFrom,
                "--grad-to": mode.gradTo,
            }}
            role="button"
            aria-pressed={on}
        >
            {/* Top tag */}
            <div className={`ms-tag ${on ? "ms-tag--on" : ""}`}
                style={{
                    borderColor: on ? mode.color : "transparent",
                    color: on ? mode.color : "#B0B8CC"
                }}>
                {mode.tag}
            </div>

            {/* Glow bg (selected only) */}
            {on && <div className="ms-card-glow" />}

            {/* Corner brackets */}
            {on && (
                <>
                    <div className="ms-bracket ms-bracket--tl" style={{ borderColor: mode.color }} />
                    <div className="ms-bracket ms-bracket--tr" style={{ borderColor: mode.color }} />
                    <div className="ms-bracket ms-bracket--bl" style={{ borderColor: mode.color }} />
                    <div className="ms-bracket ms-bracket--br" style={{ borderColor: mode.color }} />
                </>
            )}

            {/* Icon */}
            <div className="ms-icon">{mode.icon}</div>

            {/* Title */}
            <div className="ms-card-title" style={{ color: on ? mode.color : "#fff" }}>
                {mode.title}
            </div>

            {/* Desc */}
            <div className="ms-card-desc">{mode.desc}</div>

            {/* Divider */}
            <div className="ms-divider" style={{ background: on ? mode.color : "rgba(255,255,255,0.07)" }} />

            {/* Features */}
            <ul className="ms-features">
                {mode.features.map((f) => (
                    <li key={f} className="ms-feature-item">
                        <span className="ms-feature-dot" style={{ background: mode.color, boxShadow: `0 0 6px ${mode.color}` }} />
                        {f}
                    </li>
                ))}
            </ul>

            {/* Select indicator */}
            <div className={`ms-select-chip ${on ? "ms-select-chip--on" : ""}`}
                style={on ? { borderColor: mode.color, color: mode.color, background: `${mode.gradFrom}` } : {}}>
                {on ? "✓ SELECTED" : "CLICK TO SELECT"}
            </div>
        </div>
    );
}

/* ── Main component ─────────────────────────────── */
export default function ModeSelection({ avatarId, onContinue }) {
    const [selected, setSelected] = useState(null);
    const [confirmed, setConfirmed] = useState(false);
    const [mounted, setMounted] = useState(false);

    useEffect(() => {
        const t = setTimeout(() => setMounted(true), 80);
        return () => clearTimeout(t);
    }, []);

    const handleContinue = () => {
        if (!selected || confirmed) return;
        setConfirmed(true);
        setTimeout(() => onContinue(selected), 800);
    };

    const selMode = MODES.find((m) => m.id === selected);

    return (
        <div className="ms-screen">
            <GameZoneCanvas />

            {/* Top ticker */}
            <div className="ms-ticker">
                <span className="ms-ticker-dot" />
                <span className="ms-ticker-text">LEARNING PATH CONFIGURATION — CHOOSE YOUR OPERATIVE STYLE</span>
            </div>

            {/* HUD labels */}
            <div className="ms-hud-label ms-hud-l">STEP 2 OF 2</div>
            <div className="ms-hud-label ms-hud-r">TRAINING PROTOCOL</div>

            {/* Card wrap */}
            <div className={`ms-wrap ${mounted ? "ms-wrap--visible" : ""}`}>

                {/* Header */}
                <div className="ms-header">
                    <h1 className="ms-title">CHOOSE YOUR LEARNING PATH</h1>
                    <p className="ms-subtitle">How do you want to learn cybersecurity?</p>
                </div>

                {/* Mode cards row */}
                <div className="ms-row">
                    {MODES.map((m) => (
                        <ModeCard
                            key={m.id}
                            mode={m}
                            selected={selected}
                            onClick={() => !confirmed && setSelected(m.id)}
                        />
                    ))}
                </div>

                {/* VS divider (desktop only) */}
                <div className="ms-vs" aria-hidden>VS</div>

                {/* CTA */}
                <div className="ms-cta">
                    <button
                        type="button"
                        className={`ms-btn ${!selected ? "ms-btn--disabled" : ""} ${confirmed ? "ms-btn--done" : ""}`}
                        onClick={handleContinue}
                        disabled={!selected || confirmed}
                        style={selected && !confirmed ? {
                            background: `linear-gradient(90deg, ${selMode.color}, ${selMode.id === "path" ? "#4D9EFF" : "#9D4DFF"})`,
                        } : {}}
                    >
                        {confirmed
                            ? `✓ ${selMode?.title} ACTIVATED`
                            : selected
                                ? `ENTER ${selMode.title} →`
                                : "SELECT A MODE TO CONTINUE"}
                    </button>

                    <p className="ms-footnote">
                        You can switch modes anytime from Settings
                    </p>
                </div>
            </div>
        </div>
    );
}
