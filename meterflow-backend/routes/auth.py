from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.user import User
from config.database import get_db
from utils.hash import hash_password, verify_password
from utils.jwt import create_access_token

router = APIRouter(prefix="/auth")

@router.post("/signup")
def signup(email: str, password: str, role: str, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    new_user = User(
        email=email,
        password=hash_password(password),
        role=role
    )
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({
        "user_id": user.id,
        "role": user.role
    })
    return {"access_token": token}