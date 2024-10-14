from sqlalchemy import Column, String, Integer, Boolean, TIMESTAMP
from db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    isAdmin = Column(Boolean, default=False)
    registered_at= Column (TIMESTAMP)