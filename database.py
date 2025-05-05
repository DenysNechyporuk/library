from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///library.db')
Session = sessionmaker(bind=engine)

def init_db():
    # Імпорт моделей ПЕРЕД створенням таблиць
    from features.users.user import UserDB
    from features.books.models.books import Book
    from features.readers.models.reader import ReaderDB
    from features.rents.models.rent import RentDB
    
    Base.metadata.create_all(engine)