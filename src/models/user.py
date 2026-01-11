from ..database import Base
from sqlalchemy import Column, DateTime, Integer, String
from datetime import datetime

class users(Base):
    __tablename__= "users"
    id= Column(Integer,primary_key=True)
    username= Column(String, nullable=False)
    passwordhash = Column(String, nullable=False)
    created_at= Column(DateTime, default= datetime.now )