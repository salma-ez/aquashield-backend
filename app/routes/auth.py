from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
from jose import jwt
from app.config import settings
from app.models.user import LoginRequest, TokenResponse

router = APIRouter()

FAKE_USERS = {
    "admin": {"password": "aquashield123", "role": "company"},
    "farmer1": {"password": "farmer123", "role": "farmer"},
    "user1": {"password": "user123", "role": "home"},
}

def create_token(user_id: str, role: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(
        {"sub": user_id, "role": role, "exp": expire},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest):
    user = FAKE_USERS.get(data.username)
    if not user or user["password"] != data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token(data.username, user["role"])
    return TokenResponse(access_token=token)
