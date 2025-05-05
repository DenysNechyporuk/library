import tkinter as tk
from tkinter import ttk
import tksheet
from tkinter import Variable, messagebox
from sqlalchemy.orm import sessionmaker
from features.books.models.books import Book
from sqlalchemy import create_engine, Column, Integer, String, or_
from features.readers.models.reader import ReaderDB
from tkcalendar import *
from enum import Enum

engine = create_engine('sqlite:///library.db')

class BookStatus(Enum):
    TAKEN = ('TAKEN')
    RETURNED = ('RETURNED')
    EXPIRED = ('EXPIRED')

class RentPage(tk.Frame):
    def __init__(self, router):
        tk.Frame.__init__(self, router)
        
        search_frame = tk.Frame(self)
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        search_btn = tk.Button(search_frame, text="Пошук")
        search_btn.pack(side=tk.LEFT, padx=5)
        
        search_btn = tk.Button(search_frame, text="Скинути")
        search_btn.pack(side=tk.LEFT, padx=5)

        self.sheet = tksheet.Sheet(self, height=600, width=1200)
        self.sheet.pack(fill=tk.BOTH, expand=True)
        self.sheet.headers(["ID", "Назва", "ПІБ", "Коли взято", "Коли повернути", "Статус"])
    
        self.sheet.enable_bindings((
            "single_select",
            "row_select",
            "column_width_resize",
            "right_click_popup_menu", 
            "copy",
            "undo"
        ))
        
        self.sheet.disable_bindings((
            "drag_select",       
            "ctrl_select",      
            "shift_select",
            "select_all"  
        ))
        self.sheet.extra_bindings("select", lambda e: self.sheet.deselect("all") if len(self.sheet.get_selected_rows()) > 1 else None)
        
        self.sheet.set_sheet_data()
        self.set_column_widths()
        
        btn_frame = tk.Frame(self)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        add_btn = tk.Button(btn_frame, text="Додати ренту", command=self.rent_window_show)
        add_btn.pack(side=tk.LEFT, padx=5)
        
        edit_btn = tk.Button(btn_frame, text="Редагувати")
        edit_btn.pack(side=tk.LEFT, padx=5)
        
        back_btn = tk.Button(btn_frame, text="Повернутися", command=lambda: router.switch_frame("LibrarianMenu"))
        back_btn.pack(side=tk.RIGHT)

    
    def set_column_widths(self):
        widths = {
            0: 50,   # ID
            1: 400,  # Назва 
            2: 320,  # ПІБ 
            3: 120,  # Коли взято 
            4: 120,  # Коли повернути 
            5: 120,  # Статус
        }
        
        for col, width in widths.items():
            self.sheet.column_width(col, width=width)
    

    def rent_window_show(self):

        Session = sessionmaker(bind=engine)
        session = Session()

        books = session.query(Book).filter(Book.count > 0).all()
        session.close()

        rentWindow = tk.Toplevel()
        rentWindow.geometry("500x350")


        def summon_calendar_when():
            calwindow = tk.Toplevel(rentWindow)
            calwindow.geometry("400x400")
            calwindow.title('Коли взято')
            def get_calendar_data_when():
                caldata = cal.get_date()
                datawhenlabel = tk.Label(rentWindow, text= caldata)
                datawhenlabel.grid(row=2, column=2, sticky="e", padx=5, pady=5)
                calwindow.destroy()
            cal = Calendar(calwindow)
            cal.pack()
            getdata = tk.Button(calwindow, text = "Обрати дату", command = lambda: get_calendar_data_when())
            getdata.pack()

        def summon_calendar_till():
            calwindow = tk.Toplevel(rentWindow)
            calwindow.geometry("400x400")
            calwindow.title('Коли повернути')
            def get_calendar_data_till():
                caldata = cal.get_date()
                datatilllabel = tk.Label(rentWindow, text= caldata)
                datatilllabel.grid(row=3, column=2, sticky="e", padx=5, pady=5)
                calwindow.destroy()
            cal = Calendar(calwindow)
            cal.pack()
            getdata = tk.Button(calwindow, text = "Обрати", command = lambda: get_calendar_data_till())
            getdata.pack()

        booktitles = [
            book.title
            for book in books
        ]
        Session = sessionmaker(bind=engine)
        session = Session()

        pibs = session.query(ReaderDB).all()
        session.close()

        pibtitles = [
            reader.pib
            for reader in pibs
        ]
                
        rentWindow.bookchoice = ttk.Combobox(rentWindow, values = booktitles)
        rentWindow.pibentry = ttk.Combobox(rentWindow, values = pibtitles)
        rentWindow.whentaken = tk.Button(rentWindow, text="Вибрати дату", command=summon_calendar_when)
        rentWindow.tillwhen = tk.Button(rentWindow, text="Вибрати дату", command=summon_calendar_till)
        
        tk.Label(rentWindow, text="Книга").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        rentWindow.bookchoice.grid(row=0, column=1, sticky="we", padx=5, pady=5)
        
        tk.Label(rentWindow, text="ПІБ читача").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        rentWindow.pibentry.grid(row=1, column=1, sticky="we", padx=5, pady=5)
        
        tk.Label(rentWindow, text="Коли взято").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        rentWindow.whentaken.grid(row=2, column=1, sticky="we", padx=5, pady=5)
        
        tk.Label(rentWindow, text="Коли повернути").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        rentWindow.tillwhen.grid(row=3, column=1, sticky="we", padx=5, pady=5)

        tk.Button(rentWindow, text="Орендувати").grid(row=6, column=1, sticky="e", pady=10)
        
        tk.Button(rentWindow, text="Відмінити", command=rentWindow.destroy).grid(row=6, column=2, sticky="w", pady=10, padx=5)
