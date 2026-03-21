/**
 * CyberDuo — Background Animation Engine
 * Pure vanilla JS. Call initBackground(canvas) to start.
 * Call the returned cleanup() function to stop.
 */

function initBackground(canvas) {
    const ctx = canvas.getContext("2d");
    let raf, W, H;

    // ── Resize ──────────────────────────────────────────
    function resize() {
        W = canvas.width = window.innerWidth;
        H = canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener("resize", resize);

    // ── Laser grid lines ─────────────────────────────────
    const hLines = Array.from({ length: 12 }, () => ({
        y: Math.random() * H,
        speed: (Math.random() - 0.5) * 0.3,
        opacity: Math.random() * 0.12 + 0.04,
        color: Math.random() > 0.5 ? "#00FF9D" : "#4D9EFF",
    }));

    const vLines = Array.from({ length: 18 }, () => ({
        x: Math.random() * W,
        speed: (Math.random() - 0.5) * 0.3,
        opacity: Math.random() * 0.10 + 0.03,
        color: Math.random() > 0.5 ? "#4D9EFF" : "#9D4DFF",
    }));

    // ── Hex radar pulses ──────────────────────────────────
    const radars = [
        { x: W * 0.10, y: H * 0.25, r: 0, maxR: 200, speed: 0.8, color: "#00FF9D", phase: 0 },
        { x: W * 0.90, y: H * 0.70, r: 60, maxR: 180, speed: 0.6, color: "#4D9EFF", phase: 1 },
        { x: W * 0.50, y: H * 0.05, r: 120, maxR: 250, speed: 0.5, color: "#9D4DFF", phase: 2 },
    ];

    // ── Circuit sparks ────────────────────────────────────
    function makeSpark() {
        const axis = Math.random() > 0.5 ? "h" : "v";
        return {
            axis,
            x: Math.random() * W,
            y: Math.random() * H,
            len: Math.random() * 120 + 40,
            speed: Math.random() * 2 + 0.5,
            progress: 0,
            color: ["#00FF9D", "#4D9EFF", "#9D4DFF"][Math.floor(Math.random() * 3)],
            opacity: Math.random() * 0.5 + 0.2,
        };
    }
    const sparks = Array.from({ length: 30 }, makeSpark);

    // ── Floating particles ────────────────────────────────
    const particles = Array.from({ length: 140 }, () => ({
        x: Math.random() * W,
        y: Math.random() * H,
        r: Math.random() * 1.8 + 0.3,
        vy: -(Math.random() * 0.5 + 0.1),
        vx: (Math.random() - 0.5) * 0.2,
        color: ["#00FF9D", "#4D9EFF", "#9D4DFF"][Math.floor(Math.random() * 3)],
        opacity: Math.random() * 0.7 + 0.1,
        pulse: Math.random() * Math.PI * 2,
    }));

    // ── Hex grid ──────────────────────────────────────────
    const hexes = [];
    const hexSize = 55;
    const hexH = hexSize * Math.sqrt(3);

    for (let row = 0; row < Math.ceil(H / hexH) + 1; row++) {
        for (let col = 0; col < Math.ceil(W / (hexSize * 1.5)) + 1; col++) {
            hexes.push({
                cx: col * hexSize * 1.5,
                cy: row * hexH + (col % 2 === 0 ? 0 : hexH / 2),
                glowPhase: Math.random() * Math.PI * 2,
                glowSpeed: Math.random() * 0.02 + 0.005,
                active: Math.random() > 0.85,
                color: ["#00FF9D", "#4D9EFF", "#9D4DFF"][Math.floor(Math.random() * 3)],
            });
        }
    }

    // ── Helpers ───────────────────────────────────────────
    function drawHex(cx, cy, size, color, opacity) {
        ctx.beginPath();
        for (let i = 0; i < 6; i++) {
            const angle = (Math.PI / 3) * i - Math.PI / 6;
            const px = cx + size * Math.cos(angle);
            const py = cy + size * Math.sin(angle);
            i === 0 ? ctx.moveTo(px, py) : ctx.lineTo(px, py);
        }
        ctx.closePath();
        ctx.strokeStyle = color;
        ctx.globalAlpha = opacity;
        ctx.lineWidth = 0.5;
        ctx.stroke();
    }

    // ── Main draw loop ────────────────────────────────────
    let frame = 0;

    function draw() {
        W = canvas.width;
        H = canvas.height;

        // Subtle trail effect (partial clear)
        ctx.fillStyle = "rgba(10,15,31,0.18)";
        ctx.globalAlpha = 1;
        ctx.fillRect(0, 0, W, H);
        frame++;

        // ─ 1. Hex grid ───────────────────────────────────
        hexes.forEach(h => {
            h.glowPhase += h.glowSpeed;
            const base = h.active
                ? 0.08 + 0.06 * Math.sin(h.glowPhase)
                : 0.025 + 0.01 * Math.sin(h.glowPhase);
            drawHex(h.cx, h.cy, hexSize - 2, h.color, base);
            if (h.active && Math.sin(h.glowPhase) > 0.9) {
                ctx.globalAlpha = 0.15;
                ctx.fillStyle = h.color;
                ctx.fill();
            }
        });

        // ─ 2. Laser grid lines ────────────────────────────
        hLines.forEach(l => {
            l.y += l.speed;
            if (l.y > H) l.y = 0;
            if (l.y < 0) l.y = H;
            ctx.globalAlpha = l.opacity;
            ctx.strokeStyle = l.color;
            ctx.lineWidth = 0.5;
            ctx.beginPath(); ctx.moveTo(0, l.y); ctx.lineTo(W, l.y); ctx.stroke();
        });
        vLines.forEach(l => {
            l.x += l.speed;
            if (l.x > W) l.x = 0;
            if (l.x < 0) l.x = W;
            ctx.globalAlpha = l.opacity;
            ctx.strokeStyle = l.color;
            ctx.lineWidth = 0.5;
            ctx.beginPath(); ctx.moveTo(l.x, 0); ctx.lineTo(l.x, H); ctx.stroke();
        });

        // ─ 3. Radar rings ────────────────────────────────
        radars.forEach(rd => {
            rd.r += rd.speed;
            if (rd.r > rd.maxR) rd.r = 0;
            const alpha = 1 - rd.r / rd.maxR;

            ctx.globalAlpha = alpha * 0.30;
            ctx.strokeStyle = rd.color;
            ctx.lineWidth = 1.5;
            ctx.beginPath(); ctx.arc(rd.x, rd.y, rd.r, 0, Math.PI * 2); ctx.stroke();

            ctx.globalAlpha = alpha * 0.15;
            ctx.beginPath(); ctx.arc(rd.x, rd.y, rd.r * 0.6, 0, Math.PI * 2); ctx.stroke();

            // Rotating sweep line
            const angle = (frame * 0.02 * rd.speed * 3) + rd.phase * 2;
            ctx.globalAlpha = 0.12;
            ctx.beginPath();
            ctx.moveTo(rd.x, rd.y);
            ctx.lineTo(rd.x + Math.cos(angle) * rd.maxR, rd.y + Math.sin(angle) * rd.maxR);
            ctx.stroke();
        });

        // ─ 4. Circuit sparks ─────────────────────────────
        sparks.forEach((s, idx) => {
            s.progress += s.speed;
            if (s.progress > s.len + 20) { sparks[idx] = makeSpark(); return; }
            const head = Math.min(s.progress, s.len);
            const tail = Math.max(0, s.progress - 20);

            ctx.globalAlpha = s.opacity * (1 - s.progress / (s.len + 20));
            ctx.strokeStyle = s.color;
            ctx.lineWidth = 1.5;
            ctx.shadowColor = s.color;
            ctx.shadowBlur = 6;
            ctx.beginPath();
            if (s.axis === "h") {
                ctx.moveTo(s.x + tail, s.y); ctx.lineTo(s.x + head, s.y);
            } else {
                ctx.moveTo(s.x, s.y + tail); ctx.lineTo(s.x, s.y + head);
            }
            ctx.stroke();
            ctx.shadowBlur = 0;
        });

        // ─ 5. Floating particles ─────────────────────────
        particles.forEach(p => {
            p.y += p.vy;
            p.x += p.vx;
            p.pulse += 0.04;
            if (p.y < -5) { p.y = H + 5; p.x = Math.random() * W; }
            if (p.x < 0 || p.x > W) p.vx *= -1;

            const o = p.opacity * (0.7 + 0.3 * Math.sin(p.pulse));
            ctx.globalAlpha = o;
            ctx.fillStyle = p.color;
            ctx.shadowColor = p.color;
            ctx.shadowBlur = 4;
            ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2); ctx.fill();
            ctx.shadowBlur = 0;
        });

        // ─ 6. Scanline sweep ──────────────────────────────
        const scanY = ((frame * 2) % (H + 4)) - 4;
        ctx.globalAlpha = 0.04;
        ctx.fillStyle = "#00FF9D";
        ctx.fillRect(0, scanY, W, 2);

        // ─ 7. HUD corner brackets ─────────────────────────
        const bSize = 40, bGap = 16;
        const corners = [
            [bGap, bGap, 1, 1],
            [W - bGap, bGap, -1, 1],
            [bGap, H - bGap, 1, -1],
            [W - bGap, H - bGap, -1, -1],
        ];
        ctx.globalAlpha = 0.35;
        ctx.strokeStyle = "#00FF9D";
        ctx.lineWidth = 2;
        corners.forEach(([cx, cy, sx, sy]) => {
            ctx.beginPath();
            ctx.moveTo(cx, cy + sy * bSize);
            ctx.lineTo(cx, cy);
            ctx.lineTo(cx + sx * bSize, cy);
            ctx.stroke();
        });

        // ─ 8. Perspective floor grid ──────────────────────
        ctx.globalAlpha = 1;
        const floorY = H * 0.72;

        // Vanishing-point radial lines
        for (let i = -20; i <= 20; i++) {
            const x = W / 2 + i * 60;
            ctx.globalAlpha = 0.07 * Math.abs(Math.cos(i * 0.15 + frame * 0.01));
            ctx.strokeStyle = "#00FF9D";
            ctx.lineWidth = 0.5;
            ctx.beginPath(); ctx.moveTo(W / 2, floorY); ctx.lineTo(x, H); ctx.stroke();
        }
        // Horizontal floor lines
        for (let j = 0; j < 8; j++) {
            const t = j / 8;
            const y = floorY + (H - floorY) * (t * t);
            const xL = W / 2 - W * 0.8 * t * t;
            const xR = W / 2 + W * 0.8 * t * t;
            ctx.globalAlpha = 0.05 + 0.03 * Math.sin(frame * 0.02 + j);
            ctx.beginPath(); ctx.moveTo(xL, y); ctx.lineTo(xR, y); ctx.stroke();
        }

        ctx.globalAlpha = 1;
        raf = requestAnimationFrame(draw);
    }

    draw();

    // ── Cleanup ───────────────────────────────────────────
    return function cleanup() {
        cancelAnimationFrame(raf);
        window.removeEventListener("resize", resize);
    };
}
export { initBackground };
window.initBackground = initBackground;
