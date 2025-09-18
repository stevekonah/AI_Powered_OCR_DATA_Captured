from PyQt5.QtWidgets import QApplication
from ui.login_dialog import LoginDialog
from ui.main_window import MainWindow
from db.database import init_db

def main():
    init_db()
    app = QApplication([])
    login = LoginDialog()
    if login.exec_() == login.Accepted:
        window = MainWindow(login.user)
        window.show()
        app.exec_()

if __name__ == "__main__":
    main()