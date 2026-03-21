import { useState, useEffect, useRef, useCallback } from "react";
import { initBackground } from "./background.js";
import AvatarSelection from "./AvatarSelection.jsx";
import ModeSelection from "./ModeSelection.jsx";
import Dashboard from "./Dashboard.jsx";

// ═══════════════════════════════════════════════════════════
// BACKGROUND CANVAS COMPONENT
// Mounts the canvas and delegates all drawing to background.js
// ═══════════════════════════════════════════════════════════
function GameZoneCanvas() {
    const ref = useRef();
    useEffect(() => {
        const cleanup = initBackground(ref.current);
        return cleanup;
    }, []);
    return (
        <canvas
            ref={ref}
            className="bg-canvas"
        />
    );
}

// ═══════════════════════════════════════════════════════════
// FLOATING HUD SHAPES
// ═══════════════════════════════════════════════════════════
const SHAPES_CONFIG = [
    { id: 1, size: 70, left: "6%", top: "18%", delay: 0, color: "#00FF9D", shape: "hex" },
    { id: 2, size: 50, left: "87%", top: "12%", delay: 1.5, color: "#4D9EFF", shape: "cube" },
    { id: 3, size: 60, left: "4%", top: "62%", delay: 0.8, color: "#9D4DFF", shape: "shield" },
    { id: 4, size: 40, left: "91%", top: "55%", delay: 2, color: "#00FF9D", shape: "hex" },
    { id: 5, size: 55, left: "78%", top: "78%", delay: 0.4, color: "#4D9EFF", shape: "cube" },
    { id: 6, size: 35, left: "14%", top: "83%", delay: 1.2, color: "#9D4DFF", shape: "shield" },
    { id: 7, size: 45, left: "50%", top: "5%", delay: 0.6, color: "#00FF9D", shape: "hex" },
    { id: 8, size: 30, left: "22%", top: "40%", delay: 1.8, color: "#4D9EFF", shape: "cube" },
];

function ShapeEl({ shape, size, color, left, top, delay }) {
    const style = {
        position: "fixed", left, top,
        width: size, height: size,
        opacity: 0.22,
        animation: `floatShape ${6 + delay}s ease-in-out ${delay}s infinite`,
        filter: `drop-shadow(0 0 10px ${color}) drop-shadow(0 0 25px ${color}55)`,
        pointerEvents: "none",
        zIndex: 2,
    };

    if (shape === "hex") return (
        <svg style={style} viewBox="0 0 100 100">
            <polygon points="50,5 95,27.5 95,72.5 50,95 5,72.5 5,27.5"
                fill="none" stroke={color} strokeWidth="2.5" />
            <polygon points="50,18 82,35 82,65 50,82 18,65 18,35"
                fill="none" stroke={color} strokeWidth="1" opacity="0.4" />
        </svg>
    );

    if (shape === "cube") return (
        <svg style={style} viewBox="0 0 100 100">
            <rect x="18" y="18" width="64" height="64" fill="none" stroke={color} strokeWidth="2.5" rx="4" />
            <rect x="8" y="8" width="64" height="64" fill="none" stroke={color} strokeWidth="1" rx="4" opacity="0.4" />
            <line x1="18" y1="18" x2="8" y2="8" stroke={color} strokeWidth="1" opacity="0.3" />
            <line x1="82" y1="18" x2="72" y2="8" stroke={color} strokeWidth="1" opacity="0.3" />
            <line x1="82" y1="82" x2="72" y2="72" stroke={color} strokeWidth="1" opacity="0.3" />
        </svg>
    );

    // shield
    return (
        <svg style={style} viewBox="0 0 100 100">
            <path d="M50 5 L90 25 L90 60 Q90 85 50 95 Q10 85 10 60 L10 25 Z"
                fill="none" stroke={color} strokeWidth="2.5" />
            <path d="M50 22 L76 37 L76 59 Q76 76 50 84 Q24 76 24 59 L24 37 Z"
                fill="none" stroke={color} strokeWidth="1" opacity="0.4" />
            <circle cx="50" cy="52" r="8" fill="none" stroke={color} strokeWidth="1.5" opacity="0.6" />
        </svg>
    );
}

// ═══════════════════════════════════════════════════════════
// GLITCH TEXT
// ═══════════════════════════════════════════════════════════
function GlitchText({ text, style: sx = {} }) {
    return (
        <div style={{ position: "relative", display: "inline-block", ...sx }}>
            <span style={{ position: "relative", zIndex: 1 }}>{text}</span>
            <span aria-hidden style={{
                position: "absolute", inset: 0,
                color: "#FF4D4D", opacity: 0,
                animation: "glitch1 4s infinite",
                clipPath: "polygon(0 20%, 100% 20%, 100% 40%, 0 40%)",
                transform: "translateX(-2px)",
            }}>{text}</span>
            <span aria-hidden style={{
                position: "absolute", inset: 0,
                color: "#4D9EFF", opacity: 0,
                animation: "glitch2 4s infinite",
                clipPath: "polygon(0 60%, 100% 60%, 100% 80%, 0 80%)",
                transform: "translateX(2px)",
            }}>{text}</span>
        </div>
    );
}

// ═══════════════════════════════════════════════════════════
// INTRO WIZARD
// ═══════════════════════════════════════════════════════════
function IntroWizard({ onDone }) {
    const [phase, setPhase] = useState("boot");   // boot → logo → tagline → fadeout
    const [typed, setTyped] = useState("");
    const [bootLines, setBootLines] = useState([]);

    const tagline = "Learn Cybersecurity Like Playing a Game";
    const bootSeq = [
        "> INITIALIZING CYBERDUO MAINFRAME...",
        "> LOADING SECURITY PROTOCOLS [████████] 100%",
        "> SCANNING THREAT MATRIX... CLEAR",
        "> ESTABLISHING ENCRYPTED TUNNEL...",
        "> ACCESS GRANTED — WELCOME, RECRUIT",
    ];

    // Boot sequence — stagger lines
    useEffect(() => {
        let delay = 0;
        bootSeq.forEach((line, i) => {
            delay += i === 0 ? 200 : 500;
            setTimeout(() => setBootLines(l => [...l, line]), delay);
        });
        setTimeout(() => setPhase("logo"), delay + 600);
    }, []);

    // Typewriter effect
    useEffect(() => {
        if (phase !== "tagline") return;
        let i = 0;
        const iv = setInterval(() => {
            setTyped(tagline.slice(0, ++i));
            if (i >= tagline.length) {
                clearInterval(iv);
                setTimeout(() => setPhase("fadeout"), 800);
            }
        }, 40);
        return () => clearInterval(iv);
    }, [phase]);

    useEffect(() => {
        if (phase === "logo") setTimeout(() => setPhase("tagline"), 1800);
    }, [phase]);

    useEffect(() => {
        if (phase === "fadeout") {
            const t = setTimeout(onDone, 900);
            return () => clearTimeout(t);
        }
    }, [phase, onDone]);

    return (
        <div style={{
            position: "fixed", inset: 0,
            background: "#0A0F1F", zIndex: 200,
            display: "flex", flexDirection: "column",
            alignItems: "center", justifyContent: "center",
            opacity: phase === "fadeout" ? 0 : 1,
            transition: "opacity 0.9s ease",
            fontFamily: "'Courier New', monospace",
        }}>
            <GameZoneCanvas />

            {/* Boot terminal */}
            {phase === "boot" && (
                <div className="boot-terminal">
                    {bootLines.map((l, i) => (
                        <div key={i} style={{
                            color: i === bootLines.length - 1 ? "#00FF9D" : "#4D9EFF",
                            fontSize: 13, lineHeight: 2,
                            animation: "fadeSlideIn 0.3s ease",
                            textShadow: "0 0 8px currentColor",
                        }}>{l}</div>
                    ))}
                    {bootLines.length < bootSeq.length && (
                        <span style={{ color: "#00FF9D", animation: "blink 0.7s infinite" }}>_</span>
                    )}
                </div>
            )}

            {/* Logo + tagline */}
            {(phase === "logo" || phase === "tagline") && (
                <div style={{ zIndex: 2, textAlign: "center", animation: "zoomIn 0.6s cubic-bezier(0.34,1.56,0.64,1)" }}>
                    <div style={{
                        filter: "drop-shadow(0 0 40px #00FF9D) drop-shadow(0 0 80px #4D9EFF55)",
                        marginBottom: 20,
                    }}>
                        <svg width="130" height="130" viewBox="0 0 100 100">
                            <path d="M50 5 L90 25 L90 60 Q90 85 50 95 Q10 85 10 60 L10 25 Z"
                                fill="rgba(0,255,157,0.12)" stroke="#00FF9D" strokeWidth="2.5" />
                            <path d="M50 20 L75 35 L75 58 Q75 74 50 82 Q25 74 25 58 L25 35 Z"
                                fill="rgba(77,158,255,0.15)" stroke="#4D9EFF" strokeWidth="1.5" />
                            <circle cx="50" cy="52" r="12"
                                fill="rgba(0,255,157,0.2)" stroke="#00FF9D" strokeWidth="1.5" />
                            <text x="50" y="57" textAnchor="middle"
                                fill="#00FF9D" fontSize="13" fontWeight="bold">CD</text>
                        </svg>
                    </div>
                    <div style={{
                        fontSize: 52, fontWeight: 900, letterSpacing: 10,
                        background: "linear-gradient(90deg,#00FF9D,#4D9EFF,#9D4DFF,#00FF9D)",
                        backgroundSize: "300%",
                        WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent",
                        animation: "gradientFlow 3s linear infinite",
                    }}>CYBERDUO</div>
                    <div style={{ color: "#B0B8CC", fontSize: 17, marginTop: 16, minHeight: 28, letterSpacing: 1 }}>
                        {typed}
                        <span style={{ animation: "blink 0.7s infinite", color: "#00FF9D" }}>|</span>
                    </div>
                </div>
            )}
        </div>
    );
}

// ═══════════════════════════════════════════════════════════
// FORM PRIMITIVES
// ═══════════════════════════════════════════════════════════

/** Floating-label input / password field */
function FloatInput({ label, type = "text", value, onChange, error }) {
    const [focused, setFocused] = useState(false);
    const [show, setShow] = useState(false);
    const isPass = type === "password";
    const active = focused || value;

    return (
        <div className="input-wrap">
            <label style={{
                position: "absolute", left: 16,
                top: active ? -10 : 17,
                fontSize: active ? 11 : 15,
                color: active ? (error ? "#FF4D4D" : "#00FF9D") : "#B0B8CC",
                transition: "all 0.2s ease", pointerEvents: "none", zIndex: 2,
                background: active ? "rgba(10,15,31,0.95)" : "transparent",
                padding: "0 4px",
            }}>{label}</label>

            <input
                type={isPass ? (show ? "text" : "password") : type}
                value={value}
                onChange={e => onChange(e.target.value)}
                onFocus={() => setFocused(true)}
                onBlur={() => setFocused(false)}
                style={{
                    width: "100%", padding: "16px 44px 16px 16px",
                    background: "rgba(10,15,31,0.85)",
                    border: `1px solid ${error ? "#FF4D4D" : focused ? "#00FF9D" : "rgba(255,255,255,0.1)"}`,
                    borderRadius: 12, color: "#fff", fontSize: 15,
                    outline: "none", boxSizing: "border-box",
                    boxShadow: focused
                        ? `0 0 20px ${error ? "rgba(255,77,77,0.3)" : "rgba(0,255,157,0.3)"}`
                        : "none",
                    transform: focused ? "scale(1.02)" : "scale(1)",
                    transition: "all 0.2s ease",
                }}
            />

            {isPass && (
                <button type="button" onClick={() => setShow(s => !s)} style={{
                    position: "absolute", right: 14, top: "50%",
                    transform: "translateY(-50%)",
                    background: "none", border: "none",
                    cursor: "pointer", color: "#B0B8CC", fontSize: 18,
                }}>
                    {show ? "🙈" : "👁️"}
                </button>
            )}

            {error && (
                <div style={{ color: "#FF4D4D", fontSize: 11, marginTop: 4 }}>{error}</div>
            )}
        </div>
    );
}

/** Animated password strength meter */
function PasswordStrength({ password }) {
    const checks = [
        { label: "8+ chars", ok: password.length >= 8 },
        { label: "Uppercase", ok: /[A-Z]/.test(password) },
        { label: "Number", ok: /[0-9]/.test(password) },
        { label: "Symbol", ok: /[^A-Za-z0-9]/.test(password) },
    ];
    const score = checks.filter(c => c.ok).length;
    const colors = ["#FF4D4D", "#FF4D4D", "#FFB800", "#00FF9D", "#00FF9D"];
    const labels = ["", "Weak", "Fair", "Good", "Strong"];
    if (!password) return null;

    return (
        <div style={{ marginTop: -12, marginBottom: 16 }}>
            <div className="strength-row">
                {[1, 2, 3, 4].map(i => (
                    <div key={i} className="strength-bar" style={{
                        background: i <= score ? colors[score] : "rgba(255,255,255,0.1)",
                        boxShadow: i <= score ? `0 0 6px ${colors[score]}` : "none",
                    }} />
                ))}
                <span style={{ fontSize: 11, color: colors[score], marginLeft: 6, minWidth: 40 }}>
                    {labels[score]}
                </span>
            </div>
            <div style={{ display: "flex", flexWrap: "wrap", gap: "4px 12px" }}>
                {checks.map(c => (
                    <span key={c.label} style={{ fontSize: 11, color: c.ok ? "#00FF9D" : "#B0B8CC" }}>
                        {c.ok ? "✓" : "○"} {c.label}
                    </span>
                ))}
            </div>
        </div>
    );
}

/** Neon gradient CTA button */
function NeonButton({ children, onClick, gradient = "linear-gradient(90deg,#00FF9D,#4D9EFF)" }) {
    const [hov, setHov] = useState(false);
    const [press, setPress] = useState(false);

    return (
        <button
            type="button"
            onClick={onClick}
            className="neon-btn"
            onMouseEnter={() => setHov(true)}
            onMouseLeave={() => { setHov(false); setPress(false); }}
            onMouseDown={() => setPress(true)}
            onMouseUp={() => setPress(false)}
            style={{
                background: gradient,
                color: "#0A0F1F",
                transform: press ? "scale(0.97)" : hov ? "scale(1.04)" : "scale(1)",
                boxShadow: hov
                    ? "0 0 35px rgba(0,255,157,0.70), 0 0 70px rgba(0,255,157,0.25)"
                    : "0 0 15px rgba(0,255,157,0.25)",
            }}
        >
            <span style={{ position: "relative", zIndex: 1 }}>{children}</span>
            {hov && (
                <div style={{
                    position: "absolute", top: 0, left: "-100%",
                    width: "60%", height: "100%",
                    background: "linear-gradient(90deg, transparent, rgba(255,255,255,0.35), transparent)",
                    animation: "shimmer 0.65s ease forwards",
                }} />
            )}
        </button>
    );
}

/** Selection grid — single or multi select */
function SelectGrid({ items, selected, onSelect, multi = false }) {
    return (
        <div className="select-grid">
            {items.map(it => {
                const on = multi ? selected.includes(it.id) : selected === it.id;
                return (
                    <button
                        key={it.id}
                        type="button"
                        className={`select-card ${on ? "on" : "off"}`}
                        onClick={() => {
                            if (multi) onSelect(on ? selected.filter(x => x !== it.id) : [...selected, it.id]);
                            else onSelect(it.id);
                        }}
                    >
                        <span style={{ fontSize: 20 }}>{it.icon}</span>
                        {it.label}
                    </button>
                );
            })}
        </div>
    );
}

/** Pill toggle button */
function Pill({ label, selected, onSelect, color = "#00FF9D" }) {
    const on = selected === label;
    return (
        <button type="button" className="pill" onClick={() => onSelect(label)} style={{
            border: `1px solid ${on ? color : "rgba(255,255,255,0.1)"}`,
            background: on ? `${color}18` : "rgba(10,15,31,0.8)",
            color: on ? color : "#B0B8CC",
            boxShadow: on ? `0 0 10px ${color}55` : "none",
        }}>{label}</button>
    );
}

// ═══════════════════════════════════════════════════════════
// DATA CONSTANTS
// ═══════════════════════════════════════════════════════════
const PROFESSIONS = [
    { id: "doctor", icon: "👨‍⚕️", label: "Doctor" },
    { id: "lawyer", icon: "⚖️", label: "Lawyer" },
    { id: "architect", icon: "🏛️", label: "Architect" },
    { id: "teacher", icon: "👨‍🏫", label: "Teacher" },
    { id: "farmer", icon: "👨‍🌾", label: "Farmer" },
    { id: "business", icon: "👩‍💼", label: "Business" },
    { id: "artist", icon: "👨‍🎨", label: "Artist" },
    { id: "engineer", icon: "🧑‍🔧", label: "Non-IT Eng" },
    { id: "other", icon: "🧑‍🏭", label: "Other" },
];

const TECH_ROLES = [
    { id: "school", icon: "🎓", label: "School" },
    { id: "ug", icon: "🏫", label: "UG Student" },
    { id: "pg", icon: "🎓", label: "PG Student" },
    { id: "pro", icon: "👨‍💻", label: "IT Pro" },
    { id: "researcher", icon: "👨‍🔬", label: "Researcher" },
    { id: "educator", icon: "👨‍🏫", label: "Educator" },
];

const INTERESTS = [
    { id: "cyber", icon: "🔐", label: "Cybersecurity" },
    { id: "web", icon: "💻", label: "Web Dev" },
    { id: "app", icon: "📱", label: "App Dev" },
    { id: "ai", icon: "🤖", label: "AI/ML" },
    { id: "cloud", icon: "☁️", label: "Cloud" },
    { id: "hacking", icon: "🛡️", label: "Ethical Hacking" },
];

const AGE_GROUPS = ["Under 18", "18–25", "26–40", "40–60", "60+"];
const REASONS = ["Personal safety", "Family protection", "Curiosity", "Career change"];
const HOW_HEARD = ["Social Media", "Friend", "College/University", "Google Search", "Advertisement", "Other"];

// ═══════════════════════════════════════════════════════════
// SIGN IN FORM
// ═══════════════════════════════════════════════════════════
function SignInForm({ onSuccess }) {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSignIn = () => {
        if (!email || !password) { setError("Please fill in all fields."); return; }
        setError("");
        setLoading(true);
        // Simulate API call — replace with real axios call
        setTimeout(() => {
            setLoading(false);
            onSuccess && onSuccess({ username: email.split("@")[0], email });
        }, 900);
    };

    return (
        <div style={{ animation: "fadeSlideIn 0.4s ease" }}>
            <FloatInput label="Email" type="email" value={email} onChange={setEmail} />
            <FloatInput label="Password" type="password" value={password} onChange={setPassword} />

            {error && (
                <div style={{ color: "#FF4D4D", fontSize: 12, marginTop: -12, marginBottom: 12, paddingLeft: 4 }}>
                    ⚠ {error}
                </div>
            )}

            <div style={{ textAlign: "right", marginTop: -4, marginBottom: 20 }}>
                <a href="#" style={{ color: "#4D9EFF", fontSize: 12, textDecoration: "none" }}>
                    Forgot password?
                </a>
            </div>

            <NeonButton onClick={handleSignIn}>{loading ? "LOGGING IN..." : "SIGN IN"}</NeonButton>

            <div className="divider">
                <div className="divider-line-l" />
                OR
                <div className="divider-line-r" />
            </div>

            <div className="social-grid">
                {[
                    { label: "Google", icon: "G", bg: "#ffffff", fg: "#333333" },
                    { label: "GitHub", icon: "⌥", bg: "#24292e", fg: "#ffffff" },
                ].map(b => (
                    <button key={b.label} type="button" className="social-btn"
                        style={{ background: b.bg, color: b.fg }}
                        onClick={() => onSuccess && onSuccess({ username: "operative", email: "" })}
                    >
                        <span style={{ fontWeight: 900 }}>{b.icon}</span>
                        {b.label}
                    </button>
                ))}
            </div>
        </div>
    );
}

// ═══════════════════════════════════════════════════════════
// SIGN UP FORM  (3-step wizard)
// ═══════════════════════════════════════════════════════════
function SignUpForm({ onSuccess }) {
    const [step, setStep] = useState(1);
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirm, setConfirm] = useState("");
    const [background, setBackground] = useState("");
    const [profession, setProfession] = useState("");
    const [role, setRole] = useState("");
    const [interests, setInterests] = useState([]);
    const [ageGroup, setAgeGroup] = useState("");
    const [reason, setReason] = useState("");
    const [username, setUsername] = useState("");
    const [howHeard, setHowHeard] = useState("");
    const [agreed, setAgreed] = useState(false);
    const [done, setDone] = useState(false);

    return (
        <div style={{ animation: "fadeSlideIn 0.4s ease" }}>

            {/* Step progress dots */}
            <div className="step-dots">
                {[1, 2, 3].map(i => (
                    <div key={i} className="step-dot" style={{
                        width: i === step ? 28 : 10,
                        backgroundColor: i <= step ? "#00FF9D" : "rgba(255,255,255,0.15)",
                        boxShadow: i === step ? "0 0 12px #00FF9D" : "none",
                    }} />
                ))}
            </div>

            {/* ── Step 1 : Basic info ─────────────────────── */}
            {step === 1 && (
                <div style={{ animation: "fadeSlideIn 0.35s ease" }}>
                    <FloatInput label="Full Name" value={name} onChange={setName} />
                    <FloatInput label="Email" type="email" value={email} onChange={setEmail} />
                    <FloatInput label="Password" type="password" value={password} onChange={setPassword} />
                    <PasswordStrength password={password} />
                    <FloatInput label="Confirm Password" type="password" value={confirm} onChange={setConfirm}
                        error={confirm && confirm !== password ? "Passwords don't match" : ""} />
                    <NeonButton onClick={() => setStep(2)}>NEXT →</NeonButton>
                </div>
            )}

            {/* ── Step 2 : Background & profile ──────────── */}
            {step === 2 && (
                <div style={{ animation: "fadeSlideIn 0.35s ease" }}>
                    <div style={{ color: "#B0B8CC", fontSize: 13, marginBottom: 10 }}>Tech background?</div>

                    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, marginBottom: 20 }}>
                        {[
                            { id: "tech", label: "⚡ TECH", c: "#4D9EFF" },
                            { id: "nontech", label: "🌍 NON-TECH", c: "#9D4DFF" },
                        ].map(b => (
                            <button key={b.id} type="button" onClick={() => setBackground(b.id)} style={{
                                padding: 16, borderRadius: 12, cursor: "pointer",
                                border: `1px solid ${background === b.id ? b.c : "rgba(255,255,255,0.1)"}`,
                                background: background === b.id ? `${b.c}22` : "rgba(10,15,31,0.8)",
                                color: background === b.id ? b.c : "#B0B8CC",
                                fontWeight: 700, fontSize: 13, transition: "all 0.2s",
                                boxShadow: background === b.id ? `0 0 20px ${b.c}55` : "none",
                            }}>{b.label}</button>
                        ))}
                    </div>

                    {/* Non-tech path */}
                    {background === "nontech" && (
                        <>
                            <div style={{ color: "#B0B8CC", fontSize: 13, marginBottom: 8 }}>Your profession?</div>
                            <SelectGrid items={PROFESSIONS} selected={profession} onSelect={setProfession} />

                            <div style={{ color: "#B0B8CC", fontSize: 13, marginBottom: 8 }}>Age group?</div>
                            <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginBottom: 16 }}>
                                {AGE_GROUPS.map(a => (
                                    <Pill key={a} label={a} selected={ageGroup} onSelect={setAgeGroup} />
                                ))}
                            </div>

                            <div style={{ color: "#B0B8CC", fontSize: 13, marginBottom: 8 }}>Reason for learning?</div>
                            <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginBottom: 16 }}>
                                {REASONS.map(r => (
                                    <Pill key={r} label={r} selected={reason} onSelect={setReason} color="#9D4DFF" />
                                ))}
                            </div>
                        </>
                    )}

                    {/* Tech path */}
                    {background === "tech" && (
                        <>
                            <div style={{ color: "#B0B8CC", fontSize: 13, marginBottom: 8 }}>Your role?</div>
                            <SelectGrid items={TECH_ROLES} selected={role} onSelect={setRole} />

                            <div style={{ color: "#B0B8CC", fontSize: 13, marginBottom: 8 }}>Areas of interest?</div>
                            <SelectGrid items={INTERESTS} selected={interests} onSelect={setInterests} multi />
                        </>
                    )}

                    {background && <NeonButton onClick={() => setStep(3)}>NEXT →</NeonButton>}
                </div>
            )}

            {/* ── Step 3 : Final details ──────────────────── */}
            {step === 3 && (
                <div style={{ animation: "fadeSlideIn 0.35s ease" }}>
                    <FloatInput
                        label="Username"
                        value={username || name.toLowerCase().replace(/\s/g, "_")}
                        onChange={setUsername}
                    />

                    <div style={{ marginBottom: 20 }}>
                        <label style={{ color: "#B0B8CC", fontSize: 13, display: "block", marginBottom: 8 }}>
                            How did you hear about us?
                        </label>
                        <select value={howHeard} onChange={e => setHowHeard(e.target.value)} style={{
                            width: "100%", padding: "14px 16px",
                            background: "rgba(10,15,31,0.85)",
                            border: "1px solid rgba(255,255,255,0.1)",
                            borderRadius: 12,
                            color: howHeard ? "#fff" : "#B0B8CC",
                            fontSize: 14, outline: "none", boxSizing: "border-box",
                        }}>
                            <option value="" disabled>Select one…</option>
                            {HOW_HEARD.map(o => <option key={o} value={o}>{o}</option>)}
                        </select>
                    </div>

                    <div style={{ display: "flex", alignItems: "flex-start", gap: 12, marginBottom: 24 }}>
                        <div
                            className="cyber-checkbox"
                            onClick={() => setAgreed(a => !a)}
                            style={{
                                border: `2px solid ${agreed ? "#00FF9D" : "rgba(255,255,255,0.3)"}`,
                                background: agreed ? "rgba(0,255,157,0.2)" : "transparent",
                                boxShadow: agreed ? "0 0 10px rgba(0,255,157,0.4)" : "none",
                                marginTop: 2,
                            }}
                        >
                            {agreed && <span style={{ color: "#00FF9D", fontSize: 14, fontWeight: 700 }}>✓</span>}
                        </div>
                        <span style={{ color: "#B0B8CC", fontSize: 12, lineHeight: 1.6 }}>
                            I agree to the{" "}
                            <a href="#" style={{ color: "#4D9EFF" }}>Terms</a>
                            {" "}and{" "}
                            <a href="#" style={{ color: "#4D9EFF" }}>Privacy Policy</a>
                        </span>
                    </div>

                    <NeonButton
                        onClick={() => {
                            setDone(true);
                            setTimeout(() => onSuccess && onSuccess({
                                username: username || name.toLowerCase().replace(/\s/g, "_"),
                                email,
                            }), 1400);
                        }}
                        gradient="linear-gradient(90deg,#00FF9D,#9D4DFF)"
                    >
                        {done ? "🎉 WELCOME TO THE ACADEMY!" : "CREATE ACCOUNT"}
                    </NeonButton>

                    {done && (
                        <div style={{
                            textAlign: "center", marginTop: 14,
                            color: "#00FF9D", fontSize: 13,
                            animation: "fadeSlideIn 0.4s ease",
                        }}>
                            Mission briefing awaits, Recruit 🚀
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}

// ═══════════════════════════════════════════════════════════
// ROOT APP
// ═══════════════════════════════════════════════════════════
export default function CyberDuo({ onLoginSuccess }) {
    const [showIntro, setShowIntro] = useState(true);
    const [visible, setVisible] = useState(false);
    const [tab, setTab] = useState("signin");
    // screen: "login" | "avatar" | "mode" | "dashboard"
    const [screen, setScreen] = useState("login");
    const [avatarId, setAvatarId] = useState(null);
    const [gameMode, setGameMode] = useState(null);
    const [username, setUsername] = useState("");
    const [userEmail, setUserEmail] = useState("");

    const doneIntro = useCallback(() => {
        setShowIntro(false);
        setTimeout(() => setVisible(true), 60);
    }, []);

    // Auth success → go to avatar selection
    const handleAuthSuccess = useCallback(({ username: u, email: e } = {}) => {
        if (u) setUsername(u);
        if (e) setUserEmail(e);
        setScreen("avatar");
    }, []);

    // Avatar confirmed → go to mode selection
    const handleAvatarDone = useCallback((id) => {
        console.log("Avatar saved:", id);
        setAvatarId(id);
        setScreen("mode");
    }, []);

    // Mode confirmed → go to dashboard
    const handleModeDone = useCallback((mode) => {
        console.log("Mode saved:", mode);
        setGameMode(mode);
        setScreen("dashboard");
        if (onLoginSuccess) onLoginSuccess({ avatarId, mode });
    }, [onLoginSuccess, avatarId]);

    if (screen === "avatar") return <AvatarSelection onContinue={handleAvatarDone} />;
    if (screen === "mode") return <ModeSelection avatarId={avatarId} onContinue={handleModeDone} />;
    if (screen === "dashboard") return (
        <Dashboard
            avatarId={avatarId}
            username={username}
            email={userEmail}
            mode={gameMode}
            onLogout={() => {
                setScreen("login");
                setAvatarId(null);
                setGameMode(null);
                setUsername("");
                setUserEmail("");
                setVisible(false);
                setTimeout(() => setVisible(true), 60);
            }}
        />
    );

    return (
        <>
            {/* ── Intro wizard ── */}
            {showIntro && <IntroWizard onDone={doneIntro} />}

            {/* ── Background (only after intro) ── */}
            {!showIntro && <GameZoneCanvas />}

            {/* ── Floating HUD shapes ── */}
            {SHAPES_CONFIG.map(s => <ShapeEl key={s.id} {...s} />)}

            {/* ── HUD status panel ── */}
            {!showIntro && (
                <div className="hud-status">
                    <div style={{ animation: "hudBlink 2s infinite" }}>◈ SYSTEM ONLINE</div>
                    <div>THREAT LVL: <span style={{ color: "#4D9EFF" }}>MINIMAL</span></div>
                    <div>FIREWALL: <span style={{ color: "#00FF9D" }}>ACTIVE</span></div>
                </div>
            )}

            {/* ── Main login card ── */}
            <div style={{
                minHeight: "100vh",
                display: "flex", alignItems: "center", justifyContent: "center",
                padding: "40px 20px",
                position: "relative", zIndex: 10,
            }}>
                <div
                    className="login-card"
                    style={{
                        animation: visible
                            ? "slideUp 0.7s cubic-bezier(0.34,1.4,0.64,1) forwards, floatCard 6s 1s ease-in-out infinite, borderGlow 4s ease-in-out 1s infinite"
                            : "none",
                        opacity: visible ? 1 : 0,
                    }}
                >
                    {/* Card header */}
                    <div style={{ textAlign: "center", marginBottom: 26 }}>
                        <div style={{
                            display: "inline-block", marginBottom: 14,
                            filter: "drop-shadow(0 0 20px #00FF9D) drop-shadow(0 0 50px #4D9EFF55)",
                            animation: "floatShape 4s ease-in-out infinite",
                        }}>
                            <svg width="64" height="64" viewBox="0 0 100 100">
                                <path d="M50 5 L90 25 L90 60 Q90 85 50 95 Q10 85 10 60 L10 25 Z"
                                    fill="rgba(0,255,157,0.1)" stroke="#00FF9D" strokeWidth="2.5" />
                                <path d="M50 22 L76 37 L76 59 Q76 76 50 84 Q24 76 24 59 L24 37 Z"
                                    fill="rgba(77,158,255,0.12)" stroke="#4D9EFF" strokeWidth="1.5" />
                                <circle cx="50" cy="52" r="10"
                                    fill="rgba(0,255,157,0.2)" stroke="#00FF9D" strokeWidth="1.5" />
                                <text x="50" y="56" textAnchor="middle"
                                    fill="#00FF9D" fontSize="11" fontWeight="bold" fontFamily="monospace">CD</text>
                            </svg>
                        </div>

                        <GlitchText text="WELCOME, RECRUIT" style={{
                            display: "block",
                            fontSize: 22, fontWeight: 900, letterSpacing: 5,
                            background: "linear-gradient(90deg,#00FF9D,#4D9EFF,#9D4DFF,#00FF9D)",
                            backgroundSize: "300%",
                            WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent",
                            animation: "gradientFlow 4s linear infinite",
                            fontFamily: "'Orbitron', monospace",
                        }} />

                        <div style={{ color: "#B0B8CC", fontSize: 12, marginTop: 8, letterSpacing: 2 }}>
                            BEGIN YOUR CYBERSECURITY JOURNEY
                        </div>
                    </div>

                    {/* Tab switcher */}
                    <div className="tab-rail">
                        {[
                            { id: "signin", label: "SIGN IN" },
                            { id: "signup", label: "CREATE ACCOUNT" },
                        ].map(t => (
                            <button
                                key={t.id}
                                type="button"
                                className={`tab-btn ${tab === t.id ? "active" : "inactive"}`}
                                onClick={() => setTab(t.id)}
                            >
                                {t.label}
                            </button>
                        ))}
                    </div>

                    {/* Forms */}
                    <div style={{ maxHeight: "62vh", overflowY: "auto", paddingRight: 2 }}>
                        {tab === "signin"
                            ? <SignInForm key="si" onSuccess={handleAuthSuccess} />
                            : <SignUpForm key="su" onSuccess={handleAuthSuccess} />}
                    </div>

                    {/* Footer link */}
                    <div style={{ textAlign: "center", marginTop: 18, fontSize: 12, color: "#B0B8CC" }}>
                        {tab === "signin" ? (
                            <>No account?{" "}
                                <button type="button" onClick={() => setTab("signup")}
                                    style={{ background: "none", border: "none", color: "#00FF9D", cursor: "pointer", fontWeight: 700, letterSpacing: 1 }}>
                                    CREATE ONE
                                </button>
                            </>
                        ) : (
                            <>Have an account?{" "}
                                <button type="button" onClick={() => setTab("signin")}
                                    style={{ background: "none", border: "none", color: "#00FF9D", cursor: "pointer", fontWeight: 700, letterSpacing: 1 }}>
                                    SIGN IN
                                </button>
                            </>
                        )}
                    </div>
                </div>
            </div>
        </>
    );
}

// app.jsx is imported by main.jsx — no standalone mount needed.