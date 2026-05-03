from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import get_db
from models.api_key import APIKey
from utils.api_key import generate_api_key

router = APIRouter(prefix="/keys")

@router.post("/generate")
def generate_key(user_id: int, api_id: int, db: Session = Depends(get_db)):
    key = generate_api_key()

    new_key = APIKey(
        key=key,
        user_id=user_id,
        api_id=api_id
    )
    db.add(new_key)
    db.commit()
    return {"api_key": key}

@router.post("/revoke")
def revoke_key(key: str, db: Session = Depends(get_db)):
    api_key = db.query(APIKey).filter(APIKey.key == key).first()
    if not api_key:
        return {"error": "Key not found"}
    api_key.status = "revoked"
    db.commit()
    return {"message": "API key revoked"}