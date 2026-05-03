from sqlalchemy import Column, Integer, String, ForeignKey
from config.database import Base

class API(Base):
    __tablename__ = "apis"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    base_url = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))