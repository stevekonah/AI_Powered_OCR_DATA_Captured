from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox
from db.database import get_pending_staging, approve_staging, reject_staging
from db.audit import log_action

class SupervisorModule(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.label = QLabel("Supervisor Review Panel")
        self.layout.addWidget(self.label)
        self.table = QTableWidget()
        self.layout.addWidget(self.table)
        self.approve_button = QPushButton("Approve")
        self.reject_button = QPushButton("Reject")
        self.approve_button.clicked.connect(self.approve_selected)
        self.reject_button.clicked.connect(self.reject_selected)
        self.layout.addWidget(self.approve_button)
        self.layout.addWidget(self.reject_button)
        self.pending = []

    def refresh_data(self):
        self.pending = get_pending_staging()
        self.table.clear()
        self.table.setRowCount(len(self.pending))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Form Type", "Data"])
        for row, entry in enumerate(self.pending):
            self.table.setItem(row, 0, QTableWidgetItem(str(entry.id)))
            self.table.setItem(row, 1, QTableWidgetItem(entry.form_type))
            self.table.setItem(row, 2, QTableWidgetItem(str(entry.field_data)))

    def approve_selected(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Select Entry", "Please select an entry to approve.")
            return
        entry = self.pending[selected]
        approve_staging(entry.id, "supervisor")
        log_action(entry.id, "staging_forms", "approve", "supervisor", old_value=entry.field_data)
        QMessageBox.information(self, "Approved", f"Entry {entry.id} approved.")
        self.refresh_data()

    def reject_selected(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Select Entry", "Please select an entry to reject.")
            return
        entry = self.pending[selected]
        reject_staging(entry.id, "supervisor")
        log_action(entry.id, "staging_forms", "reject", "supervisor", old_value=entry.field_data)
        QMessageBox.information(self, "Rejected", f"Entry {entry.id} rejected.")
        self.refresh_data()