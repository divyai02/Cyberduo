from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..database import users_collection
from .. import auth
from datetime import datetime
from bson import ObjectId

router = APIRouter(prefix="/auth", tags=["auth"])

class SignupRequest(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class AvatarRequest(BaseModel):
    user_id: str
    avatar: str

class ModeRequest(BaseModel):
    user_id: str
    mode: str


# ✅ SIGNUP
@router.post("/signup")
def signup(data: SignupRequest):
    if not data.password:
        raise HTTPException(status_code=400, detail="Password cannot be empty")
    
    if users_collection.find_one({"email": data.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    if users_collection.find_one({"username": data.username}):
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed_pw = auth.hash_password(data.password)
    new_user = {
        "username": data.username,
        "email": data.email,
        "hashed_password": hashed_pw,
        "avatar": None,
        "mode": None,
        "created_at": datetime.utcnow()
    }
    result = users_collection.insert_one(new_user)
    return {
        "message": "Account created successfully!",
        "user_id": str(result.inserted_id)
    }


# ✅ LOGIN
@router.post("/login")
def login(data: LoginRequest):
    if not data.password:
        raise HTTPException(status_code=400, detail="Password cannot be empty")
    
    user = users_collection.find_one({"email": data.email})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    if not auth.verify_password(data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = auth.create_access_token({
        "sub": str(user["_id"]),
        "username": user["username"]
    })
    return {
        "access_token": token,
        "token_type": "bearer",
        "username": user["username"],
        "user_id": str(user["_id"]),
        "avatar": user.get("avatar"),
        "mode": user.get("mode")
    }


# ✅ SAVE AVATAR
@router.post("/save-avatar")
def save_avatar(data: AvatarRequest):
    result = users_collection.update_one(
        {"_id": ObjectId(data.user_id)},
        {"$set": {"avatar": data.avatar}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Avatar saved!", "avatar": data.avatar}


# ✅ SAVE MODE
@router.post("/save-mode")
def save_mode(data: ModeRequest):
    result = users_collection.update_one(
        {"_id": ObjectId(data.user_id)},
        {"$set": {"mode": data.mode}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Mode saved!", "mode": data.mode}