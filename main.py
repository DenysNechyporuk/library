from routesapp import RouterApp
from database import init_db

def main():
    init_db()  # Створює всі таблиці перед запуском додатка
    app = RouterApp()
    app.mainloop()

if __name__ == "__main__":
    main()