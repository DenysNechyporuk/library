from sqlite3 import IntegrityError
import tkinter as tk
import tksheet
from tkinter import messagebox
from sqlalchemy.orm import sessionmaker
from features.books.models.books import Book
from sqlalchemy import create_engine, Column, Integer, String, or_

engine = create_engine('sqlite:///library.db')

class BooksPage(tk.Frame):
    def __init__(self, router):
        tk.Frame.__init__(self, router)
        
        search_frame = tk.Frame(self)
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        search_btn = tk.Button(search_frame, text="Пошук", command=self.search_books)
        search_btn.pack(side=tk.LEFT, padx=5)
        
        search_btn = tk.Button(search_frame, text="Скинути", command=self.resetsearch)
        search_btn.pack(side=tk.LEFT, padx=5)

        self.sheet = tksheet.Sheet(self, height=600, width=1200)
        self.sheet.pack(fill=tk.BOTH, expand=True)
        self.sheet.headers(["ID", "Назва", "Автор", "Жанр", "Рік", "Кількість"])
        
        Session = sessionmaker(bind=engine)
        session = Session()

        books = session.query(Book).all()
        session.close()
        data = [
            [book.id, book.title, book.author, book.genre, book.year, book.count]
            for book in books
        ]
        self.sheet.set_sheet_data(data)
        self.set_column_widths()
        
        btn_frame = tk.Frame(self)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        add_btn = tk.Button(btn_frame, text="Додати книгу", command=self.show_book_window)
        add_btn.pack(side=tk.LEFT, padx=5)
        
        edit_btn = tk.Button(btn_frame, text="Редагувати", command=self.show_edit_book)
        edit_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = tk.Button(btn_frame, text="Видалити", command=self.delete_book)
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        back_btn = tk.Button(btn_frame, text="Повернутися", 
                           command=lambda: router.switch_frame("LibrarianMenu"))
        back_btn.pack(side=tk.RIGHT)
        
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

    def resetsearch(self):
        self.search_entry.delete(0, 'end')
        self.refresh_table()

    def refresh_table(self):
        Session = sessionmaker(bind=engine)
        session = Session()

        books = session.query(Book).all()
        session.close()
        data = [
            [book.id, book.title, book.author, book.genre, book.year, book.count]
            for book in books
        ]
        self.sheet.set_sheet_data(data)
        self.set_column_widths()

    def set_column_widths(self):
        widths = {
            0: 50,   # ID
            1: 420,  # Назва (широкий)
            2: 350,  # Автор (широкий)
            3: 150,  # Жанр
            4: 80,   # Рік
            5: 80,   # Кількість
        }
        
        for col, width in widths.items():
            self.sheet.column_width(col, width=width)

    def search_books(self):
        search_term = self.search_entry.get()
        Session = sessionmaker(bind=engine)
        session = Session()
        books = session.query(Book).filter(or_(
        Book.title.contains(search_term),
        Book.author.contains(search_term),
        Book.genre.contains(search_term))).all()

        searchdata = [
            [book.id, book.title, book.author, book.genre, book.year, book.count]
            for book in books
        ]
        session.close()
        self.sheet.set_sheet_data(searchdata)
        self.set_column_widths()   



    def show_book_window(self):
        addwindow = tk.Toplevel()
        addwindow.title("Додати нову книгу")
        addwindow.geometry("500x350")
        addwindow.nameentry = tk.Entry(addwindow)
        addwindow.authorentry = tk.Entry(addwindow)
        addwindow.genreentry = tk.Entry(addwindow)
        addwindow.yearentry = tk.Entry(addwindow)
        addwindow.quantityentry = tk.Entry(addwindow)
        tk.Label(addwindow, text="Назва").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        addwindow.nameentry.grid(row=0, column=1, sticky="we", padx=5, pady=5)
        
        tk.Label(addwindow, text="Автор").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        addwindow.authorentry.grid(row=1, column=1, sticky="we", padx=5, pady=5)
        
        tk.Label(addwindow, text="Жанр").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        addwindow.genreentry.grid(row=2, column=1, sticky="we", padx=5, pady=5)
        
        tk.Label(addwindow, text="Рік").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        addwindow.yearentry.grid(row=3, column=1, sticky="we", padx=5, pady=5)
        
        tk.Label(addwindow, text="Кількість").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        addwindow.quantityentry.grid(row=4, column=1, sticky="we", padx=5, pady=5)
        
        tk.Button(
            addwindow, 
            text="Додати", 
            command=lambda: self.save_book(addwindow)
        ).grid(row=6, column=1, sticky="e", pady=10)
        
        tk.Button(
            addwindow, 
            text="Відмінити", 
            command=addwindow.destroy
        ).grid(row=6, column=2, sticky="w", pady=10, padx=5)

    def save_book(self, window):
        try:
            
            Session = sessionmaker(bind=engine)
            session = Session()
            new_book = Book(
                window.nameentry.get(),
                window.authorentry.get(),
                window.genreentry.get(),
                int(window.yearentry.get()),
                int(window.quantityentry.get())
            )
            session.add(new_book)
            session.commit()
            
            self.refresh_table()
            window.destroy()
            
        except ValueError as e:
            messagebox.showerror("Помилка", f"Невірний формат даних: {e}\nБудь ласка, перевірте числові поля (рік, кількість).")

        except IntegrityError as e:
            if "UNIQUE constraint failed" in str(e.orig):
                messagebox.showerror("Помилка", "Запис з таким унікальним полем уже існує (наприклад, назва книги).")
            else:
                messagebox.showerror("Помилка бази даних", f"Виникла помилка цілісності: {e}")
        except Exception as e:
            if "UNIQUE constraint failed" in str(e.orig):
                messagebox.showerror("Помилка", "Запис з таким унікальним полем уже існує (наприклад, назва книги).")
            else:
                messagebox.showerror("Помилка", f"Не вдалося додати книгу: {e}")
        finally:
            if 'session' in locals():
                session.close()
        
    def update_edit_data(self, book_id, window):
        Session = sessionmaker(bind=engine)
        session = Session()
        editedbook = session.query(Book).filter_by(id = book_id).first()
        editedbook.title = window.nameentry.get()
        editedbook.author = window.authorentry.get()
        editedbook.genre = window.genreentry.get()
        editedbook.year = int(window.yearentry.get())
        editedbook.count = window.quantityentry.get()
        print(editedbook.count)
        print(window.quantityentry.get())
        session.commit()
        session.close()
        self.set_column_widths()
        self.refresh_table()
        window.destroy()

    def show_edit_book(self):
        selected_rows = self.sheet.get_selected_rows() 

        row_idx = next(iter(selected_rows)) 
        
        row_data = self.sheet.get_row_data(row_idx)  
        Session = sessionmaker(bind=engine)
        session = Session() 
        
        book_id = row_data[0] 
        editting = session.query(Book).filter_by(id = book_id).first()
        session.close()
        if not editting:
            messagebox.showerror("Помилка", f"Не вдалося знайти книгу")
            return
        
        editwindow = tk.Toplevel()
        editwindow.title("Редагування книги")
        editwindow.geometry("500x350")
        editwindow.nameentry = tk.Entry(editwindow)
        editwindow.authorentry = tk.Entry(editwindow)
        editwindow.genreentry = tk.Entry(editwindow)
        editwindow.yearentry = tk.Entry(editwindow)
        editwindow.quantityentry = tk.Entry(editwindow)

        editwindow.nameentry.insert(0, editting.title)
        editwindow.authorentry.insert(0, editting.author)
        editwindow.genreentry.insert(0, editting.genre)
        editwindow.yearentry.insert(0, editting.year)
        editwindow.quantityentry.insert(0, editting.count)
    

        tk.Label(editwindow, text="Назва").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        editwindow.nameentry.grid(row=0, column=1, sticky="we", padx=5, pady=5)
        
        tk.Label(editwindow, text="Автор").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        editwindow.authorentry.grid(row=1, column=1, sticky="we", padx=5, pady=5)
        
        tk.Label(editwindow, text="Жанр").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        editwindow.genreentry.grid(row=2, column=1, sticky="we", padx=5, pady=5)
        
        tk.Label(editwindow, text="Рік").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        editwindow.yearentry.grid(row=3, column=1, sticky="we", padx=5, pady=5)
        
        tk.Label(editwindow, text="Кількість").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        editwindow.quantityentry.grid(row=4, column=1, sticky="we", padx=5, pady=5)
        
        tk.Button(editwindow, text="Зберегти", command=lambda: self.update_edit_data(book_id, editwindow)).grid(row=6, column=1, sticky="e", pady=10)
        

        tk.Button(editwindow,  text="Відмінити", command=editwindow.destroy).grid(row=6, column=2, sticky="w", pady=10, padx=5)
    

        
    def delete_book(self):
        selected_rows = self.sheet.get_selected_rows() 
        
        row_idx = next(iter(selected_rows)) 
        
        row_data = self.sheet.get_row_data(row_idx)  
        Session = sessionmaker(bind=engine)
        session = Session() 
        
        book_id = row_data[0]  
        deletion = session.query(Book).filter_by(id = book_id).first()
        if deletion:
            session.delete(deletion)
            session.commit()
        session.close()
        self.sheet.delete_row(row_idx)