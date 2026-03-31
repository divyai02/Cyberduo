import React, { useEffect, useState } from 'react';
import { getStreakData } from '../utils/gameProgress';
import '../styles/StreakTracker.css';

export default function StreakTracker() {
    const [streakData, setStreakData] = useState({
        currentStreak: 0,
        longestStreak: 0,
        lastPlayed: null,
        streakHistory: []
    });

    useEffect(() => {
        setStreakData(getStreakData());
        
        const handleStorageChange = () => {
             setStreakData(getStreakData());
        };
        
        window.addEventListener('storage', handleStorageChange);
        window.addEventListener('streakUpdated', handleStorageChange);
        
        return () => {
            window.removeEventListener('storage', handleStorageChange);
            window.removeEventListener('streakUpdated', handleStorageChange);
        };
    }, []);

    // Helper to get local YYYY-MM-DD
    const getLocalYYYYMMDD = (d) => {
        const year = d.getFullYear();
        const month = String(d.getMonth() + 1).padStart(2, '0');
        const day = String(d.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    };

    const today = new Date();
    const currentDayOfWeek = today.getDay(); // 0 is Sunday
    // Map to Monday(1) - Sunday(7)
    const daysSinceMonday = currentDayOfWeek === 0 ? 6 : currentDayOfWeek - 1;
    
    // Find Monday's date
    const mondayDate = new Date(today);
    mondayDate.setDate(today.getDate() - daysSinceMonday);

    const weekNodes = [];
    for (let i = 0; i < 7; i++) {
        const d = new Date(mondayDate);
        d.setDate(mondayDate.getDate() + i);
        
        const dateStr = getLocalYYYYMMDD(d);
        const dayAbbrev = d.toLocaleDateString('en-US', { weekday: 'short' }).toUpperCase();
        
        const isToday = dateStr === getLocalYYYYMMDD(today);
        const isCompleted = streakData.streakHistory.includes(dateStr);
        // Compare string alphabetically since it's YYYY-MM-DD format
        const isFuture = dateStr > getLocalYYYYMMDD(today);
        
        weekNodes.push({
            dateStr,
            dayAbbrev,
            isToday,
            isCompleted,
            isFuture
        });
    }

    const getNextReward = (currentStreak) => {
        if (currentStreak < 3) return { daysLeft: 3 - currentStreak, target: 3, xp: 10 };
        if (currentStreak < 7) return { daysLeft: 7 - currentStreak, target: 7, xp: 50 };
        if (currentStreak < 14) return { daysLeft: 14 - currentStreak, target: 14, xp: 100 };
        if (currentStreak < 30) return { daysLeft: 30 - currentStreak, target: 30, xp: 500 };
        return { daysLeft: 0, target: 'MAX', xp: 0 }; 
    };

    const nextReward = getNextReward(streakData.currentStreak);

    // Generate calendar days for the current month
    const currentYear = today.getFullYear();
    const currentMonth = today.getMonth(); // 0-11
    
    // First day of the month
    const firstDay = new Date(currentYear, currentMonth, 1);
    const lastDay = new Date(currentYear, currentMonth + 1, 0);
    
    // days in month
    const daysInMonth = lastDay.getDate();
    
    // day of week of first day (0-6, Sun-Sat)
    let firstDayOfWeek = firstDay.getDay(); 
    
    const calendarDays = [];
    
    // empty cells before the 1st
    for (let i = 0; i < firstDayOfWeek; i++) {
        calendarDays.push(null);
    }
    
    // actual days
    for (let d = 1; d <= daysInMonth; d++) {
        const dateObj = new Date(currentYear, currentMonth, d);
        const dateStr = getLocalYYYYMMDD(dateObj);
        const isCompleted = streakData.streakHistory.includes(dateStr);
        const isToday = dateStr === getLocalYYYYMMDD(today);
        const isFuture = dateStr > getLocalYYYYMMDD(today);
        
        calendarDays.push({
            dateStr,
            dayString: d.toString(),
            isCompleted,
            isToday,
            isFuture
        });
    }

    return (
        <div className="st-streak-container">
            <h2 className="st-title">Activity Protocol</h2>
            
            <div className="st-circuit-board">
                {weekNodes.map((node, index) => {
                    let statusClass = "unplayed";
                    let icon = "⭕";
                    
                    if (node.isFuture) {
                        statusClass = "future";
                        icon = "⭕";
                    } else if (node.isToday && !node.isCompleted) {
                        statusClass = "today";
                        icon = "🔥";
                    } else if (node.isCompleted) {
                        statusClass = "completed";
                        icon = "✅";
                    }

                    const isLineActive = node.isCompleted || (node.isToday && streakData.currentStreak > 0);

                    return (
                        <React.Fragment key={node.dateStr}>
                            <div className="st-node-wrapper" title={node.dateStr}>
                                <div className="st-day-label">{node.dayAbbrev}</div>
                                <div className={`st-day-node ${statusClass} ${node.isToday ? 'is-today-override' : ''}`}>
                                    <span className="st-node-icon">{icon}</span>
                                </div>
                            </div>
                            {index < weekNodes.length - 1 && (
                                <div className={`st-circuit-line ${isLineActive ? 'active' : ''}`}></div>
                            )}
                        </React.Fragment>
                    );
                })}
            </div>

            <div className="st-stats-row">
                <div className="st-stat-box">
                    <span className="st-stat-label">🔥 CURRENT STREAK</span>
                    <span className="st-stat-value current">{streakData.currentStreak} DAYS</span>
                </div>
                <div className="st-stat-box">
                    <span className="st-stat-label">🏆 LONGEST STREAK</span>
                    <span className="st-stat-value">{streakData.longestStreak} DAYS</span>
                </div>
            </div>

            <div className="st-reward-preview">
                {nextReward.target !== 'MAX' ? (
                    <>Next reward preview: "Complete <strong style={{color: '#00FF9D'}}>{nextReward.daysLeft}</strong> more days to reach <strong style={{color: '#00FF9D'}}>{nextReward.target}</strong> days and earn <strong>+{nextReward.xp} XP</strong>"</>
                ) : (
                    <>Legendary Status Achieved! Keep up the daily protocol.</>
                )}
            </div>

            <div className="st-calendar-section">
                <h3 className="st-subtitle">{today.toLocaleString('default', { month: 'long', year: 'numeric' })} Logs</h3>
                <div className="st-calendar-grid">
                    {['SUN','MON','TUE','WED','THU','FRI','SAT'].map(day => (
                        <div key={day} className="st-cal-header">{day}</div>
                    ))}
                    
                    {calendarDays.map((calDay, i) => {
                        if (!calDay) {
                            return <div key={`empty-${i}`} className="st-cal-cell empty"></div>;
                        }
                        
                        let cellClass = "unplayed";
                        if (calDay.isFuture) {
                             cellClass = "future";
                        } else if (calDay.isCompleted) {
                             cellClass = "completed";
                        } else if (calDay.isToday) {
                             cellClass = "today"; // today but not completed yet
                        }

                        return (
                            <div key={calDay.dateStr} className={`st-cal-cell ${cellClass} ${calDay.isToday ? 'is-today' : ''}`} title={calDay.dateStr}>
                                <span className="st-cal-date">{calDay.dayString}</span>
                                {calDay.isCompleted && <span className="st-cal-icon">✅</span>}
                                {(calDay.isToday && !calDay.isCompleted) && <span className="st-cal-icon">🔥</span>}
                            </div>
                        );
                    })}
                </div>
            </div>
        </div>
    );
}
