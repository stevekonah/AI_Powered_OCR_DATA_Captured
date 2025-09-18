from PyQt5.QtWidgets import QMainWindow, QTabWidget, QAction
from ui.scan_tab import ScanTab
from ui.review_tab import ReviewTab
from ui.supervisor_tab import SupervisorTab
from ui.supervisor_random_validation import SupervisorRandomValidationTab
from ui.report_tab import ReportTab

class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.setWindowTitle("AI OCR Data Capture System")
        self.user = user
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.scan_tab = ScanTab(self, user)
        self.review_tab = ReviewTab(self, user)
        self.tabs.addTab(self.scan_tab, "Scan")
        self.tabs.addTab(self.review_tab, "Review")

        if user.role in ("supervisor", "admin"):
            self.supervisor_tab = SupervisorTab(self, user)
            self.supervisor_random_tab = SupervisorRandomValidationTab(self, user)
            self.tabs.addTab(self.supervisor_tab, "Supervisor")
            self.tabs.addTab(self.supervisor_random_tab, "Random Validation")

        if user.role == "admin":
            self.report_tab = ReportTab(self, user)
            self.tabs.addTab(self.report_tab, "Reports")

        self.statusBar().showMessage(f"Logged in as: {user.username} ({user.role})")
        logout_action = QAction("Logout", self)
        logout_action.triggered.connect(self.logout)
        self.menuBar().addAction(logout_action)

    def logout(self):
        self.close()  # Or re-show login dialog and reset session