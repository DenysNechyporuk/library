import tkinter as tk

class GeneralMenu(tk.Frame):
    def __init__(self, router):
        tk.Frame.__init__(self, router)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)
        

        main_container = tk.Frame(self)
        main_container.grid(row=1, column=0, sticky="news", pady=170)
        

        tk.Button(main_container, text="Книги", width=20, height=5,
                command=lambda: router.switch_frame("BooksPage")).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(main_container, text="Читачі", width=20, height=5).grid(row=0, column=1, padx=10, pady=10)
        

        tk.Button(main_container, text="Оренда книг", width=20, height=5).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(main_container, text="Вихід", width=20, height=5).grid(row=1, column=1, padx=10, pady=10)

class LibrarianMenu(GeneralMenu):
    def __init__(self, parent):
        super().__init__(parent)

class AdminMenu(GeneralMenu):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Button(self, text="Бібліотекарі", width=20, height=5).pack(side="top", fill="x", pady=10)