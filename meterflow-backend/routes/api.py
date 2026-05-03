from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import get_db
from models.api import API

router = APIRouter(prefix="/apis")

@router.post("/create")
def create_api(name: str, base_url: str, user_id: int, db: Session = Depends(get_db)):
    new_api = API(
        name=name,
        base_url=base_url,
        user_id=user_id
    )
    db.add(new_api)
    db.commit()
    return {"message": "API created successfully"}