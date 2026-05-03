from sqlalchemy import Column, Integer, String, DateTime
from config.database import Base
from datetime import datetime

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    api_key = Column(String)
    user_id = Column(Integer)
    endpoint = Column(String)
    status_code = Column(Integer)
    latency = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)