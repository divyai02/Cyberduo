import React, { useEffect, useState, useRef } from 'react';
import '../styles/SkillRadar.css';
import { calculateSkillRadar } from '../utils/gameProgress.js';

export default function SkillRadar({ progress, compact = false }) {
    const [radarData, setRadarData] = useState([]);
    const [animRadarPct, setAnimRadarPct] = useState(0);
    
    useEffect(() => {
        if (progress) {
            setRadarData(calculateSkillRadar(progress));
        }
    }, [progress]);

    useEffect(() => {
        // Animation for the spider web chart growing outwards
        let startTime;
        let animationFrame;
        const animate = (timestamp) => {
            if (!startTime) startTime = timestamp;
            const progress = timestamp - startTime;
            const duration = 1500;
            const easeOutQuart = 1 - Math.pow(1 - progress/duration, 4);
            const currentVal = Math.min(easeOutQuart, 1);
            
            setAnimRadarPct(currentVal);
            
            if (progress < duration) {
                animationFrame = requestAnimationFrame(animate);
            } else {
                setAnimRadarPct(1);
            }
        };
        const timeout = setTimeout(() => {
            animationFrame = requestAnimationFrame(animate);
        }, 600); 

        return () => {
            clearTimeout(timeout);
            cancelAnimationFrame(animationFrame);
        };
    }, []);

    if (!radarData || radarData.length === 0) {
        return <div className="sr-loading">Loading radar intel...</div>;
    }

    // Mathematical parameters for the Spider Web Chart
    const svgSize = compact ? 220 : 300;
    const center = svgSize / 2;
    const maxRadius = compact ? 70 : 100;

    const getRadarPoint = (percent, index) => {
        const angle = -Math.PI / 2 + (index * 2 * Math.PI) / 5;
        const r = (percent / 100) * maxRadius;
        return `${center + r * Math.cos(angle)},${center + r * Math.sin(angle)}`;
    };

    // Calculate user polygon taking animation state into account
    const userPolygonPoints = radarData.map((skill, i) => getRadarPoint(skill.percentage * animRadarPct, i)).join(" ");
    const webLevels = [20, 40, 60, 80, 100];
    
    // Assessor logic to find worst skill
    const sortedSkills = [...radarData].sort((a,b) => a.percentage - b.percentage);
    const weakestSkill = sortedSkills.length > 0 ? sortedSkills[0] : null;

    if (compact) {
        return (
            <div className="sr-container compact">
                <h2 className="sr-title">SKILL RADAR</h2>
                <div className="sr-radar-chart">
                    <svg width={svgSize} height={svgSize} className="sr-spider-svg">
                        {webLevels.map(level => {
                            const pts = [0, 1, 2, 3, 4].map(i => getRadarPoint(level, i)).join(" ");
                            return <polygon key={level} points={pts} className="sr-spider-level" />;
                        })}
                        {[0, 1, 2, 3, 4].map(i => {
                            const endPt = getRadarPoint(100, i);
                            const [ex, ey] = endPt.split(",");
                            return <line key={`spoke-${i}`} x1={center} y1={center} x2={ex} y2={ey} className="sr-spider-spoke" />;
                        })}
                        <polygon points={userPolygonPoints} className="sr-user-polygon" />
                        {radarData.map((skill, i) => {
                            const angle = -Math.PI / 2 + (i * 2 * Math.PI) / 5;
                            const r = maxRadius + 20;
                            const x = center + r * Math.cos(angle);
                            const y = center + r * Math.sin(angle);
                            return (
                                <text key={`lbl-${i}`} x={x} y={y} className="sr-spider-label" textAnchor="middle" dominantBaseline="middle" fill={skill.color} style={{ fontSize: '14px' }}>
                                    {skill.icon}
                                </text>
                            );
                        })}
                    </svg>
                </div>
                {weakestSkill && (
                    <div className="sr-compact-stat">
                        Weakest: <span style={{ color: weakestSkill.color }}>{weakestSkill.name} ({weakestSkill.percentage}%)</span>
                    </div>
                )}
            </div>
        );
    }

    return (
        <div className="sr-container">
            <h2 className="sr-title">SKILL RADAR</h2>
            <div className="sr-grid">
                {radarData.map((skill, index) => (
                    <SkillCircle key={skill.key} skill={skill} index={index} />
                ))}
            </div>
            
            <div className="sr-lower-section">
                
                {/* Visual SVG Map Sub-Dashboard */}
                <div className="sr-radar-chart">
                    <svg width={svgSize} height={svgSize} className="sr-spider-svg">
                        {/* Background Web Polygons */}
                        {webLevels.map(level => {
                            const pts = [0, 1, 2, 3, 4].map(i => getRadarPoint(level, i)).join(" ");
                            return <polygon key={level} points={pts} className="sr-spider-level" />;
                        })}
                        {/* Axis Intercept Spokes */}
                        {[0, 1, 2, 3, 4].map(i => {
                            const endPt = getRadarPoint(100, i);
                            const [ex, ey] = endPt.split(",");
                            return <line key={`spoke-${i}`} x1={center} y1={center} x2={ex} y2={ey} className="sr-spider-spoke" />;
                        })}
                        {/* Animated Overlay Shape corresponding to real score percents */}
                        <polygon points={userPolygonPoints} className="sr-user-polygon" />
                        
                        {/* Axis Emojis Labels */}
                        {radarData.map((skill, i) => {
                            const angle = -Math.PI / 2 + (i * 2 * Math.PI) / 5;
                            const r = maxRadius + 25; // Render labels firmly outside of polygon constraints
                            const x = center + r * Math.cos(angle);
                            const y = center + r * Math.sin(angle);
                            return (
                                <text key={`lbl-${i}`} x={x} y={y} className="sr-spider-label" textAnchor="middle" dominantBaseline="middle" fill={skill.color}>
                                    {skill.icon}
                                </text>
                            );
                        })}
                    </svg>
                </div>
                
                {/* Briefing Analytics Console */}
                <div className="sr-tactical-assessor">
                    <div className="sr-ta-header">TACTICAL THREAT ASSESSOR</div>
                    <div className="sr-ta-body">
                        <div className="sr-ta-line system slide-1">&gt; ANALYZING OPERATIVE CAPABILITIES...</div>
                        <div className="sr-ta-line system slide-2">&gt; PROFILING {radarData.length} CYBERSECURITY DOMAINS...</div>
                        
                        {weakestSkill && (
                            <>
                                <div className="sr-ta-line warning slide-3">
                                    &gt; WARNING: Critical vulnerability detected in <span style={{color: weakestSkill.color}}>[{weakestSkill.name.toUpperCase()}]</span> parameters.
                                </div>
                                <div className="sr-ta-line warning slide-4">
                                    &gt; MODULE INTEGRITY: {weakestSkill.percentage}%
                                </div>
                                <div className="sr-ta-line action slide-5">
                                    &gt; RECOMMENDED ACTION: Engage <span style={{color: '#00FF9D'}}>{weakestSkill.name}</span> training missions immediately to restore network equilibrium.
                                </div>
                            </>
                        )}
                        <div className="sr-ta-cursor slide-6">_</div>
                    </div>
                </div>

            </div>

            <p className="sr-description">
                Monitor your proficiency across all cybersecurity domains. Complete missions across beginner, medium, and hard levels to maximize your rating and earn unique badges.
            </p>
        </div>
    );
}

function SkillCircle({ skill, index }) {
    const [animatedPct, setAnimatedPct] = useState(0);
    const [isHovered, setIsHovered] = useState(false);
    
    // Config for 100x100 SVG ring
    const radius = 42;
    const circumference = 2 * Math.PI * radius;
    
    useEffect(() => {
        // Stagger load and animated numbered count-up
        const loadDelay = index * 100; // 0.1s stagger per circle
        let animationFrame;
        let startTime;

        const animate = (timestamp) => {
            if (!startTime) startTime = timestamp;
            const progress = timestamp - startTime;
            const duration = 1500; // 1.5s
            
            // ease out quart computation
            const easeOutQuart = 1 - Math.pow(1 - progress/duration, 4);
            const currentVal = Math.min(Math.round(easeOutQuart * skill.percentage), skill.percentage);
            
            setAnimatedPct(currentVal);

            if (progress < duration) {
                animationFrame = requestAnimationFrame(animate);
            } else {
                setAnimatedPct(skill.percentage);
            }
        };

        const timeout = setTimeout(() => {
            animationFrame = requestAnimationFrame(animate);
        }, loadDelay + 300); // base delay to let the page render smoothly

        return () => {
            clearTimeout(timeout);
            cancelAnimationFrame(animationFrame);
        };
    }, [skill.percentage, index]);

    // calculate stroke-dashoffset for SVG ring animation
    const strokeDashoffset = circumference - (animatedPct / 100) * circumference;

    return (
        <div 
            className="sr-circle-wrap pop-in"
            onMouseEnter={() => setIsHovered(true)}
            onMouseLeave={() => setIsHovered(false)}
            style={{ animationDelay: `${index * 0.1}s` }}
        >
            <div className="sr-circle-inner" style={{ 
                boxShadow: isHovered ? `0 0 20px ${skill.color}55, inset 0 0 10px ${skill.color}33` : `inset 0 0 10px rgba(0,0,0,0.5)`,
                borderColor: isHovered ? skill.color : 'rgba(255,255,255,0.1)',
                transform: isHovered ? 'scale(1.05)' : 'scale(1)',
                background: 'rgba(20,27,43,0.6)',
                backdropFilter: 'blur(5px)'
            }}>
                <svg className="sr-svg-ring" width="100" height="100">
                    <circle className="sr-ring-bg" cx="50" cy="50" r={radius} />
                    <circle 
                        className="sr-ring-path" 
                        cx="50" cy="50" r={radius} 
                        stroke={skill.color}
                        strokeDasharray={circumference}
                        strokeDashoffset={strokeDashoffset}
                    />
                </svg>
                <div className="sr-icon">{skill.icon}</div>
                
                {/* Hover Tooltip */}
                <div className={`sr-tooltip ${isHovered ? 'visible' : ''}`}>
                    <div className="sr-tt-title" style={{color: skill.color}}>
                        {skill.icon} {skill.name}
                    </div>
                    <div className="sr-tt-pct">{skill.percentage}% Complete</div>
                    <div className="sr-tt-breakdown">
                        <span className="sr-tt-bd-col">Beginner<br/><span>{skill.breakdown.beginner}/5</span></span>
                        <span className="sr-tt-bd-col dot">&bull;</span>
                        <span className="sr-tt-bd-col">Medium<br/><span>{skill.breakdown.medium}/5</span></span>
                        <span className="sr-tt-bd-col dot">&bull;</span>
                        <span className="sr-tt-bd-col">Hard<br/><span>{skill.breakdown.hard}/5</span></span>
                    </div>
                    {skill.nextBadge !== 'MAXED' ? (
                        <div className="sr-tt-badge">
                            <span>{skill.neededForNext}%</span> more to reach <strong style={{color: '#FFB800'}}>{skill.nextBadge}</strong> badge
                        </div>
                    ) : (
                        <div className="sr-tt-badge">
                            🎉 <strong>MAXIMUM SKILL REACHED</strong>
                        </div>
                    )}
                </div>
            </div>
            
            <div className="sr-info">
                <div className="sr-reading">
                    <span className="sr-number" style={{ color: skill.color }}>{animatedPct}%</span>
                    <span className={`sr-trend ${skill.trend.up ? 'up' : 'down'}`} title="Change since last week">
                        {skill.trend.up ? '▲' : '▼'} {skill.trend.val}%
                    </span>
                </div>
                <div className="sr-name">{skill.name.split(' ')[0]}</div>
            </div>
        </div>
    );
}
