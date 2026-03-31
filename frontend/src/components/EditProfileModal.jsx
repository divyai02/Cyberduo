import React, { useState } from 'react';
import { AVATARS } from './AvatarSelection.jsx';

const EditProfileModal = ({ isOpen, onClose, userData, onSave }) => {
    const [username, setUsername] = useState(userData.username || "");
    const [email, setEmail] = useState(userData.email || "");
    const [avatarId, setAvatarId] = useState(userData.avatarId || "hacker");

    if (!isOpen) return null;

    const handleSave = () => {
        onSave({ username, email, avatarId });
        onClose();
    };

    return (
        <div className="db-modal-overlay" onClick={onClose}>
            <div className="db-modal-content" onClick={(e) => e.stopPropagation()}>
                <button className="db-modal-close" onClick={onClose}>×</button>
                <h2 className="db-modal-title">Edit Operative Profile</h2>
                
                <div className="db-edit-section">
                    <label className="db-modal-label">Choose Persona</label>
                    <div className="db-avatar-picker">
                        {AVATARS.map((av) => (
                            <button
                                key={av.id}
                                className={`db-avatar-option ${avatarId === av.id ? 'active' : ''}`}
                                onClick={() => setAvatarId(av.id)}
                                title={av.name}
                            >
                                <span className="db-avatar-emoji">{av.emoji}</span>
                            </button>
                        ))}
                    </div>
                </div>

                <div className="db-edit-section">
                    <label className="db-modal-label">Username</label>
                    <input
                        type="text"
                        className="db-modal-input"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        placeholder="Operative Name"
                    />
                </div>

                <div className="db-edit-section">
                    <label className="db-modal-label">Email Address</label>
                    <input
                        type="email"
                        className="db-modal-input"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="operative@cyberduo.io"
                    />
                </div>

                <div className="db-modal-actions">
                    <button className="db-btn-secondary" onClick={onClose}>CANCEL</button>
                    <button className="db-btn-primary" onClick={handleSave}>SAVE CHANGES</button>
                </div>
            </div>
        </div>
    );
};

export default EditProfileModal;
