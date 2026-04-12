import React, { useState, useEffect, useMemo } from 'react';
import '../styles/leaderboard.css';
import { AVATARS } from './AvatarSelection.jsx';

const API_BASE_URL = "http://localhost:5000";

// Helper to get emoji from ID using the shared AVATARS list
const getAvatarEmoji = (id) => {
    const av = AVATARS.find(a => a.id === id);
    return av ? av.emoji : "🛡️";
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
    const [userData, setUserData] = useState({ id: null, name: 'You', avatar: '🛡️' });
    const [rankings, setRankings] = useState([]);
    const [loading, setLoading] = useState(true);

    const fetchLeaderboard = async () => {
        try {
            const resp = await fetch(`${API_BASE_URL}/user/leaderboard?_t=${Date.now()}`, { cache: 'no-store' });
            const data = await resp.json();
            if (resp.ok) {
                // Map the avatar IDs to emojis
                const mapped = data.map(u => ({
                    ...u,
                    avatar: getAvatarEmoji(u.avatar)
                }));
                setRankings(mapped);
            }
        } catch (err) {
            console.error("Leaderboard fetch failed:", err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchLeaderboard();

        // Re-fetch leaderboard whenever user returns to the tab or XP is updated
        const handleVisibility = () => { if (document.visibilityState === 'visible') fetchLeaderboard(); };
        const handleXPUpdate = () => fetchLeaderboard();

        document.addEventListener('visibilitychange', handleVisibility);
        window.addEventListener('xpUpdated', handleXPUpdate);
        window.addEventListener('leaderboardRefresh', handleXPUpdate);
        
        const updateFromStorage = () => {
            const stored = localStorage.getItem("cyberduo_user_data");
            if (stored) {
                const data = JSON.parse(stored);
                setUserData({ 
                    id: data.user_id,
                    name: data.username, 
                    avatar: getAvatarEmoji(data.avatarId) 
                });
            }
            const xp = localStorage.getItem("userXP");
            setUserXP(xp ? parseInt(xp, 10) : 0);
        };
        updateFromStorage();
        window.addEventListener('storage', updateFromStorage);
        window.addEventListener('xpUpdated', updateFromStorage);
        return () => {
            document.removeEventListener('visibilitychange', handleVisibility);
            window.removeEventListener('xpUpdated', handleXPUpdate);
            window.removeEventListener('leaderboardRefresh', handleXPUpdate);
            window.removeEventListener('storage', updateFromStorage);
            window.removeEventListener('xpUpdated', updateFromStorage);
        };
    }, []);

    const allRankings = useMemo(() => {
        // Find current user in rankings by ID
        const currentInList = rankings.find(r => r.id === userData.id);
        
        let list = [...rankings];
        
        // If current user isn't in top 50 (returned by API), add them manually for display
        if (!currentInList && userData.id) {
            list.push({
                id: userData.id,
                name: userData.name,
                avatar: userData.avatar,
                xp: userXP,
                isCurrentUser: true
            });
        }
        
        const sorted = list.sort((a, b) => b.xp - a.xp);
        return sorted.map((user, index) => ({ 
            ...user, 
            rank: index + 1,
            isCurrentUser: user.id === userData.id
        }));
    }, [rankings, userXP, userData]);

    if (loading) return <div className="lb-loading">ACCESSING GLOBAL RANKINGS...</div>;

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
