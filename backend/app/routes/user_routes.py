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