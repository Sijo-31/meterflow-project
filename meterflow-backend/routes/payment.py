from sqlalchemy.orm import Session
from fastapi import Depends
from config.database import get_db
from models.api_key import APIKey
from fastapi import APIRouter
from services.payment import create_order

router = APIRouter(prefix="/payment")

@router.post("/create")
def create_payment(amount: int):
    order = create_order(amount)
    return order

@router.post("/upgrade")
def upgrade_plan(user_id: int, db: Session = Depends(get_db)):
    keys = db.query(APIKey).filter(APIKey.user_id == user_id).all()

    for key in keys:
        key.plan = "pro"
    db.commit()
    return {"message": "User upgraded to PRO"}