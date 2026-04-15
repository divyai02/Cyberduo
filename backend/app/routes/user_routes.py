from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..database import users_collection
from datetime import datetime, date
from bson import ObjectId
import os
import urllib.request
import json
from typing import Optional

router = APIRouter(prefix="/user", tags=["user"])

# ✅ GET USER DASHBOARD DATA
@router.get("/dashboard/{user_id}")
def get_dashboard(user_id: str):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "username": user.get("username"),
        "avatar": user.get("avatar"),
        "mode": user.get("mode"),
        "xp": user.get("xp", 0),
        "streak": user.get("streak", 0),
        "badges": user.get("badges", []),
        "games_played": user.get("games_played", 0),
        "daily_questions_done": user.get("daily_questions_done", 0),
        "daily_goal_total": 10, # Goal is now 10 questions
        "games_unlocked": user.get("games_unlocked", ["phishing"]),
    }


# ✅ UPDATE STREAK
class StreakUpdate(BaseModel):
    user_id: str
    reported_streak: Optional[int] = None

@router.post("/update-streak")
def update_streak(data: StreakUpdate):
    user = users_collection.find_one({"_id": ObjectId(data.user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    today = date.today().isoformat()
    last_login = user.get("last_login_date", "")
    streak = user.get("streak", 0)

    if last_login == today:
        # Recovery: If current server streak is 0 or less than reported, bridge it
        reconciled = False
        if data.reported_streak is not None and data.reported_streak > streak:
            streak = data.reported_streak
            reconciled = True
        elif streak == 0:
            streak = 1
            reconciled = True
            
        if reconciled:
            users_collection.update_one(
                {"_id": ObjectId(data.user_id)},
                {"$set": {"streak": streak}}
            )
        return {"message": "Already updated today", "streak": streak}

    import datetime as dt
    yesterday = (dt.date.today() - dt.timedelta(days=1)).isoformat()
    
    # Honor higher local streak if provided
    if data.reported_streak is not None and data.reported_streak > (streak + 1):
         streak = data.reported_streak
    elif last_login == yesterday:
        streak += 1
    else:
        streak = 1

    users_collection.update_one(
        {"_id": ObjectId(data.user_id)},
        {"$set": {
            "streak": streak,
            "last_login_date": today
        }}
    )

    return {"message": "Streak updated!", "streak": streak}


# ✅ GET GLOBAL LEADERBOARD
@router.get("/leaderboard")
def get_leaderboard():
    # Fetch all users, sort by XP descending, limit to top 50
    users = users_collection.find({}, {"username": 1, "avatar": 1, "xp": 1}).sort("xp", -1).limit(50)
    
    leaderboard = []
    for user in users:
        leaderboard.append({
            "id": str(user["_id"]),
            "name": user.get("username"),
            "avatar": user.get("avatar"),
            "xp": user.get("xp", 0)
        })
    
    return leaderboard


# ✅ UPDATE USER PROFILE
class UserUpdate(BaseModel):
    user_id: str
    username: str = None
    email: str = None
    avatar: str = None
    mode: str = None

@router.post("/update")
def update_user(data: UserUpdate):
    # Prepare update payload
    update_ops = {}
    if data.username: update_ops["username"] = data.username
    if data.email: update_ops["email"] = data.email
    if data.avatar: update_ops["avatar"] = data.avatar
    if data.mode: update_ops["mode"] = data.mode
    
    if not update_ops:
        return {"message": "No fields to update"}
        
    result = users_collection.update_one(
        {"_id": ObjectId(data.user_id)},
        {"$set": update_ops}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
        
    return {"message": "Profile updated!", "updated_fields": update_ops}

# ✅ SYNC LOCAL STORAGE STATE
class SyncStateRequest(BaseModel):
    user_id: str
    sync_data: dict

@router.post("/sync")
def sync_user_state(data: SyncStateRequest):
    users_collection.update_one(
        {"_id": ObjectId(data.user_id)},
        {"$set": {"sync_data": data.sync_data}}
    )
    return {"message": "State synced successfully"}

@router.get("/sync/{user_id}")
def get_user_state(user_id: str):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"sync_data": user.get("sync_data", {})}
# ✅ ADMIN: GET ALL USERS (FOR COMMAND DASHBOARD)
@router.get("/admin/all-users")
def get_all_users():
    # In a real app, we would verify the requester's admin role here
    # Include sync_data to ensure streaks are correctly reconciled for the Admin
    users = users_collection.find({}, {
        "hashed_password": 0
    })
    
    all_users = []
    for user in users:
        # Extract streak from sync_data if primary streak is 0
        sync_data = user.get("sync_data", {}) or {}
        streak = user.get("streak", 0)
        
        # Look for the streak in Cloud Sync if the primary index is zero
        if streak == 0 and "cyberduo_streak_data" in sync_data:
            s_data = sync_data["cyberduo_streak_data"]
            try:
                if isinstance(s_data, str):
                    import json
                    s_data = json.loads(s_data)
                
                if isinstance(s_data, dict):
                    streak = s_data.get("currentStreak", 0)
            except:
                pass

        u = {
            "id": str(user["_id"]),
            "username": user.get("username"),
            "email": user.get("email"),
            "name": user.get("name"),
            "role": user.get("role", "user"),
            "xp": user.get("xp", 0),
            "streak": streak,
            "badges": user.get("badges", []),
            "games_played": user.get("games_played", 0),
            "created_at": user.get("created_at"),
            "game_history": user.get("game_history", [])
        }
        all_users.append(u)
    
    return all_users

CORTEX_NEWS_VAULT = [
    {
        "title": "Major UPI Phishing Campaign Detected targeting Mumbai Professionals",
        "description": "Security researchers have identified a large-scale phishing ring impersonating bank officials to drain UPI accounts via malicious QR codes.",
        "pubDate": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source_id": "cortex_vault"
    },
    {
        "title": "Deepfake Video Scam causes ripples in Delhi Financial Sector",
        "description": "A sophisticated deepfake video of a CEO was used to authorize an emergency transfer of 5 Crores. Forensic investigation is underway.",
        "pubDate": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source_id": "cortex_vault"
    },
    {
        "title": "Critical RCE Vulnerability found in popular Indian E-commerce Middleware",
        "description": "A Remote Code Execution flaw could expose millions of customer records. A patch is being rolled out across major vendors today.",
        "pubDate": (datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
        "source_id": "cortex_vault"
    },
    {
        "title": "New 'Digital Arrest' Scam variant targeting Bengaluru Tech Workers",
        "description": "Sophisticated scammers are posing as CBI officers in video calls, demanding exorbitant fees to 'clear' investigation records.",
        "pubDate": (datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
        "source_id": "cortex_vault"
    },
    {
        "title": "Ransomware Attack halts operations at Kolkata Logistics Firm",
        "description": "The 'DarkByte' group has claimed responsibility for encrypting core server databases. No data leak reported yet.",
        "pubDate": (datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
        "source_id": "cortex_vault"
    }
]

@router.get("/alerts/news")
def get_news():
    news_key = os.getenv("NEWS_API_KEY")
    if not news_key:
        print("NEWS_API_KEY not found! Using CORTEX_NEWS_VAULT.")
        return {"status": "success", "results": CORTEX_NEWS_VAULT, "source": "vault"}
    
    # Primary Search
    query = urllib.parse.quote('"cyber crime" OR cybercrime OR "online fraud" OR "digital arrest" OR hacker')
    url = f"https://newsdata.io/api/1/news?apikey={news_key}&q={query}&country=in&language=en"
    
    def fetch_data(target_url):
        try:
            req = urllib.request.Request(target_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                return json.loads(response.read().decode())
        except Exception as e:
            print(f"News Fetch Error ({target_url[:20]}...): {e}")
            return None

    data = fetch_data(url)
    
    # Fallback Logic: Broader search
    if not data or data.get("status") == "error" or not data.get("totalResults", 0):
        print("Broadening search due to zero results...")
        broad_query = urllib.parse.quote('cyber OR digital OR technology OR security')
        url = f"https://newsdata.io/api/1/news?apikey={news_key}&q={broad_query}&country=in&language=en"
        data = fetch_data(url)

    if data and data.get("status") == "success" and data.get("totalResults", 0) > 0:
        data["source"] = "live"
        return data
    
    # FINAL FORCEFUL FALLBACK: Vault
    print("API Failed or Empty. Using CORTEX_NEWS_VAULT to ensure visibility.")
    return {"status": "success", "results": CORTEX_NEWS_VAULT, "source": "vault"}

# ✅ SYNC DAILY MISSION PROGRESS
class SyncDaily(BaseModel):
    user_id: str
    count: int

@router.post("/sync-daily")
def sync_daily(data: SyncDaily):
    users_collection.update_one(
        {"_id": ObjectId(data.user_id)},
        {"$set": {"daily_questions_done": data.count}}
    )
    return {"message": "Daily mission progress synced", "count": data.count}


# ✅ SAVE CERTIFICATE TO USER PROFILE
class CertificateSave(BaseModel):
    user_id: str
    certificate_id: str
    issue_date: str

@router.post("/save-certificate")
def save_certificate(data: CertificateSave):
    user = users_collection.find_one({"_id": ObjectId(data.user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Only save if not already saved (idempotent)
    if user.get("certificate_earned"):
        return {
            "message": "Certificate already saved",
            "certificate_id": user.get("certificate_id"),
            "issue_date": user.get("certificate_date")
        }

    users_collection.update_one(
        {"_id": ObjectId(data.user_id)},
        {"$set": {
            "certificate_earned": True,
            "certificate_id": data.certificate_id,
            "certificate_date": data.issue_date,
            "certificate_saved_at": datetime.utcnow().isoformat()
        }}
    )
    return {
        "message": "Certificate saved to profile!",
        "certificate_id": data.certificate_id,
        "issue_date": data.issue_date
    }


# ✅ GET CERTIFICATE STATUS
@router.get("/certificate/{user_id}")
def get_certificate(user_id: str):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "certificate_earned": user.get("certificate_earned", False),
        "certificate_id": user.get("certificate_id", None),
        "certificate_date": user.get("certificate_date", None)
    }
