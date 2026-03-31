import React, { useState } from 'react';

const SettingsModal = ({ isOpen, onClose, currentMode, onSave }) => {
    const [mode, setMode] = useState(currentMode || "free");
    const [showWarning, setShowWarning] = useState(false);

    if (!isOpen) return null;

    const handleModeToggle = (newMode) => {
        if (newMode !== currentMode) {
            setShowWarning(true);
        } else {
            setShowWarning(false);
        }
        setMode(newMode);
    };

    const handleSave = () => {
        const resetProgress = mode !== currentMode;
        onSave({ mode, resetProgress });
        onClose();
    };

    return (
        <div className="db-modal-overlay" onClick={onClose}>
            <div className="db-modal-content" onClick={(e) => e.stopPropagation()}>
                <button className="db-modal-close" onClick={onClose}>×</button>
                <h2 className="db-modal-title">Academy Settings</h2>
                
                <div className="db-edit-section">
                    <label className="db-modal-label">Learning Mode Selection</label>
                    <div className="db-mode-picker">
                        <button
                            className={`db-mode-option ${mode === 'free' ? 'active' : ''}`}
                            onClick={() => handleModeToggle('free')}
                        >
                            <span className="db-mode-icon">🎮</span>
                            <div className="db-mode-text">
                                <span className="db-mode-title">FREE MODE</span>
                                <span className="db-mode-desc">Unlock levels freely with ANY 3 game completions per level.</span>
                            </div>
                        </button>

                        <button
                            className={`db-mode-option ${mode === 'path' ? 'active' : ''}`}
                            onClick={() => handleModeToggle('path')}
                        >
                            <span className="db-mode-icon">🗺️</span>
                            <div className="db-mode-text">
                                <span className="db-mode-title">PATH MODE</span>
                                <span className="db-mode-desc">Standard structured path. Complete ALL games to proceed.</span>
                            </div>
                        </button>
                    </div>
                </div>

                {showWarning && (
                    <div className="db-modal-warning">
                        <span className="db-warning-icon">⚠️</span>
                        <div className="db-warning-text">
                            <strong>WARNING:</strong> Switching modes will reset all current mission progress. 
                            XP and Badges will be preserved.
                        </div>
                    </div>
                )}

                <div className="db-modal-actions">
                    <button className="db-btn-secondary" onClick={onClose}>CANCEL</button>
                    <button className="db-btn-primary" onClick={handleSave}>APPLY CHANGES</button>
                </div>
            </div>
        </div>
    );
};

export default SettingsModal;
