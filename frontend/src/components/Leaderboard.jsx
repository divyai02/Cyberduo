import React, { useState, useEffect, useMemo } from 'react';
import '../styles/leaderboard.css';
import mockData from '../data/leaderboard.json';

const AVATAR_MAP = {
    "hacker": { emoji: "🦸", label: "Hacker Hero" },
    "agent": { emoji: "🦹", label: "Cyber Agent" },
    "cat": { emoji: "🐱", label: "Cyber Cat" },
    "bot": { emoji: "🤖", label: "AI Bot" },
    "ninja": { emoji: "👩‍💻", label: "Code Ninja" },
};

const DEFAULT_AVATAR = { emoji: "🛡️", label: "Operative" };

const XPCountUp = ({ value, duration = 1500 }) => {
    const [count, setCount] = useState(0);
    useEffect(() => {
        let start = 0;
        const end = parseInt(value, 10) || 0;
        if (start === end) { setCount(end); return; }
        let totalMiliseconds = duration;
        let incrementTime = 15;
        let totalSteps = Math.floor(totalMiliseconds / incrementTime);
        let increment = end / totalSteps;
        let timer = setInterval(() => {
            start += increment;
            if (start >= end) { setCount(end); clearInterval(timer); }
            else { setCount(Math.floor(start)); }
        }, incrementTime);
        return () => clearInterval(timer);
    }, [value, duration]);
    return <span>{count.toLocaleString()} XP</span>;
};

const PodiumItem = ({ user, rank, type }) => {
    return (
        <div className={`podium-item ${type}`}>
            <div className="podium-avatar-wrap">
                {rank === 1 && <div className="podium-crown">👑</div>}
                <div className="podium-avatar">{user.avatar}</div>
            </div>
            <div className="podium-base">
                <div className="podium-rank">#{rank}</div>
                <div className="podium-name">
                    {user.name}
                    {user.isCurrentUser && <span className="lb-table-you">YOU</span>}
                </div>
                <div className="podium-xp"><XPCountUp value={user.xp} /></div>
            </div>
        </div>
    );
};

const Leaderboard = ({ compact = false }) => {
    const [userXP, setUserXP] = useState(0);
    const [userData, setUserData] = useState({ name: 'You', avatar: '🛡️' });

    useEffect(() => {
        const updateFromStorage = () => {
            const xp = localStorage.getItem("userXP");
            const storedUsername = localStorage.getItem("cyberduo_username") || "You";
            const avatarId = localStorage.getItem("cyberduo_avatar");
            const avatar = AVATAR_MAP[avatarId]?.emoji || DEFAULT_AVATAR.emoji;
            setUserXP(xp ? parseInt(xp, 10) : 0);
            setUserData({ name: storedUsername, avatar });
        };
        updateFromStorage();
        window.addEventListener('storage', updateFromStorage);
        window.addEventListener('xpUpdated', updateFromStorage);
        return () => {
            window.removeEventListener('storage', updateFromStorage);
            window.removeEventListener('xpUpdated', updateFromStorage);
        };
    }, []);

    const allRankings = useMemo(() => {
        const currentUser = {
            id: 'current-user',
            name: userData.name,
            avatar: userData.avatar,
            xp: userXP,
            isCurrentUser: true
        };
        const combined = [...mockData, currentUser].sort((a, b) => b.xp - a.xp);
        return combined.map((user, index) => ({ ...user, rank: index + 1 }));
    }, [userXP, userData]);

    if (compact) {
        return (
            <div className="lb-compact-container">
                <div className="lb-compact-header">
                    <span className="lb-compact-title">🏆 Top Academy Operatives</span>
                </div>
                <div className="lb-compact-list">
                    {allRankings.slice(0, 5).map((user) => (
                        <div key={user.id} className={`lb-compact-row ${user.isCurrentUser ? 'you' : ''}`}>
                            <span className="lb-compact-rank">#{user.rank}</span>
                            <span className="lb-compact-avatar">{user.avatar}</span>
                            <span className="lb-compact-name">{user.name}</span>
                            <span className="lb-compact-xp">{user.xp.toLocaleString()} XP</span>
                        </div>
                    ))}
                    {!allRankings.slice(0, 5).some(u => u.isCurrentUser) && (
                        <div className="lb-compact-row you mt-2">
                             <span className="lb-compact-rank">#{allRankings.find(u => u.isCurrentUser).rank}</span>
                             <span className="lb-compact-avatar">{userData.avatar}</span>
                             <span className="lb-compact-name">{userData.name}</span>
                             <span className="lb-compact-xp">{userXP.toLocaleString()} XP</span>
                        </div>
                    )}
                </div>
            </div>
        );
    }

    const top3 = allRankings.slice(0, 3);
    const others = allRankings.slice(3);
    const first = top3.find(u => u.rank === 1);
    const second = top3.find(u => u.rank === 2);
    const third = top3.find(u => u.rank === 3);

    return (
        <div className="lb-full-container">
            <header className="lb-page-header">
                <h1 className="lb-page-title">ELITE OPERATIVES</h1>
                <p className="lb-page-subtitle">Cyber Academy Global Rankings</p>
            </header>

            <section className="lb-podium">
                {second && <PodiumItem user={second} rank={2} type="second" />}
                {first && <PodiumItem user={first} rank={1} type="first" />}
                {third && <PodiumItem user={third} rank={3} type="third" />}
            </section>

            <section className="lb-grid-list">
                <div className="lb-table-header">
                    <span>Rank</span>
                    <span style={{ textAlign: 'center' }}>Avatar</span>
                    <span>Operative Name</span>
                    <span style={{ textAlign: 'right' }}>Experience Points</span>
                </div>
                <div className="lb-table-body">
                    {others.map((user) => (
                        <div key={user.id} className={`lb-table-row ${user.isCurrentUser ? 'you' : ''}`}>
                            <div className="lb-row-rank">#{user.rank}</div>
                            <div className="lb-row-avatar">{user.avatar}</div>
                            <div className="lb-row-name">
                                {user.name}
                                {user.isCurrentUser && <span className="lb-table-you">YOU</span>}
                            </div>
                            <div className="lb-row-xp"><XPCountUp value={user.xp} /></div>
                        </div>
                    ))}
                    {/* If user not in others and not in top 3 (should be impossible with mock data, but for safety) */}
                    {allRankings.find(u => u.isCurrentUser)?.rank > allRankings.length && (
                         <div className="lb-table-row you">
                            <div className="lb-row-rank">#{allRankings.find(u => u.isCurrentUser).rank}</div>
                            <div className="lb-row-avatar">{userData.avatar}</div>
                            <div className="lb-row-name">{userData.name} <span className="lb-table-you">YOU</span></div>
                            <div className="lb-row-xp"><XPCountUp value={userXP} /></div>
                         </div>
                    )}
                </div>
            </section>
        </div>
    );
};

export default Leaderboard;
