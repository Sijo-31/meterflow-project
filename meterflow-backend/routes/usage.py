from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import get_db
from models.log import Log
from sqlalchemy import func

router = APIRouter(prefix="/usage", tags=["Usage"])

@router.get("/user/{user_id}")
def get_usage(user_id: int, db: Session = Depends(get_db)):
    count = db.query(func.count(Log.id)).filter(Log.user_id == user_id).scalar()
    return {
        "user_id": user_id,
        "total_requests": count
    }
PRICE_PER_REQUEST = 0.01

@router.get("/billing/{user_id}")
def get_billing(user_id: int, db: Session = Depends(get_db)):
    count = db.query(func.count(Log.id)).filter(Log.user_id == user_id).scalar()
    total_cost = count * PRICE_PER_REQUEST
    return {
        "user_id": user_id,
        "total_requests": count,
        "price_per_request": PRICE_PER_REQUEST,
        "total_cost": total_cost
    }