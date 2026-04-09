from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..database import users_collection
from datetime import datetime, date
from bson import ObjectId

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
        "daily_goal_done": user.get("daily_goal_done", 0),
        "daily_goal_total": user.get("daily_goal_total", 3),
        "games_unlocked": user.get("games_unlocked", ["phishing"]),
    }


# ✅ UPDATE STREAK
class StreakUpdate(BaseModel):
    user_id: str

@router.post("/update-streak")
def update_streak(data: StreakUpdate):
    user = users_collection.find_one({"_id": ObjectId(data.user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    today = date.today().isoformat()
    last_login = user.get("last_login_date", "")
    streak = user.get("streak", 0)

    if last_login == today:
        return {"message": "Already updated today", "streak": streak}

    import datetime as dt
    yesterday = (dt.date.today() - dt.timedelta(days=1)).isoformat()
    if last_login == yesterday:
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