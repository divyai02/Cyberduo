import { useState, useEffect } from "react";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:5000";

export default function AdminDashboard({ onLogout }) {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState("");

    useEffect(() => {
        const fetchUsers = async () => {
            try {
                const res = await fetch(`${API_BASE_URL}/user/admin/all-users`);
                const data = await res.json();
                setUsers(data);
            } catch (err) {
                console.error("Failed to fetch users:", err);
            } finally {
                setLoading(false);
            }
        };
        
        fetchUsers();
        
        // HEARTBEAT: Auto-refresh every 30 seconds
        const interval = setInterval(fetchUsers, 30000);
        return () => clearInterval(interval);
    }, []);

    const filteredUsers = users.filter(u => 
        u.username?.toLowerCase().includes(searchTerm.toLowerCase()) || 
        u.email?.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div className="admin-dashboard" style={{
            minHeight: "100vh",
            background: "#0A0F1F",
            color: "#fff",
            fontFamily: "'Orbitron', sans-serif",
            padding: "40px",
            position: "relative",
            zIndex: 10
        }}>
            {/* Header */}
            <div style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                marginBottom: "40px",
                borderBottom: "1px solid rgba(0,255,157,0.3)",
                paddingBottom: "20px"
            }}>
                <div>
                    <h1 style={{ color: "#00FF9D", margin: 0, letterSpacing: "4px", fontSize: "2rem" }}>COMMAND CENTER</h1>
                    <p style={{ color: "#4D9EFF", margin: "5px 0 0 0", fontSize: "0.9rem" }}>MONITORING GLOBAL OPERATIVES</p>
                </div>
                <button 
                    onClick={onLogout}
                    style={{
                        background: "rgba(255,77,77,0.1)",
                        border: "1px solid #FF4D4D",
                        color: "#FF4D4D",
                        padding: "10px 20px",
                        borderRadius: "8px",
                        cursor: "pointer",
                        fontWeight: "bold",
                        transition: "0.3s"
                    }}
                    onMouseEnter={e => e.target.style.background = "rgba(255,77,77,0.2)"}
                    onMouseLeave={e => e.target.style.background = "rgba(255,77,77,0.1)"}
                >
                    ABORT SESSION
                </button>
            </div>

            {/* Stats Overview */}
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: "20px", marginBottom: "40px" }}>
                <div className="stat-card" style={{ background: "rgba(0,255,157,0.05)", border: "1px solid rgba(0,255,157,0.2)", padding: "20px", borderRadius: "12px", textAlign: "center" }}>
                    <div style={{ color: "#00FF9D", fontSize: "0.8rem", marginBottom: "5px" }}>TOTAL OPERATIVES</div>
                    <div style={{ fontSize: "2rem", fontWeight: "bold" }}>{users.length}</div>
                </div>
                <div className="stat-card" style={{ background: "rgba(77,158,255,0.05)", border: "1px solid rgba(77,158,255,0.2)", padding: "20px", borderRadius: "12px", textAlign: "center" }}>
                    <div style={{ color: "#4D9EFF", fontSize: "0.8rem", marginBottom: "5px" }}>ACTIVE MISSIONS</div>
                    <div style={{ fontSize: "2rem", fontWeight: "bold" }}>{users.reduce((acc, u) => acc + (u.game_history?.length || 0), 0)}</div>
                </div>
            </div>

            {/* Search Bar */}
            <div style={{ marginBottom: "20px", position: "relative" }}>
                 <input 
                    type="text" 
                    placeholder="Search by Username or Email..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    style={{
                        width: "100%",
                        padding: "15px 20px",
                        background: "rgba(255,255,255,0.05)",
                        border: "1px solid rgba(255,255,255,0.1)",
                        borderRadius: "12px",
                        color: "#fff",
                        outline: "none",
                        fontSize: "1rem"
                    }}
                 />
            </div>

            {/* User Table */}
            <div style={{
                background: "rgba(255,255,255,0.02)",
                borderRadius: "15px",
                border: "1px solid rgba(255,255,255,0.05)",
                overflow: "hidden"
            }}>
                <table style={{ width: "100%", borderCollapse: "collapse", textAlign: "left" }}>
                    <thead style={{ background: "rgba(0,255,157,0.1)", color: "#00FF9D" }}>
                        <tr>
                            <th style={{ padding: "20px" }}>OPERATIVE</th>
                            <th style={{ padding: "20px" }}>STATUS/ROLE</th>
                            <th style={{ padding: "20px" }}>XP LVL</th>
                            <th style={{ padding: "20px" }}>STREAK</th>
                            <th style={{ padding: "20px" }}>PROGRESS</th>
                        </tr>
                    </thead>
                    <tbody>
                        {loading ? (
                            <tr><td colSpan="5" style={{ padding: "40px", textAlign: "center", color: "#B0B8CC" }}>LOADING DATA STREAMS...</td></tr>
                        ) : filteredUsers.length === 0 ? (
                            <tr><td colSpan="5" style={{ padding: "40px", textAlign: "center", color: "#B0B8CC" }}>NO OPERATIVES MATCH CRITERIA</td></tr>
                        ) : filteredUsers.map(user => (
                            <tr key={user.id} style={{ borderBottom: "1px solid rgba(255,255,255,0.05)", transition: "0.3s" }} onMouseEnter={e => e.currentTarget.style.background = "rgba(255,255,255,0.03)"} onMouseLeave={e => e.currentTarget.style.background = "transparent"}>
                                <td style={{ padding: "20px" }}>
                                    <div style={{ fontWeight: "bold", color: "#fff" }}>{user.username}</div>
                                    <div style={{ fontSize: "0.8rem", color: "#B0B8CC" }}>{user.email}</div>
                                </td>
                                <td style={{ padding: "20px" }}>
                                    <span style={{ 
                                        padding: "4px 10px", 
                                        borderRadius: "6px", 
                                        fontSize: "0.7rem", 
                                        background: user.role === 'admin' ? "rgba(77,158,255,0.2)" : "rgba(0,255,157,0.2)",
                                        color: user.role === 'admin' ? "#4D9EFF" : "#00FF9D",
                                        border: `1px solid ${user.role === 'admin' ? "#4D9EFF55" : "#00FF9D55"}`
                                    }}>
                                        {user.role === 'admin' ? "COMMAND" : "OPERATIVE"}
                                    </span>
                                </td>
                                <td style={{ padding: "20px", color: "#FFE100", fontWeight: "bold" }}>{user.xp} XP</td>
                                <td style={{ padding: "20px", color: "#FF4D4D" }}>⚡ {user.streak}</td>
                                <td style={{ padding: "20px" }}>
                                    <div style={{ fontSize: "0.8rem", color: "#B0B8CC" }}>
                                        {user.game_history?.length || 0} Missions Completed
                                    </div>
                                    {/* Simple progress bar based on 15 total missions (5 games x 3 levels) */}
                                    <div style={{ width: "100px", height: "4px", background: "rgba(255,255,255,0.1)", borderRadius: "2px", marginTop: "5px" }}>
                                        <div style={{ 
                                            width: `${Math.min(100, ((user.game_history?.length || 0) / 15) * 100)}%`, 
                                            height: "100%", 
                                            background: "#00FF9D", 
                                            boxShadow: "0 0 10px #00FF9D" 
                                        }} />
                                    </div>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
