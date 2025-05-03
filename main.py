from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, validates
from features.books.models.books import Base, Book
from features.users.user import UsersBase
from routes import RouterApp


engine = create_engine('sqlite:///library.db')
Base.metadata.create_all(engine)
UsersBase.metadata.create_all(engine)

if __name__ == "__main__":
    app = RouterApp()
    app.mainloop()