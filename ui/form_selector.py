from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QFileDialog, QMessageBox
from ocr.ocr_engine import process_image
import os

FORM_NAMES = ["FormA", "FormB", "FormC", "FormD"]

class FormSelector(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(QLabel("Select Form Type:"))
        self.form_combo = QComboBox()
        self.form_combo.addItems(FORM_NAMES)
        self.layout.addWidget(self.form_combo)

        self.scan_button = QPushButton("Scan/Import Form Image")
        self.scan_button.clicked.connect(self.scan_form)
        self.layout.addWidget(self.scan_button)

    def scan_form(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg *.tiff *.bmp)")
        if not file_name:
            return
        form_type = self.form_combo.currentText()
        if not os.path.exists(f"form_templates/{form_type}.json"):
            QMessageBox.critical(self, "Error", f"Form template not found for {form_type}")
            return
        try:
            scanned_data = process_image(file_name, form_type)
            self.main_window.switch_to_validation(scanned_data, form_type)
        except Exception as e:
            QMessageBox.critical(self, "OCR Error", str(e))