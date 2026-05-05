from pydantic import BaseModel
from typing import Literal

class TokenData(BaseModel):
    user_id: str
    role: Literal["home", "farmer", "company"]

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
