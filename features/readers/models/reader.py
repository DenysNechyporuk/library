from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float
from sqlalchemy.orm import declarative_base, sessionmaker, validates, relationship
from typing import Optional
from database import Base

class ReaderDB(Base):
    __tablename__ = 'readers'
    
    id = Column(Integer, primary_key=True)
    pib = Column(String(100), nullable=False)
    phonenumber = Column(String(50), nullable=False)
    liveaddress = Column(String(50), nullable=False)

    rents = relationship("RentDB", back_populates = "reader")
    def __init__(self, pib: str, phonenumber: str, liveaddress: str, id: Optional[int] = None):
        super().__init__()
        self.pib = pib
        self.phonenumber = phonenumber
        self.liveaddress = liveaddress
        if id is not None:
            self.id = id

    @validates('pib')
    def validate_title(self, key, pib):
        if not isinstance(pib, str) or not pib.strip():
            raise ValueError("ПІБ має бути не порожнім рядком")
        return pib.strip()
    
    @validates('phonenumber')
    def validate_title(self, key, phonenumber):
        if not isinstance(phonenumber, str) or not phonenumber.strip():
            raise ValueError("Номер телефону має бути не порожнім рядком")
        return phonenumber.strip()
    
    @validates('liveaddress')
    def validate_title(self, key, liveaddress):
        if not isinstance(liveaddress, str) or not liveaddress.strip():
            raise ValueError("Адреса має бути не порожнім рядком")
        return liveaddress.strip()