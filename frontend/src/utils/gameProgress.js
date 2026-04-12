// src/utils/gameProgress.js

const DEFAULT_GAMES = {
    phishing: { completed: false, questionsDone: 0, totalQuestions: 25, name: "Phishing Frenzy", icon: "🎣" },
    password: { completed: false, questionsDone: 0, totalQuestions: 25, name: "Password Protector", icon: "🔑" },
    malware: { completed: false, questionsDone: 0, totalQuestions: 25, name: "Malware Mayhem", icon: "🦠" },
    firewall: { completed: false, questionsDone: 0, totalQuestions: 25, name: "Firewall Defender", icon: "🛡️" },
    scams: { completed: false, questionsDone: 0, totalQuestions: 25, name: "Scam Spotter", icon: "🕵️" },
};

const DEFAULT_PROGRESS = {
    beginner: JSON.parse(JSON.stringify(DEFAULT_GAMES)),
    medium: JSON.parse(JSON.stringify(DEFAULT_GAMES)),
    hard: JSON.parse(JSON.stringify(DEFAULT_GAMES)),
};

export function getGameProgress() {
    try {
        const stored = localStorage.getItem("cyberduo_game_progress");
        if (stored) {
            let parsed = JSON.parse(stored);
            // Force update all totalQuestions to 25 to ensure old caches update properly
            ['beginner', 'medium', 'hard'].forEach(level => {
                if (parsed[level]) {
                    Object.keys(parsed[level]).forEach(gameKey => {
                        parsed[level][gameKey].totalQuestions = 25;
                    });
                }
            });
            return parsed;
        }
    } catch (e) {
        console.error("Failed to parse game progress", e);
    }
    return JSON.parse(JSON.stringify(DEFAULT_PROGRESS));
}

export function updateGameProgress(level, gameKey, questionsDone) {
    const progress = getGameProgress();
    if (progress[level] && progress[level][gameKey]) {
        progress[level][gameKey].questionsDone = Math.min(questionsDone, progress[level][gameKey].totalQuestions);
        if (progress[level][gameKey].questionsDone >= progress[level][gameKey].totalQuestions) {
            progress[level][gameKey].completed = true;
        }
        localStorage.setItem("cyberduo_game_progress", JSON.stringify(progress));
        checkAndUnlockBadges(); // Check for new badges
    }
    return progress;
}

export function getLevelUnlockStatus(mode, progress, currentLevelStr) {
    if (currentLevelStr === "beginner") return true;

    const levels = ["beginner", "medium", "hard"];
    const currentIdx = levels.indexOf(currentLevelStr);
    if (currentIdx <= 0) return true;

    const prevLevelStr = levels[currentIdx - 1];
    const gamesOrder = ["phishing", "password", "malware", "firewall", "scams"];
    const prevGames = gamesOrder.map(k => progress[prevLevelStr][k]);

    if (mode === "free") {
        // Free Mode: Level unlocks after completing ANY 3 games of prev level
        const completedCount = prevGames.filter(g => g.completed).length;
        return completedCount >= 3;
    } else {
        // Path Mode: Level unlocks only after ALL 5 games of prev level
        return prevGames.every(g => g.completed);
    }
}

export function checkUnlockStatus(mode, progress, level, gameKey) {
    const isLevelUnlocked = getLevelUnlockStatus(mode, progress, level);
    if (!isLevelUnlocked) return false;

    if (mode === "free") {
        // In Free Mode, all games within unlocked level are accessible
        return true;
    } else {
        // In Path Mode, games within a level unlock sequentially
        const gamesOrder = ["phishing", "password", "malware", "firewall", "scams"];
        const gameIdx = gamesOrder.indexOf(gameKey);
        
        if (gameIdx === 0) return true;
        
        const prevGameKey = gamesOrder[gameIdx - 1];
        return progress[level][prevGameKey].completed;
    }
}

export function getStreakData() {
    try {
        const stored = localStorage.getItem("cyberduo_streak_data");
        if (stored) {
            return JSON.parse(stored);
        }
    } catch (e) {
        console.error("Failed to parse streak data", e);
    }
    return {
        currentStreak: 0,
        longestStreak: 0,
        lastPlayed: null, // YYYY-MM-DD
        streakHistory: [] // array of YYYY-MM-DD
    };
}

export function updateStreak() {
    const streak = getStreakData();
    const today = new Date();
    
    // adjust to exactly YYYY-MM-DD local time string
    const getLocalYYYYMMDD = (d) => {
        const year = d.getFullYear();
        const month = String(d.getMonth() + 1).padStart(2, '0');
        const day = String(d.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    };

    const todayStr = getLocalYYYYMMDD(today);

    if (streak.lastPlayed === todayStr) {
        // Already played today, no change
        return { streak, reward: null };
    }

    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    const yesterdayStr = getLocalYYYYMMDD(yesterday);

    let streakIncreased = false;

    if (streak.lastPlayed === yesterdayStr) {
        // Played yesterday, increase streak
        streak.currentStreak += 1;
        streakIncreased = true;
    } else {
        // Last played before yesterday, reset streak
        streak.currentStreak = 1;
        streakIncreased = true;
    }

    streak.lastPlayed = todayStr;
    
    // add to history if not there
    if (!streak.streakHistory) {
        streak.streakHistory = [];
    }
    
    if (!streak.streakHistory.includes(todayStr)) {
        streak.streakHistory.push(todayStr);    
    }
    
    if (streak.currentStreak > streak.longestStreak) {
        streak.longestStreak = streak.currentStreak;
    }

    // Determine rewards
    let reward = null;
    if (streakIncreased) {
        if (streak.currentStreak === 3) {
            reward = { xp: 10, badge: null };
        } else if (streak.currentStreak === 7) {
            reward = { xp: 50, badge: "Flame Keeper" };
        } else if (streak.currentStreak === 14) {
            reward = { xp: 100, badge: "Circuit Master" };
        } else if (streak.currentStreak === 30) {
            reward = { xp: 500, badge: "Legendary Streak" };
        }
    }

    localStorage.setItem("cyberduo_streak_data", JSON.stringify(streak));
    
    // Dispatch event so StreakTracker can update in real-time
    if (typeof window !== 'undefined') {
        const event = new Event('streakUpdated');
        window.dispatchEvent(event);
    }

    return { streak, reward };
}

export function calculateSkillRadar(progress) {
    if (!progress) return [];
    
    const skills = [
        { key: 'phishing', name: 'Phishing Frenzy', icon: '🎯' }, 
        { key: 'password', name: 'Password Protector', icon: '🔐' },
        { key: 'malware', name: 'Malware Mayhem', icon: '🦠' },
        { key: 'firewall', name: 'Firewall Defender', icon: '🔥' },
        { key: 'scams', name: 'Scam Spotter', icon: '💰' }
    ];

    const radarData = skills.map(skill => {
        const beginnerDone = progress.beginner?.[skill.key]?.questionsDone || 0;
        const mediumDone = progress.medium?.[skill.key]?.questionsDone || 0;
        const hardDone = progress.hard?.[skill.key]?.questionsDone || 0;
        
        const totalDone = beginnerDone + mediumDone + hardDone;
        // Total possible per skill across 3 levels: 25 + 25 + 25 = 75
        const maxQuestions = 75; 
        const percentage = Math.round((totalDone / maxQuestions) * 100);
        
        // Set colors based on percentage
        let color = '#00FF9D'; // green
        if (percentage <= 40) color = '#FF4D4D'; // red
        else if (percentage <= 70) color = '#FFB800'; // yellow

        // Calculate milestones
        let nextBadge = '';
        let neededForNext = '';
        if (percentage < 33) {
            nextBadge = 'Bronze';
            neededForNext = 33 - percentage;
        } else if (percentage < 66) {
            nextBadge = 'Silver';
            neededForNext = 66 - percentage;
        } else if (percentage < 100) {
            nextBadge = 'Gold';
            neededForNext = 100 - percentage;
        } else {
            nextBadge = 'MAXED';
            neededForNext = 0;
        }
        
        // Create mock trend
        const isUp = Math.random() > 0.3;
        const trendVal = Math.floor(Math.random() * 5) + 1;

        return {
            key: skill.key,
            name: skill.name,
            icon: skill.icon,
            percentage,
            color,
            breakdown: {
                beginner: beginnerDone,
                medium: mediumDone,
                hard: hardDone
            },
            nextBadge,
            neededForNext,
            trend: { up: isUp, val: trendVal }
        };
    });
    
    return radarData;
}


export function getCurrentUserXP() {
    try {
        const xp = localStorage.getItem("userXP");
        return xp ? parseInt(xp, 10) : 0;
    } catch (e) {
        console.error("Failed to get user XP", e);
        return 0;
    }
}

export function updateUserXP(earnedXP) {
    try {
        const currentXP = getCurrentUserXP();
        const newXP = currentXP + earnedXP;
        localStorage.setItem("userXP", newXP.toString());
        
        // Dispatch event so Leaderboard and other components can update
        if (typeof window !== 'undefined') {
            const event = new Event('xpUpdated');
            window.dispatchEvent(event);
            checkAndUnlockBadges(); // Check for new badges (like 500 XP club)
        }
        return newXP;
    } catch (e) {
        console.error("Failed to update user XP", e);
        return getCurrentUserXP();
    }
}

export function checkAndUnlockBadges() {
    try {
        const xp = getCurrentUserXP();
        const progress = getGameProgress();
        const streakData = getStreakData();
        const earned = JSON.parse(localStorage.getItem('cyberduo_earned_badges') || '[]');

        const badgesMetadata = [
            // ---- Game completion (any level) ----
            { id: 'phishing_rookie',       type: 'completeGame',     val: 'phishing' },
            { id: 'password_apprentice',   type: 'completeGame',     val: 'password' },
            { id: 'malware_hunter',        type: 'completeGame',     val: 'malware' },
            { id: 'firewall_novice',       type: 'completeGame',     val: 'firewall' },
            { id: 'scam_spotter',          type: 'completeGame',     val: 'scams' },
            // ---- Level completionist ----
            { id: 'beginner_completionist',type: 'completeLevel',    val: 'beginner' },
            { id: 'medium_completionist',  type: 'completeLevel',    val: 'medium' },
            { id: 'hard_completionist',    type: 'completeLevel',    val: 'hard' },
            // ---- Streak ----
            { id: 'seven_day_warrior',     type: 'streakDays',       val: 7 },
            { id: 'fourteen_day_champion', type: 'streakDays',       val: 14 },
            { id: 'thirty_day_legend',     type: 'streakDays',       val: 30 },
            // ---- XP milestones ----
            { id: 'five_hundred_xp_club',  type: 'totalXP',          val: 500 },
            { id: 'thousand_xp_breaker',   type: 'totalXP',          val: 1000 },
            { id: 'two_five_hundred_xp_titan', type: 'totalXP',      val: 2500 },
            { id: 'five_k_xp_overlord',    type: 'totalXP',          val: 5000 },
            // ---- Two-level game mastery ----
            { id: 'phishing_master',       type: 'twoLevelsGame',    val: 'phishing' },
            { id: 'password_guardian',     type: 'twoLevelsGame',    val: 'password' },
            // ---- Specific hard level game completion ----
            { id: 'malware_architect',     type: 'completeLevelGame', val: { level: 'hard', game: 'malware' } },
            { id: 'firewall_commander',    type: 'completeLevelGame', val: { level: 'hard', game: 'firewall' } },
            { id: 'scam_investigator',     type: 'completeLevelGame', val: { level: 'hard', game: 'scams' } },
            // ---- Meta achievements ----
            { id: 'all_domains_cleared',   type: 'allGamesOnce',     val: true },
            { id: 'academy_graduate',      type: 'fullMastery',      val: true },
        ];

        const gamesOrder = ['phishing', 'password', 'malware', 'firewall', 'scams'];
        let newlyEarned = [];

        badgesMetadata.forEach(badge => {
            if (earned.includes(badge.id)) return;

            let met = false;

            if (badge.type === 'completeGame') {
                met = ['beginner', 'medium', 'hard'].some(l => progress[l]?.[badge.val]?.completed);

            } else if (badge.type === 'completeLevel') {
                const games = Object.values(progress[badge.val] || {});
                met = games.length >= 5 && games.every(g => g.completed);

            } else if (badge.type === 'streakDays') {
                met = (streakData.currentStreak || 0) >= badge.val;

            } else if (badge.type === 'totalXP') {
                met = xp >= badge.val;

            } else if (badge.type === 'twoLevelsGame') {
                const beg = progress.beginner?.[badge.val]?.completed;
                const med = progress.medium?.[badge.val]?.completed;
                met = beg && med;

            } else if (badge.type === 'completeLevelGame') {
                met = progress[badge.val.level]?.[badge.val.game]?.completed;

            } else if (badge.type === 'allGamesOnce') {
                met = gamesOrder.every(g =>
                    ['beginner', 'medium', 'hard'].some(l => progress[l]?.[g]?.completed)
                );

            } else if (badge.type === 'fullMastery') {
                const all = ['beginner', 'medium', 'hard'].flatMap(l => Object.values(progress[l] || {}));
                met = all.length >= 15 && all.every(g => g.completed);
            }

            if (met) {
                earned.push(badge.id);
                newlyEarned.push(badge.id);
            }
        });

        if (newlyEarned.length > 0) {
            localStorage.setItem('cyberduo_earned_badges', JSON.stringify(earned));
            newlyEarned.forEach(id => {
                const medalName = id.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
                alert(`🏆 New Badge Unlocked: ${medalName}!`);
                if (typeof window !== 'undefined') {
                    window.dispatchEvent(new CustomEvent('badgeUnlocked', { detail: { id } }));
                }
            });
        }
    } catch (e) {
        console.error('Failed to check badges', e);
    }
}
