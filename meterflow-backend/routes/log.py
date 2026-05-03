from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import get_db
from models.log import Log

router = APIRouter(prefix="/logs", tags=["Logs"])

#Get all logs
@router.get("/")
def get_logs(db: Session = Depends(get_db)):
    logs = db.query(Log).all()
    return logs

#Get logs by API key
@router.get("/by-key")
def get_logs_by_key(api_key: str, db: Session = Depends(get_db)):
    logs = db.query(Log).filter(Log.api_key == api_key).all()
    return logs

#Get latest logs (limit)
@router.get("/latest")
def get_latest_logs(limit: int = 5, db: Session = Depends(get_db)):
    logs = db.query(Log).order_by(Log.id.desc()).limit(limit).all()
    return logs

@router.get("/{user_id}")
def get_logs(user_id: int, db: Session = Depends(get_db)):
    logs = db.query(Log).filter(Log.user_id == user_id).all()

    return logs