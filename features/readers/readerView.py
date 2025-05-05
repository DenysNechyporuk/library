import tkinter as tk
import tksheet
from features.readers.models.reader import ReaderDB
from tkinter import messagebox
from sqlalchemy.orm import sessionmaker
from features.books.models.books import Book
from sqlalchemy import create_engine, Column, Integer, String, or_

engine = create_engine('sqlite:///library.db')

class ReaderPage(tk.Frame):
    def __init__(self, router):
        tk.Frame.__init__(self, router)
        
        search_frame = tk.Frame(self)
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        search_btn = tk.Button(search_frame, text="Пошук", command = self.search_readers)
        search_btn.pack(side=tk.LEFT, padx=5)
        
        search_btn = tk.Button(search_frame, text="Скинути", command = self.resetsearch)
        search_btn.pack(side=tk.LEFT, padx=5)

        self.sheet = tksheet.Sheet(self, height=600, width=1200)
        self.sheet.pack(fill=tk.BOTH, expand=True)
        self.sheet.headers(["ID", "ПІБ", "Номер телефону", "Адреса"])
        
        Session = sessionmaker(bind=engine)
        session = Session()

        reads = session.query(ReaderDB).all()
        session.close()
        data = [
            [reader.id, reader.fullname, reader.phonenumber, reader.liveaddress]
            for reader in reads
        ]
        self.sheet.set_sheet_data(data)
        
        btn_frame = tk.Frame(self)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        add_btn = tk.Button(btn_frame, text="Додати читача", command = self.show_reader_window)
        add_btn.pack(side=tk.LEFT, padx=5)
        
        edit_btn = tk.Button(btn_frame, text="Редагувати", command= self.show_edit_reader)
        edit_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = tk.Button(btn_frame, text="Видалити", command = self.delete_reader)
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        back_btn = tk.Button(btn_frame, text="Повернутися", command=lambda: router.switch_frame("LibrarianMenu"))
        back_btn.pack(side=tk.RIGHT)
        
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

    def set_column_widths(self):
            widths = {
                0: 50,   # ID
                1: 320,  # ПІБ
                2: 150,  # Номер телефону
                3: 250,  # Адреса
            }
            
            for col, width in widths.items():
                self.sheet.column_width(col, width=width)
        

    def resetsearch(self):
        self.search_entry.delete(0, 'end')
        self.set_column_widths()
        self.refresh_table()

    def refresh_table(self):
        Session = sessionmaker(bind=engine)
        session = Session()

        reads = session.query(ReaderDB).all()
        session.close()
        data = [
            [reader.id, reader.fullname, reader.phonenumber, reader.liveaddress]
            for reader in reads
        ]
        self.sheet.set_sheet_data(data)
        self.set_column_widths()


    def search_readers(self):
        search_term = self.search_entry.get()
        Session = sessionmaker(bind=engine)
        session = Session()
        reads = session.query(ReaderDB).filter(or_(
        ReaderDB.fullname.contains(search_term),
        ReaderDB.phonenumber.contains(search_term),
        ReaderDB.liveaddress.contains(search_term))).all()

        searchdata = [
            [reader.id, reader.fullname, reader.phonenumber, reader.liveaddress]
            for reader in reads]
        session.close()
        self.set_column_widths() 
        self.sheet.set_sheet_data(searchdata)


    def show_reader_window(self):
        addwindow = tk.Toplevel()
        addwindow.title("Додати нового читача")
        addwindow.geometry("500x350")
        addwindow.pibentry = tk.Entry(addwindow)
        addwindow.phoneentry = tk.Entry(addwindow)
        addwindow.addressentry = tk.Entry(addwindow)

        tk.Label(addwindow, text="ПІБ").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        addwindow.pibentry.grid(row=0, column=1, sticky="we", padx=5, pady=5)
        
        tk.Label(addwindow, text="Номер телефону").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        addwindow.phoneentry.grid(row=1, column=1, sticky="we", padx=5, pady=5)
        
        tk.Label(addwindow, text="Адреса").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        addwindow.addressentry.grid(row=2, column=1, sticky="we", padx=5, pady=5)
        
        
        tk.Button(addwindow,  text="Додати", command=lambda: self.save_reader(addwindow) ).grid(row=6, column=1, sticky="e", pady=10)
        
        tk.Button(addwindow, text="Відмінити", command=addwindow.destroy).grid(row=6, column=2, sticky="w", pady=10, padx=5)

    def save_reader(self, window):
        try:
            
            Session = sessionmaker(bind=engine)
            session = Session()
            new_reader = ReaderDB(
                window.pibentry.get(),
                window.phoneentry.get(),
                window.addressentry.get(),
            )
            session.add(new_reader)
            session.commit()
            
            self.refresh_table()
            self.set_column_widths()
            window.destroy()
            
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося додати читача: {e}")
        finally:
            if 'session' in locals():
                session.close()
        
    
    def update_edit_data(self, book_id, window):
        Session = sessionmaker(bind=engine)
        session = Session()
        editedbook = session.query(ReaderDB).filter_by(id = book_id).first()
        editedbook.fullname = window.pibentry.get()
        editedbook.phonenumber = window.phoneentry.get()
        editedbook.liveaddress = window.addressentry.get()
        session.commit()
        session.close()
        self.set_column_widths()
        self.refresh_table()
        window.destroy()

    def show_edit_reader(self):
        selected_rows = self.sheet.get_selected_rows() 

        row_idx = next(iter(selected_rows)) 
        
        row_data = self.sheet.get_row_data(row_idx)  
        Session = sessionmaker(bind=engine)
        session = Session() 
        
        reader_id = row_data[0] 
        editting = session.query(ReaderDB).filter_by(id = reader_id).first()
        session.close()
        if not editting:
            messagebox.showerror("Помилка", f"Не вдалося знайти читача")
            return
        
        editwindow = tk.Toplevel()
        editwindow.title("Редагування читача")
        editwindow.geometry("500x350")
        editwindow.pibentry = tk.Entry(editwindow)
        editwindow.phoneentry = tk.Entry(editwindow)
        editwindow.addressentry = tk.Entry(editwindow)

        editwindow.pibentry.insert(0, editting.fullname)
        editwindow.phoneentry.insert(0, editting.phonenumber)
        editwindow.addressentry.insert(0, editting.liveaddress)
    

        tk.Label(editwindow, text="ПІБ").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        editwindow.pibentry.grid(row=0, column=1, sticky="we", padx=5, pady=5)
        
        tk.Label(editwindow, text="Номер телефону").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        editwindow.phoneentry.grid(row=1, column=1, sticky="we", padx=5, pady=5)
        
        tk.Label(editwindow, text="Адреса").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        editwindow.addressentry.grid(row=2, column=1, sticky="we", padx=5, pady=5)
        
        tk.Button(editwindow, text="Зберегти", command=lambda: self.update_edit_data(reader_id, editwindow)).grid(row=6, column=1, sticky="e", pady=10)
        
        tk.Button(editwindow,  text="Відмінити", command=editwindow.destroy).grid(row=6, column=2, sticky="w", pady=10, padx=5)
    

        
    def delete_reader(self):
        selected_rows = self.sheet.get_selected_rows() 
        
        row_idx = next(iter(selected_rows)) 
        
        row_data = self.sheet.get_row_data(row_idx)  
        Session = sessionmaker(bind=engine)
        session = Session() 
        
        reader_id = row_data[0]  
        deletion = session.query(ReaderDB).filter_by(id = reader_id).first()
        if deletion:
            session.delete(deletion)
            session.commit()
        session.close()
        self.sheet.delete_row(row_idx)