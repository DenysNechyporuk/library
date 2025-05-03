from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float
from sqlalchemy.orm import declarative_base, sessionmaker, validates
from datetime import datetime
from typing import Optional

Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    author = Column(String(50), nullable=False)
    genre = Column(String(30))
    year = Column(Integer)
    count = Column(Integer)
    
    def __init__(self, title: str, author: str, genre: str, year: int, quantity: int, id: Optional[int] = None):
        super().__init__()
        self.title = title
        self.author = author
        self.genre = genre
        self.year = year
        self.count = int(quantity)
        if id is not None:
            self.id = id
                
    
    @validates('title')
    def validate_title(self, key, title):
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Назва книги має бути не порожнім рядком")
        return title.strip()
    
    @validates('author')
    def validate_author(self, key, author):
        if not isinstance(author, str) or not author.strip():
            raise ValueError("Ім'я автора має бути не порожнім рядком")
        return author.strip()
    
    @validates('genre')
    def validate_genre(self, key, genre):
        if genre is not None and (not isinstance(genre, str) or not genre.strip()):
            raise ValueError("Жанр має бути не порожнім рядком")
        return genre.strip() if genre else None
    
    @validates('year')
    def validate_year(self, key, year):
        current_year = datetime.now().year
        if not isinstance(year, int) or year < 0 or year > current_year + 1:
            raise ValueError(f"Рік має бути додатнім числом не більше {current_year + 1}")
        return year
    

    @validates('quantity')
    def validate_quantity(self, key, quantity):
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Кількість має бути додатнім числом")
        