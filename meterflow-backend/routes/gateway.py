from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from config.database import get_db
from models.api_key import APIKey
from models.api import API
from models.log import Log
from models.usage import Usage
from services.rate_limiter import check_rate_limit
import requests
import time

router = APIRouter(prefix="/gateway")

@router.get("/{api_id}")
def gateway(api_id: int, x_api_key: str = Header(None), db: Session = Depends(get_db)):
    start_time = time.time()

    #Validate API key
    if not x_api_key:
        raise HTTPException(status_code=400, detail="API key missing")
    api_key = db.query(APIKey).filter(APIKey.key == x_api_key).first()
    if not api_key or api_key.status != "active":
        raise HTTPException(status_code=403, detail="Invalid API key")
  #Get API
    api = db.query(API).filter(API.id == api_id).first()
    if not api:
        raise HTTPException(status_code=404, detail="API not found")
    #Plan-based rate limit
    limit = 5 if api_key.plan == "free" else 50
    allowed, retry_after = check_rate_limit(
        f"user:{api_key.user_id}", limit=limit
    )
    if not allowed:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Try again in {retry_after} seconds"
        )
   #Usage tracking (FIXED commit flow)
    usage = db.query(Usage).filter(Usage.user_id == api_key.user_id).first()
    if not usage:
        usage = Usage(user_id=api_key.user_id, request_count=1)
        db.add(usage)
    else:
        usage.request_count += 1

    db.commit()
    db.refresh(usage)
    try:
        response = requests.get(api.base_url)
        latency = int((time.time() - start_time) * 1000)
        new_log = Log(
            api_key=x_api_key,
            user_id=api_key.user_id,
            endpoint=f"/gateway/{api_id}",
            status_code=response.status_code,
            latency=latency
        )
        db.add(new_log)
        db.commit()
        db.refresh(new_log)
        return response.json()
    except Exception as e:
        latency = int((time.time() - start_time) * 1000)
        error_log = Log(
            api_key=x_api_key,
            user_id=api_key.user_id,
            endpoint=f"/gateway/{api_id}",
            status_code=500,
            latency=latency
        )
        db.add(error_log)
        db.commit()
        db.refresh(error_log)
        return {"error": str(e)}