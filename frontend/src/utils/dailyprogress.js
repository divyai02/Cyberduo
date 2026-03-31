// dailyProgress.js
import { updateUserXP } from './gameProgress';

export function getTodayDate() {
    const d = new Date();
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

export function getTodayProgress() {
    try {
        const stored = localStorage.getItem("cyberduo_daily_progress");
        if (stored) {
            const data = JSON.parse(stored);
            const today = getTodayDate();
            if (data.date === today) {
                return data.count || 0;
            }
        }
    } catch (e) {
        console.error("Failed to parse daily progress", e);
    }
    return 0;
}

export function incrementDailyProgress() {
    const today = getTodayDate();
    let count = getTodayProgress();
    const newCount = count + 1;
    
    const wasAlreadyReached = count >= 1;
    const isNowReached = newCount >= 1;

    localStorage.setItem("cyberduo_daily_progress", JSON.stringify({
        date: today,
        count: newCount,
        rewardClaimed: wasAlreadyReached ? true : false // will set to true only when awarded
    }));

    // Check if goal newly reached
    let awarded = false;
    if (isNowReached && !wasAlreadyReached) {
        awarded = awardBonusXP();
    }

    // Dispatch event for UI
    if (typeof window !== 'undefined') {
        window.dispatchEvent(new CustomEvent('dailyGoalUpdated', { detail: { count: newCount, awarded } }));
    }

    return { count: newCount, awarded };
}

export function resetDailyIfNeeded() {
    const today = getTodayDate();
    const stored = localStorage.getItem("cyberduo_daily_progress");
    if (stored) {
        const data = JSON.parse(stored);
        if (data.date !== today) {
            localStorage.setItem("cyberduo_daily_progress", JSON.stringify({
                date: today,
                count: 0,
                rewardClaimed: false
            }));
        }
    } else {
        localStorage.setItem("cyberduo_daily_progress", JSON.stringify({
            date: today,
            count: 0,
            rewardClaimed: false
        }));
    }
}

export function isGoalReached() {
    return getTodayProgress() >= 1;
}

export function awardBonusXP() {
    try {
        const stored = localStorage.getItem("cyberduo_daily_progress");
        if (stored) {
            const data = JSON.parse(stored);
            if (data.rewardClaimed) return false; // Already awarded
            
            // Mark as claimed
            data.rewardClaimed = true;
            localStorage.setItem("cyberduo_daily_progress", JSON.stringify(data));
            
            // Award 20 XP
            updateUserXP(20);
            return true;
        }
    } catch (e) {
        console.error("Failed to award bonus XP", e);
    }
    return false;
}

// ---- NEW: Daily Dashboard Stats ----
import { getStreakData, getCurrentUserXP } from './gameProgress';

export function getDailyStats() {
    const streak = getStreakData();
    const totalXP = getCurrentUserXP();
    const progress = getTodayProgress();
    const isReached = isGoalReached();
    
    return {
        streak: streak.currentStreak || 0,
        totalXP: totalXP || 0,
        progress,
        isReached
    };
}
