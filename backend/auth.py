import os
import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session
from .database import get_db
from .email_service import send_email
from .models import User
from .schemas import (LoginRequest, MessageResponse, PasswordResetConfirm, PasswordResetRequest, RegisterRequest, TokenRequest, TokenResponse, UserResponse)
from .security import ACCESS_TOKEN_MINUTES, create_token, hash_password, read_token, verify_password

router = APIRouter(prefix="/api/auth", tags=["authentication"])
bearer = HTTPBearer(auto_error=False)
APP_URL = os.getenv("APP_URL", "http://localhost:5173").rstrip("/")

@router.post("/register", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    email = str(payload.email).lower()
    if db.scalar(select(User).where(User.email == email)):
        raise HTTPException(status_code=409, detail="An account with this email already exists.")
    user = User(full_name=payload.full_name.strip(), email=email, password_hash=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_token(str(user.id), "email_verification", 24 * 60)
    link = f"{APP_URL}/?verify={token}"
    sent = send_email(email, "Verify your Learning Forex Academy account", f"Hello {user.full_name},\n\nVerify your email using this link (valid for 24 hours):\n{link}\n")
    if not sent and os.getenv("ENVIRONMENT", "development") == "development":
        print(f"Development verification link for {email}: {link}")
    return {"message": "Account created. Please check your email for the verification link."}

@router.post("/verify-email", response_model=MessageResponse)
def verify_email(payload: TokenRequest, db: Session = Depends(get_db)):
    try:
        user_id = int(read_token(payload.token, "email_verification"))
    except (jwt.InvalidTokenError, ValueError):
        raise HTTPException(status_code=400, detail="This verification link is invalid or has expired.")
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=400, detail="This verification link is invalid or has expired.")
    user.is_verified = True
    db.commit()
    return {"message": "Email verified. You can now sign in."}

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == str(payload.email).lower()))
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Email or password is incorrect.")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="This account has been disabled. Contact support.")
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Please verify your email before signing in.")
    token = create_token(str(user.id), "access", ACCESS_TOKEN_MINUTES)
    return {"access_token": token, "token_type": "bearer"}

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer), db: Session = Depends(get_db)) -> User:
    if not credentials:
        raise HTTPException(status_code=401, detail="Sign in to continue.")
    try:
        user_id = int(read_token(credentials.credentials, "access"))
    except (jwt.InvalidTokenError, ValueError):
        raise HTTPException(status_code=401, detail="Your session has expired. Please sign in again.")
    user = db.get(User, user_id)
    if not user or not user.is_active or not user.is_verified:
        raise HTTPException(status_code=401, detail="This account is not available.")
    return user

@router.get("/me", response_model=UserResponse)
def me(user: User = Depends(get_current_user)):
    return user

@router.post("/password-reset/request", response_model=MessageResponse)
def request_password_reset(payload: PasswordResetRequest, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == str(payload.email).lower()))
    if user and user.is_active:
        token = create_token(str(user.id), "password_reset", 30)
        link = f"{APP_URL}/?reset={token}"
        send_email(user.email, "Reset your Learning Forex Academy password", f"Hello {user.full_name},\n\nReset your password using this link (valid for 30 minutes):\n{link}\n")
        if not os.getenv("SMTP_HOST") and os.getenv("ENVIRONMENT", "development") == "development":
            print(f"Development password reset link for {user.email}: {link}")
    return {"message": "If an account exists for that email, password reset instructions have been sent."}

@router.post("/password-reset/confirm", response_model=MessageResponse)
def confirm_password_reset(payload: PasswordResetConfirm, db: Session = Depends(get_db)):
    try:
        user_id = int(read_token(payload.token, "password_reset"))
    except (jwt.InvalidTokenError, ValueError):
        raise HTTPException(status_code=400, detail="This reset link is invalid or has expired.")
    user = db.get(User, user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=400, detail="This reset link is invalid or has expired.")
    user.password_hash = hash_password(payload.new_password)
    db.commit()
    return {"message": "Password updated. You can now sign in."}
