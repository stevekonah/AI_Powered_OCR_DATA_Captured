from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox
from db.database import save_to_staging
from db.validation import validate_field
from db.corrections import save_correction
from PyQt5.QtCore import Qt

class ReviewTab(QWidget):
    def __init__(self, main_window, user):
        super().__init__()
        self.main_window = main_window
        self.user = user
        self.layout = QVBoxLayout(self)
        self.label = QLabel("Review and validate extracted data:")
        self.layout.addWidget(self.label)
        self.table = QTableWidget()
        self.layout.addWidget(self.table)
        self.save_button = QPushButton("Send for Supervisor Review")
        self.save_button.clicked.connect(self.save_data)
        self.layout.addWidget(self.save_button)
        self.data = {}
        self.form_type = None
        self.image_path = None

    def load_data(self, scanned_data, form_type, image_path=None):
        self.data = scanned_data
        self.form_type = form_type
        self.image_path = image_path
        self.table.clear()
        self.table.setRowCount(len(scanned_data))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Field", "Value", "Validation"])
        for row, (k, v) in enumerate(scanned_data.items()):
            self.table.setItem(row, 0, QTableWidgetItem(str(k)))
            value_item = QTableWidgetItem(str(v))
            value_item.setFlags(value_item.flags() | Qt.ItemIsEditable)
            self.table.setItem(row, 1, value_item)
            validation = validate_field(form_type, k, v)
            val_item = QTableWidgetItem("OK" if validation else "Invalid")
            if not validation:
                val_item.setBackground(Qt.red)
            self.table.setItem(row, 2, val_item)

    def save_data(self):
        corrected = False
        for row in range(self.table.rowCount()):
            key = self.table.item(row, 0).text()
            old_value = self.data.get(key, "")
            value = self.table.item(row, 1).text()
            if value != old_value:
                corrected = True
                save_correction(self.form_type, key, self.image_path or "", old_value, value)
            if not validate_field(self.form_type, key, value):
                QMessageBox.warning(self, "Validation Error", f"Field '{key}' is invalid. Please correct it.")
                return
            self.data[key] = value
        save_to_staging(self.data, self.form_type)
        msg = "Corrections saved, data sent for supervisor review." if corrected else "Data sent for supervisor review."
        QMessageBox.information(self, "Saved", msg)