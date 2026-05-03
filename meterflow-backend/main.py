from fastapi import FastAPI
from config.database import engine, Base
from routes.auth import router as auth_router
from routes.api_key import router as api_key_router
from routes.api import router as api_router
from routes.gateway import router as gateway_router
from models import api, api_key, log 
from routes.log import router as log_router
from routes.usage import router as usage_router
from routes.billing import router as billing_router
from routes.payment import router as payment_router
from routes.analytics import router as analytics_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_key_router)
app.include_router(api_router)
app.include_router(gateway_router)
app.include_router(log_router)
app.include_router(usage_router)
app.include_router(billing_router)
app.include_router(payment_router)
app.include_router(analytics_router)
# Create DB tables
Base.metadata.create_all(bind=engine)

# Register routes
app.include_router(auth_router)

@app.get("/")
def home():
    return {"message": "MeterFlow Backend Running 🚀"}