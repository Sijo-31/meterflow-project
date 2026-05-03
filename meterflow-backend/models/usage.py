# models/usage.py
from sqlalchemy import Column, Integer
from config.database import Base

class Usage(Base):
    __tablename__ = "usage"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    request_count = Column(Integer, default=0)