from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import get_db
from models.log import Log
from datetime import datetime, timedelta

router = APIRouter(prefix="/analytics")


@router.get("/{user_id}")
def get_analytics(user_id: int, db: Session = Depends(get_db)):

    logs = db.query(Log).filter(Log.user_id == user_id).all()

    if not logs:
        return {
            "total_requests": 0,
            "success": 0,
            "failures": 0,
            "error_rate": 0,
            "avg_latency": 0
        }

    total = len(logs)

    success = len([l for l in logs if l.status_code == 200])
    failures = total - success

    error_rate = (failures / total) * 100 if total > 0 else 0

    avg_latency = sum([l.latency for l in logs]) / total

    return {
        "total_requests": total,
        "success": success,
        "failures": failures,
        "error_rate": round(error_rate, 2),
        "avg_latency_ms": int(avg_latency)
    }

@router.get("/rpm/{user_id}")
def requests_per_minute(user_id: int, db: Session = Depends(get_db)):

    one_minute_ago = datetime.utcnow() - timedelta(minutes=1)

    count = db.query(Log).filter(
        Log.user_id == user_id,
        Log.timestamp >= one_minute_ago
    ).count()

    return {
        "requests_last_minute": count
    }