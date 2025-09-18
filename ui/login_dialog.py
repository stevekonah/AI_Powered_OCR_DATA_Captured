from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from db.user_auth import authenticate_user

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setModal(True)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(QLabel("Username:"))
        self.username = QLineEdit()
        self.layout.addWidget(self.username)
        self.layout.addWidget(QLabel("Password:"))
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password)
        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.try_login)
        self.layout.addWidget(self.login_btn)
        self.user = None

    def try_login(self):
        user = authenticate_user(self.username.text(), self.password.text())
        if user:
            self.user = user
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Invalid credentials")