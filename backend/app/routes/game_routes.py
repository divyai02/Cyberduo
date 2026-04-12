from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..database import users_collection, db
from datetime import datetime, date
from bson import ObjectId

router = APIRouter(prefix="/game", tags=["game"])

# ✅ GET QUESTIONS FROM DB
@router.get("/questions/{game_key}/{level}")
def get_questions(game_key: str, level: str):
    # Sort by local_id ascending (1, 2, 3...) so our high-engagement Q1-Q5 show up first
    questions = list(db["questions"].find({"game_key": game_key, "level_name": level}).sort("local_id", 1))
    for q in questions:
        q["_id"] = str(q["_id"])
        if "local_id" in q:
            q["id"] = q.pop("local_id")
    return questions

# ✅ SAVE GAME RESULT WHEN USER FINISHES ALL 5 QUESTIONS
class GameResult(BaseModel):
    user_id: str
    game_key: str
    level: str
    xp_earned: int
    score: int
    is_single_question: bool = False
    question_index: int = -1 # Added to track specific question for anti-grinding

@router.post("/save-result")
def save_game_result(data: GameResult):
    user = users_collection.find_one({"_id": ObjectId(data.user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # ✅ ANTI-GRINDING LOGIC: Check if XP was already awarded for this question
    # We use a map: { "game_key_level": [list of awarded question indices] }
    awarded_map = user.get("xp_awarded_questions", {})
    mission_key = f"{data.game_key}_{data.level}"
    awarded_indices = awarded_map.get(mission_key, [])

    should_reward_xp = True
    if data.is_single_question and data.question_index != -1:
        if data.question_index in awarded_indices:
            should_reward_xp = False
            print(f"XP already awarded for {mission_key} question {data.question_index}. Skipping increment.")
        else:
            awarded_indices.append(data.question_index)
            awarded_map[mission_key] = awarded_indices
    elif not data.is_single_question:
        # If it's a full game completion, we mark the whole level as awarded if not already
        # However, current frontend is per-question.
        pass

    # ✅ ATOMIC XP increment (only if not already awarded)
    if should_reward_xp and data.xp_earned > 0:
        xp_result = users_collection.find_one_and_update(
            {"_id": ObjectId(data.user_id)},
            {"$inc": {"xp": data.xp_earned}},
            return_document=True
        )
        new_xp = xp_result.get("xp", 0)
    else:
        new_xp = user.get("xp", 0)

    # Compute values that depend on new_xp
    # Only increment games_played if it's NOT a single question or if it's the first time
    new_games_played = user.get("games_played", 0) + (1 if not data.is_single_question else 0)

    # Unlock next games based on updated XP
    unlocked = user.get("games_unlocked", ["phishing"])
    if new_xp >= 100 and "password" not in unlocked:
        unlocked.append("password")
    if new_xp >= 250 and "malware" not in unlocked:
        unlocked.append("malware")
    if new_xp >= 500 and "firewall" not in unlocked:
        unlocked.append("firewall")
    if new_xp >= 800 and "scams" not in unlocked:
        unlocked.append("scams")

    # Award badges based on new_xp
    badges = user.get("badges", [])
    if new_games_played >= 1 and "First Mission" not in badges:
        badges.append("First Mission")
    if data.score >= 100 and "Perfect Score" not in badges:
        badges.append("Perfect Score")
    if new_xp >= 100 and "XP Hunter" not in badges:
        badges.append("XP Hunter")
    if new_xp >= 500 and "Cyber Warrior" not in badges:
        badges.append("Cyber Warrior")

    # Save game history entry
    game_history = user.get("game_history", [])
    game_history.append({
        "game_key": data.game_key,
        "level": data.level,
        "xp_earned": data.xp_earned if should_reward_xp else 0,
        "score": data.score,
        "played_at": datetime.utcnow().isoformat(),
        "is_reattempt": not should_reward_xp
    })

    # Daily question counter
    today = date.today().isoformat()
    last_login = user.get("last_login_date", "")
    daily_questions_done = user.get("daily_questions_done", 0)
    if last_login != today:
        daily_questions_done = 0
    
    # We still count daily questions done even if reattempted (for activity), 
    # OR we can restrict it too. Let's keep it for activity.
    if data.is_single_question:
        daily_questions_done += 1
    else:
        daily_questions_done += 25

    # ✅ Update all non-XP fields
    users_collection.update_one(
        {"_id": ObjectId(data.user_id)},
        {"$set": {
            "games_played": new_games_played,
            "games_unlocked": unlocked,
            "badges": badges,
            "game_history": game_history,
            "daily_questions_done": daily_questions_done,
            "last_played": datetime.utcnow(),
            "last_login_date": today,
            "xp_awarded_questions": awarded_map
        }}
    )

    return {
        "message": "Game result saved!",
        "new_xp": new_xp,
        "badges": badges,
        "games_unlocked": unlocked,
        "total_games_played": new_games_played,
        "daily_goal_done": daily_questions_done
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