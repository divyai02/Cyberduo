// src/utils/gameProgress.js

const DEFAULT_GAMES = {
    phishing: { completed: false, questionsDone: 0, totalQuestions: 5, name: "Phishing Frenzy", icon: "🎣" },
    password: { completed: false, questionsDone: 0, totalQuestions: 5, name: "Password Protector", icon: "🔑" },
    malware: { completed: false, questionsDone: 0, totalQuestions: 5, name: "Malware Mayhem", icon: "🦠" },
    firewall: { completed: false, questionsDone: 0, totalQuestions: 5, name: "Firewall Defender", icon: "🛡️" },
    scams: { completed: false, questionsDone: 0, totalQuestions: 5, name: "Scam Spotter", icon: "🕵️" },
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
            return JSON.parse(stored);
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
