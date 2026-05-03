from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import get_db
from models.log import Log
from models.usage import Usage

router = APIRouter(prefix="/billing")

#helper function
def calculate_cost(count: int):
    price_per_request = 0.01
    return count * price_per_request

#Get usage from logs
@router.get("/usage/{user_id}")
def get_usage(user_id: int, db: Session = Depends(get_db)):
    count = db.query(Log).filter(
        Log.user_id == user_id,
        Log.status_code == 200
    ).count()
    return {
        "user_id": user_id,
        "total_requests": count or 0
    }
#Billing endpoint
@router.get("/{user_id}")
def get_bill(user_id: int, db: Session = Depends(get_db)):
    usage = db.query(Usage).filter(Usage.user_id == user_id).first()
    if not usage:
        return {
            "usage": 0,
            "cost": 0
        }
    cost = calculate_cost(usage.request_count)
    return {
        "usage": usage.request_count,
        "cost": cost
    }