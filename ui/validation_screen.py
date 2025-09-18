from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox
from db.database import save_to_staging
from db.validation import validate_field
from PyQt5.QtGui import Qt
import json

class ValidationScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.label = QLabel("Review and validate extracted data:")
        self.layout.addWidget(self.label)
        self.table = QTableWidget()
        self.layout.addWidget(self.table)
        self.save_button = QPushButton("Send for Supervisor Review")
        self.save_button.clicked.connect(self.save_data)
        self.layout.addWidget(self.save_button)
        self.data = {}
        self.form_type = None

    def load_data(self, scanned_data, form_type):
        self.data = scanned_data
        self.form_type = form_type
        self.table.clear()
        self.table.setRowCount(len(scanned_data))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Field", "Value", "Validation"])
        for row, (k, v) in enumerate(scanned_data.items()):
            self.table.setItem(row, 0, QTableWidgetItem(str(k)))
            self.table.setItem(row, 1, QTableWidgetItem(str(v)))
            validation = validate_field(form_type, k, v)
            self.table.setItem(row, 2, QTableWidgetItem("OK" if validation else "Invalid"))
            if not validation:
                self.table.item(row, 2).setBackground(Qt.red)

    def save_data(self):
        # Collect edited data from table
        for row in range(self.table.rowCount()):
            key = self.table.item(row, 0).text()
            value = self.table.item(row, 1).text()
            if not validate_field(self.form_type, key, value):
                QMessageBox.warning(self, "Validation Error", f"Field '{key}' is invalid. Please correct it.")
                return
            self.data[key] = value
        save_to_staging(self.data, self.form_type)
        QMessageBox.information(self, "Saved", "Data sent for supervisor review.")
        self.main_window.stacked_widget.setCurrentWidget(self.main_window.form_selector)
