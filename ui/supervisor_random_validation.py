from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox
from db.database import get_random_validated
from PyQt5.QtCore import Qt 
class SupervisorRandomValidationTab(QWidget):
    def __init__(self, main_window, user):
        super().__init__()
        self.main_window = main_window
        self.user = user
        self.layout = QVBoxLayout(self)
        self.label = QLabel("Supervisor Random Validation (Spot Check)")
        self.layout.addWidget(self.label)
        self.table = QTableWidget()
        self.layout.addWidget(self.table)
        self.refresh_button = QPushButton("Sample Random Forms")
        self.refresh_button.clicked.connect(self.load_random_samples)
        self.layout.addWidget(self.refresh_button)
        self.validate_button = QPushButton("Mark as Spot-Validated")
        self.validate_button.clicked.connect(self.validate_selected)
        self.layout.addWidget(self.validate_button)
        self.samples = []
        self.load_random_samples()

    def load_random_samples(self, sample_size=5):
        self.samples = get_random_validated(sample_size)
        self.table.clear()
        self.table.setRowCount(len(self.samples))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Form Type", "Data"])
        for row, entry in enumerate(self.samples):
            self.table.setItem(row, 0, QTableWidgetItem(str(entry.id)))
            self.table.setItem(row, 1, QTableWidgetItem(entry.form_type))
            self.table.setItem(row, 2, QTableWidgetItem(str(entry.field_data)))

    def validate_selected(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Select Entry", "Select an entry to mark as spot-validated.")
            return
        entry = self.samples[selected]
        # Optionally, mark with a "spot_validated" flag in the DB
        QMessageBox.information(self, "Validated", f"Entry {entry.id} spot-validated.")
