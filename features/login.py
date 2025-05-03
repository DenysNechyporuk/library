import tkinter as tk
from tkinter import messagebox
from sqlalchemy.orm import sessionmaker
from features.books.models.books import Book
from features.users.user import UserDB
from sqlalchemy import create_engine, Column, Integer, String, or_, exists

engine = create_engine('sqlite:///library.db')

class LoginPage(tk.Frame):
    def __init__(self, router):      
        Session = sessionmaker(bind=engine)
        session = Session()

        exists_query = session.query(exists().where(UserDB.id != None)).scalar()
        if exists_query:
            session.close()
        else:
            adminuser = UserDB('admin', 'admin', 'admin')
            session.add(adminuser)
            session.commit()
            session.close()         
            
        tk.Frame.__init__(self, router)
        loginlabel = tk.Label(self, text="Логін")
        loginlabel.pack(pady=5)

        self.loginentry = tk.Entry(self, justify='center')
        self.loginentry.pack(pady=5)

        passwordlabel = tk.Label(self, text="Пароль")
        passwordlabel.pack(pady=5)

        self.passwordentry = tk.Entry(self, show="*", justify='center')
        self.passwordentry.pack(pady=5)

        tk.Button(self, text="Увійти", command= lambda: self.logincheck(router)).pack()

    def logincheck(self, router):
        Session = sessionmaker(bind=engine)
        session = Session() 
        dbuser = session.query(UserDB).filter(UserDB.login == self.loginentry.get()).first()
        session.close()
        if not dbuser:
            messagebox.showerror("Помилка", "Користувача не знайдено")    
            return
        if dbuser.password != self.passwordentry.get():
            messagebox.showerror("Помилка", "Неправильний пароль")
            return
        router.switch_frame("LibrarianMenu")
        
          