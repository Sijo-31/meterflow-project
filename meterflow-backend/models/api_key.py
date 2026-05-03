from sqlalchemy import Column, Integer, String, ForeignKey
from config.database import Base

class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    api_id = Column(Integer, ForeignKey("apis.id"))
    status = Column(String, default="active")

    plan = Column(String, default="free")  #free/pro subscription plan