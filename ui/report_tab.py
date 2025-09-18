from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit
from reports.reporting import generate_validation_report

class ReportTab(QWidget):
    def __init__(self, main_window, user):
        super().__init__()
        self.main_window = main_window
        self.user = user
        self.layout = QVBoxLayout(self)
        self.report_btn = QPushButton("Generate Validation Report")
        self.report_btn.clicked.connect(self.show_report)
        self.layout.addWidget(self.report_btn)
        self.text = QTextEdit()
        self.text.setReadOnly(True)
        self.layout.addWidget(self.text)

    def show_report(self):
        report = generate_validation_report()
        self.text.setText(report)