from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, validates, relationship
from typing import Optional

from database import Base


class RentDB(Base):
    __tablename__ = 'rents'
    
    id = Column(Integer, primary_key=True)
    bookId = Column(Integer, ForeignKey('books.id'))
    readerId = Column(Integer, ForeignKey('readers.id'))
    takenDate = Column(Date, nullable=False)
    expiredDate = Column(Date, nullable=False)
    rentStatus = Column(String(30), nullable=False)

    book = relationship("Book", back_populates = "rents")
    reader = relationship("ReaderDB", back_populates = "rents")
    def __init__(self, takenDate: Date, expiredDate: Date, rentStatus: str, id: Optional[int] = None):
        super().__init__()
        self.takenDate = takenDate
        self.expiredDate = expiredDate
        self.rentStatus = rentStatus
        if id is not None:
            self.id = id