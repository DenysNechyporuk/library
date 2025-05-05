import tkinter as tk
from features import login, menu
from features.books.booksView import booksView
from features.rents.bookRentView import RentPage
from features.readers.readerView import ReaderPage

class RouterApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("1280x720")
        self.title('Library')
        self._frame = None
        self.switch_frame("LoginPage")

    def switch_frame(self, frame_class_name):
        
        frame_classes = {
            "LoginPage": login.LoginPage,
            "LibrarianMenu": menu.LibrarianMenu,
            "AdminMenu": menu.AdminMenu,
            "BooksPage": booksView.BooksPage,
            "RentPage" : RentPage,
            "ReaderPage" : ReaderPage
        }
        
        frame_class = frame_classes.get(frame_class_name)
        if frame_class:
            new_frame = frame_class(self)
            if self._frame is not None:
                self._frame.destroy()
            self._frame = new_frame
            self._frame.pack()