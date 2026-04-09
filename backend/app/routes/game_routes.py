from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..database import users_collection
from datetime import datetime
from bson import ObjectId

router = APIRouter(prefix="/game", tags=["game"])

# ✅ SAVE GAME RESULT WHEN USER FINISHES ALL 5 QUESTIONS
class GameResult(BaseModel):
    user_id: str
    game_key: str
    level: str
    xp_earned: int
    score: int

@router.post("/save-result")
def save_game_result(data: GameResult):
    user = users_collection.find_one({"_id": ObjectId(data.user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update XP
    new_xp = user.get("xp", 0) + data.xp_earned
    new_games_played = user.get("games_played", 0) + 1

    # Unlock next games based on XP
    unlocked = user.get("games_unlocked", ["phishing"])
    if new_xp >= 100 and "password" not in unlocked:
        unlocked.append("password")
    if new_xp >= 250 and "malware" not in unlocked:
        unlocked.append("malware")
    if new_xp >= 500 and "firewall" not in unlocked:
        unlocked.append("firewall")
    if new_xp >= 800 and "scam" not in unlocked:
        unlocked.append("scam")

    # Award badges
    badges = user.get("badges", [])
    if new_games_played >= 1 and "First Mission" not in badges:
        badges.append("First Mission")
    if data.score >= 100 and "Perfect Score" not in badges:
        badges.append("Perfect Score")
    if new_xp >= 100 and "XP Hunter" not in badges:
        badges.append("XP Hunter")
    if new_xp >= 500 and "Cyber Warrior" not in badges:
        badges.append("Cyber Warrior")

    # Save game history
    game_history = user.get("game_history", [])
    game_history.append({
        "game_key": data.game_key,
        "level": data.level,
        "xp_earned": data.xp_earned,
        "score": data.score,
        "played_at": datetime.utcnow().isoformat()
    })

    # Update daily goal
    daily_goal_done = user.get("daily_goal_done", 0) + 1

    # Update user in MongoDB
    users_collection.update_one(
        {"_id": ObjectId(data.user_id)},
        {"$set": {
            "xp": new_xp,
            "games_played": new_games_played,
            "games_unlocked": unlocked,
            "badges": badges,
            "game_history": game_history,
            "daily_goal_done": daily_goal_done,
            "last_played": datetime.utcnow()
        }}
    )

    return {
        "message": "Game result saved!",
        "new_xp": new_xp,
        "badges": badges,
        "games_unlocked": unlocked,
        "total_games_played": new_games_played,
        "daily_goal_done": daily_goal_done
    }


# ✅ GET USER GAME HISTORY
@router.get("/history/{user_id}")
def get_game_history(user_id: str):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "game_history": user.get("game_history", []),
        "games_unlocked": user.get("games_unlocked", ["phishing"])
    }