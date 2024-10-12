from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from models.user import User as UserModel
from db.database import get_db
from utils.security import hash_password, create_access_token, verify_password
from pydantic import BaseModel
from typing import Optional
from datetime import timedelta

router = APIRouter()

class User(BaseModel):
    username: str
    password: str
    email: str

class OTP(BaseModel):
    email: str
    otp: str

class ResetPassword(BaseModel):
    email: str
    new_password: str

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

@router.post("/signup")
async def signup(user: User, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    new_user = UserModel(
        username=user.username,
        email=user.email,
        hashed_password= hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User created successfully"}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == form_data.username).first()  # Changed form_data.email to form_data.username

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    # Create access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/otp")
async def otp_verification(otp: OTP):
    # Implement OTP verification logic here
    return {"msg": "OTP verified"}

@router.post("/reset-password")
async def reset_password(reset: ResetPassword, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == reset.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    user.hashed_password = hash_password(reset.new_password)
    db.commit()
    return {"msg": "Password reset successfully"}