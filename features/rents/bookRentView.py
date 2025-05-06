import tkinter as tk
from tkinter import ttk
import tksheet
from tkinter import Variable, messagebox
from sqlalchemy.orm import sessionmaker
from features.books.models.books import Book
from sqlalchemy import create_engine, Column, Integer, String, or_
from features.readers.models.reader import ReaderDB
from tkcalendar import *
from datetime import datetime
from enum import Enum

from features.rents.models.rent import RentDB

engine = create_engine('sqlite:///library.db')

class BookStatus(Enum):
    TAKEN = 'TAKEN'
    RETURNED = 'RETURNED'
    EXPIRED = 'EXPIRED'

class RentPage(tk.Frame):
    def __init__(self, router):
        tk.Frame.__init__(self, router)
        self.takenDate = None
        self.expired__Date = None

        search_frame = tk.Frame(self)
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        search_btn = tk.Button(search_frame, text="Пошук", command = self.search_rents)
        search_btn.pack(side=tk.LEFT, padx=5)
        
        search_btn = tk.Button(search_frame, text="Скинути", command = self.resetsearch)
        search_btn.pack(side=tk.LEFT, padx=5)

        self.sheet = tksheet.Sheet(self, height=600, width=1200)
        self.sheet.pack(fill=tk.BOTH, expand=True)
        self.sheet.headers(["ID", "Назва", "ПІБ", "Коли взято", "Коли повернути", "Статус"])

        Session = sessionmaker(bind=engine)
        session = Session()

        rents = session.query(RentDB).join(Book).join(ReaderDB).all()
        
        data = [
            [rent.id, rent.book.title, rent.reader.fullname, rent.takenDate, rent.expiredDate, self.localizestatus(rent.rentStatus)]
            for rent in rents
        ]
        session.close()
        self.set_column_widths()
    
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
        
        self.sheet.set_sheet_data(data)
        self.set_column_widths()
        
        
        btn_frame = tk.Frame(self)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        add_btn = tk.Button(btn_frame, text="Додати ренту", command=self.rent_window_show)
        add_btn.pack(side=tk.LEFT, padx=5)
        
        edit_btn = tk.Button(btn_frame, text="Редагувати", command = self.show_edit_rent)
        edit_btn.pack(side=tk.LEFT, padx=5)

        delete_btn = tk.Button(btn_frame, text="Книгу повернуто", command = self.changestatus)
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        back_btn = tk.Button(btn_frame, text="Повернутися", command=lambda: router.switch_frame("LibrarianMenu"))
        back_btn.pack(side=tk.RIGHT)

    def resetsearch(self):
        self.search_entry.delete(0, 'end')
        self.refresh_table()




    def changestatus(self):
        selected_rows = self.sheet.get_selected_rows() 

        row_idx = next(iter(selected_rows)) 
        
        row_data = self.sheet.get_row_data(row_idx)  
        Session = sessionmaker(bind=engine)
        session = Session() 
        
        rent_id = row_data[0] 
        changing = session.query(RentDB).filter_by(id = rent_id).first()
        changing.rentStatus = BookStatus.RETURNED.value
        session.commit()
        session.close()
        self.refresh_table()

    def localizestatus(self, rentStatus):
        match rentStatus:
            case BookStatus.RETURNED.value:
                return 'Повернено'
            case BookStatus.EXPIRED.value:
                return 'Протерміновано'
            case BookStatus.TAKEN.value:
                return 'Взято'



    def search_rents(self):
        search_term = self.search_entry.get()
        Session = sessionmaker(bind=engine)
        session = Session()
        rents = session.query(RentDB).join(Book).join(ReaderDB).filter(or_(
        Book.title.contains(search_term),
        ReaderDB.fullname.contains(search_term))).all()

        searchdata = [
            [rent.id, rent.book.title, rent.reader.fullname, rent.takenDate, rent.expiredDate, self.localizestatus(rent.rentStatus)]
            for rent in rents
        ]
        session.close()
        self.sheet.set_sheet_data(searchdata)
        self.set_column_widths()   
        




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

        self.books_dict = {book.title: book.id for book in books}
        book_titles = list(self.books_dict.keys())

        rentWindow = tk.Toplevel()
        rentWindow.geometry("500x350")


        

        def summon_calendar_when():
            calwindow = tk.Toplevel(rentWindow)
            calwindow.geometry("400x400")
            calwindow.title('Коли взято')
            def get_calendar_data_when():
                self.takenDate = cal.get_date()
                datawhenlabel = tk.Label(rentWindow, text = self.takenDate)
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
                self.expired__Date = cal.get_date()
                datatilllabel = tk.Label(rentWindow, text= self.expired__Date)
                datatilllabel.grid(row=3, column=2, sticky="e", padx=5, pady=5)
                calwindow.destroy()
            cal = Calendar(calwindow)
            cal.pack()
            getdata = tk.Button(calwindow, text = "Обрати", command = lambda: get_calendar_data_till())
            getdata.pack()



        Session = sessionmaker(bind=engine)
        session = Session()

        fullnames = session.query(ReaderDB).all()
        session.close()
        self.readers_dict = {reader.fullname: reader.id for reader in fullnames}
        reader_titles = list(self.readers_dict.keys())
        
        rentWindow.book_choice_var = tk.StringVar()
        rentWindow.reader_choice_var = tk.StringVar()
        rentWindow.bookchoice = ttk.Combobox(rentWindow, textvariable=rentWindow.book_choice_var,values=book_titles, state="readonly")
        rentWindow.pibentry = ttk.Combobox(rentWindow, textvariable=rentWindow.reader_choice_var, values=reader_titles, state="readonly")
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

        tk.Button(rentWindow, text="Орендувати", command = lambda: self.save_rent(rentWindow)).grid(row=6, column=1, sticky="e", pady=10)
        
        tk.Button(rentWindow, text="Відмінити", command=rentWindow.destroy).grid(row=6, column=2, sticky="w", pady=10, padx=5)





    def refresh_table(self):
        Session = sessionmaker(bind=engine)
        session = Session()

        rents = session.query(RentDB).join(Book).join(ReaderDB).all()
        data = [
            [rent.id, rent.book.title, rent.reader.fullname, rent.takenDate, rent.expiredDate, self.localizestatus(rent.rentStatus)]
            for rent in rents
        ]

        session.close()
    
        self.sheet.set_sheet_data(data)
        self.set_column_widths()





    def save_rent(self, window):

        try:
            taken_date = datetime.strptime(self.takenDate, f'%m/%d/%y').date()
            expired_date = datetime.strptime(self.expired__Date, f'%m/%d/%y').date()
            
            book_title = window.book_choice_var.get()
            book_id = self.books_dict[book_title]  
            
            reader_name = window.reader_choice_var.get()
            reader_id = self.readers_dict[reader_name]  

            Session = sessionmaker(bind=engine)
            session = Session()
            
            new_rent = RentDB(
                taken_date,
                expired_date,
                BookStatus.TAKEN.value,
                book_id,  
                reader_id  
            )
            
            session.add(new_rent)
            session.commit()
            
            self.refresh_table()
            window.destroy()
            
        except ValueError as e:
            messagebox.showerror("Помилка", f"Невірний формат даних: {e}\nБудь ласка, перевірте числові поля (рік, кількість).")
        except Exception as e:
            messagebox.showerror("Помилка", f"{e}")
        finally:
            if 'session' in locals():
                session.close()





    def update_edit_data(self, rent_id, window):
        expired = datetime.strptime(self.expired__Date, '%m/%d/%y').date()
        Session = sessionmaker(bind=engine)
        session = Session()
        editedrent = session.query(RentDB).filter_by(id = rent_id).first()
        editedrent.expiredDate = expired
        session.commit()
        session.close()
        self.set_column_widths()
        self.refresh_table()
        window.destroy()





    def show_edit_rent(self):
        selected_rows = self.sheet.get_selected_rows() 

        row_idx = next(iter(selected_rows)) 
        
        row_data = self.sheet.get_row_data(row_idx)  
        Session = sessionmaker(bind=engine)
        session = Session() 
        
        rent_id = row_data[0] 
        editting = session.query(RentDB).filter_by(id = rent_id).first()
        session.close()
        if not editting:
            messagebox.showerror("Помилка", f"Не вдалося знайти ренту")
            return
        def show_edit_calendar():
            calwindow = tk.Toplevel(editwindow)
            calwindow.geometry("400x400")
            calwindow.title('Коли повернути')
            def get_calendar_data_till():
                self.expired__Date = cal.get_date()
                datatilllabel = tk.Label(editwindow, text= self.expired__Date)
                datatilllabel.grid(row=0, column=2, sticky="e", padx=5, pady=5)
                calwindow.destroy()
            cal = Calendar(calwindow)
            cal.pack()
            getdata = tk.Button(calwindow, text = "Обрати", command = lambda: get_calendar_data_till())
            getdata.pack()
        editwindow = tk.Toplevel()
        editwindow.title("Редагування ренти")
        editwindow.geometry("500x350")
        editwindow.expiredlabel = tk.Label(editwindow, text="Коли повернути").grid(row=0,column=0,sticky="e", padx=5, pady=5)
        editwindow.expiredentry = tk.Button(editwindow, text="Вибрати дату" ,command = show_edit_calendar)
        editwindow.expiredentry.grid(row=0, column=1, sticky="e", padx=5, pady=5)
        
        tk.Button(editwindow, text="Зберегти", command=lambda: self.update_edit_data(rent_id, editwindow)).grid(row=1, column=2, sticky="e", pady=10)
        
        tk.Button(editwindow,  text="Відмінити", command=editwindow.destroy).grid(row=2, column=2, sticky="e", padx=5, pady=5)
    

