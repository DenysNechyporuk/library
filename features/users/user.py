from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float
from sqlalchemy.orm import declarative_base, sessionmaker, validates
from typing import Optional
from database import Base

class UserDB(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    login = Column(String(100), nullable=False)
    password = Column(String(50), nullable=False)
    role = Column(String(30), nullable=False)

    def __init__(self, login: str, password: str, role: str, id: Optional[int] = None):
        super().__init__()
        self.login = login
        self.password = password
        self.role = role
        if id is not None:
           self.id = id
    
