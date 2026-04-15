# CyberDuo: Project Comprehensive Documentation

CyberDuo is a premium, gamified cybersecurity education platform designed to transform complex security concepts into an engaging, interactive learning experience. It targets non-technical users, students, and professionals through cinematic storytelling and real-world threat analysis.

---

## 🚀 Core Vision & Philosophy
**Goal**: "Learn Cybersecurity Like Playing a Game."
CyberDuo bridges the gap between technical complexity and user awareness. It uses a **Cyber-Neon (Cyberpunk) aesthetic** to create an immersive environment where users learn by doing, not just reading.

---

## 🛠️ Technology Stack

### **1. Frontend (The Operative Interface)**
- **Framework**: React.js (Bootstrapped with Vite for speed).
- **Styling**: Vanilla CSS (CSS3) using a custom **Neon Design System**.
  - Components use Glassmorphism effects, gradient borders, and heavy micro-animations.
  - Fully responsive layouts for desktop viewing.
- **State Management**: React Hooks (`useState`, `useEffect`, `useContext`) and **LocalStorage** for mission persistence.
- **Visuals**: AI-generated character avatars and cinematic story frames.

### **2. Backend (Command Center API)**
- **Framework**: FastAPI (Python 3.10+).
- **Database**: MongoDB Atlas (Cloud NoSQL) for secure storage of:
  - User profiles and high-score leaderboards.
  - Mastery badges and daily streaks.
  - Mission completion history.
- **Security**: Pydantic based data validation and JWT-ready authentication architecture.

### **3. Third-Party Integrations**
- **News Engine**: `NewsData.io` API relay (Backend-to-Frontend) for live Indian cyber threat alerts.
- **AI Core**: **Google Gemini 2.0 Flash** integration for a real-time "CyberSec AI Assistant" capable of explaining threats at any moment.

---

## 💎 Key Features & Modules

### **A. Operative Dashboard**
- **Stat Tracking**: Visualizes XP, Levels, and Badges.
- **Daily Goals**: Encourages consistent learning through a "Daily Mission" counter.
- **Global Leaderboard**: A real-time ranking system to foster healthy competition among recruits.

### **B. Cyber Alert News (Real-Time)**
- Fetches live cybercrime news specifically from India.
- **Risk Meter**: Each news item is analyzed and assigned a risk score from 1-10.
- **Game Domain Mapping**: Categorizes news into domains like "Phishing Frenzy" or "Malware Mayhem."

### **C. The Training Modules (375+ Scenarios)**
Interactive challenges across five key domains:
1. **Phishing Frenzy**: Identifying fake emails, domains, and deceptive links.
2. **Malware Mayhem**: Detecting ransomware, fake updates, and trojans.
3. **Password Protector**: Mastering complexity, MFA, and breach response.
4. **Firewall Defender**: Understanding network boundaries and secure connections.
5. **Scam Spotter**: Identifying "Digital Arrest" scams, financial fraud, and identity theft.

### **D. CyberComics: Interactive Story Mode**
A cinematic adventure where the user plays as "Operative Kabir."
- **Branching Narratives**: Decisions made during the story affect the character's success.
- **Visual Storytelling**: High-quality frames with a dramatic "Night City" feel.
- **Integrated AI Help**: Recruits can "Ask the AI" directly within the story if they encounter a term they don't understand.

---

## 📂 Project Structure

### **CyberDuo_AllContent (Core Repository)**
```text
/backend
  ├── app/
  │   ├── routes/        # API Endpoints (auth, user, games, alerts)
  │   ├── database.py    # MongoDB Connection & Collection logic
  │   └── main.py        # FastAPI Entry & CORS configuration
  ├── .env               # API Keys (NewsData, MongoDB)
  └── insert_*.py        # Heavy-duty scripts to populate 375+ questions
/frontend
  ├── src/
  │   ├── components/    # Reusable UI (CyberAlert, Dashboard, Leaderboard)
  │   ├── styles/        # The Project's Design System (CSS)
  │   └── data/          # JSON Fallbacks for offline resilience
  └── .env               # VITE_GEMINI_API_KEY
```

### **Cyber_comics (Interactive Module)**
```text
/src
  ├── components/        # StoryPlayer.jsx (Cinema engine)
  ├── data/              # story_main.json (Complete story beats)
  └── styles/            # Cinematic layout & animation CSS
```

---

## 🚦 Deployment & Initialization

1. **System Requirements**: Node.js, Python 3.10+, MongoDB.
2. **Backend Setup**:
   - `python -m venv venv`
   - `source venv/bin/activate` or `.\venv\Scripts\Activate`
   - `pip install uvicorn fastapi pymongo python-dotenv`
   - `uvicorn app.main:app --reload --port 5000`
3. **Frontend Setup**:
   - `npm install`
   - `npm run dev`
4. **Global Start**: Launching `start_app.bat` initializes both the Main Service and the Story Service.

---

## 📈 Future Roadmap
- Implementation of Hard-Mode certification exams.
- Multi-language support for regional awareness.
- Deep-dive forensics simulator module.
