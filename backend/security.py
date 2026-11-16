import os
from datetime import datetime, timedelta, timezone
import jwt
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()
JWT_SECRET = os.getenv("JWT_SECRET", "")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_MINUTES = int(os.getenv("ACCESS_TOKEN_MINUTES", "60"))

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return password_hash.verify(password, hashed)

def create_token(subject: str, purpose: str, minutes: int) -> str:
    if not JWT_SECRET:
        raise RuntimeError("JWT_SECRET must be configured before starting the API")
    now = datetime.now(timezone.utc)
    payload = {"sub": subject, "purpose": purpose, "iat": now, "exp": now + timedelta(minutes=minutes)}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def read_token(token: str, purpose: str) -> str:
    payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    if payload.get("purpose") != purpose or not payload.get("sub"):
        raise jwt.InvalidTokenError("Invalid token purpose")
    return str(payload["sub"])
