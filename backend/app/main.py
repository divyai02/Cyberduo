from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import auth_routes, user_routes, game_routes
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="CyberDuo API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(game_routes.router)

@app.get("/")
def root():
    return {"message": "CyberDuo backend is running!"}