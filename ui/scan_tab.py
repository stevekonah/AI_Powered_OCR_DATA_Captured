from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QFileDialog, QMessageBox, QProgressBar
from ui.threading_utils import WorkerThread
from ocr.ml_pipeline import extract_fields
from ocr.scanner_interface import scan_document

FORM_NAMES = ["FormA", "FormB", "FormC", "FormD"]

class ScanTab(QWidget):
    def __init__(self, main_window, user):
        super().__init__()
        self.main_window = main_window
        self.user = user
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(QLabel("Select Form Type:"))
        self.form_combo = QComboBox()
        self.form_combo.addItems(FORM_NAMES)
        self.layout.addWidget(self.form_combo)
        self.scan_button = QPushButton("Scan from Hardware")
        self.scan_button.clicked.connect(self.scan_from_scanner)
        self.layout.addWidget(self.scan_button)
        self.import_button = QPushButton("Import Image")
        self.import_button.clicked.connect(self.import_form)
        self.layout.addWidget(self.import_button)
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        self.layout.addWidget(self.progress)

    def scan_from_scanner(self):
        self.progress.setVisible(True)
        self.progress.setValue(10)
        self.worker = WorkerThread(scan_document)
        self.worker.finished.connect(self.handle_scanned)
        self.worker.start()

    def handle_scanned(self, image_path, error):
        if error or not image_path:
            QMessageBox.critical(self, "Scanner Error", str(error) if error else "Scan failed.")
            self.progress.setVisible(False)
            return
        self.progress.setValue(50)
        form_type = self.form_combo.currentText()
        self.worker = WorkerThread(extract_fields, image_path, form_type)
        self.worker.finished.connect(self.handle_extracted)
        self.worker.start()

    def import_form(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg *.tiff *.bmp)")
        if not file_name:
            return
        self.progress.setVisible(True)
        form_type = self.form_combo.currentText()
        self.worker = WorkerThread(extract_fields, file_name, form_type)
        self.worker.finished.connect(self.handle_extracted)
        self.worker.start()

    def handle_extracted(self, scanned_data, error):
        self.progress.setVisible(False)
        if error or not scanned_data:
            QMessageBox.critical(self, "Extraction Error", str(error) if error else "No data extracted.")
            return
        QMessageBox.information(self, "Done", "Form processed.")
        # Move to Review tab and load data
        self.main_window.tabs.setCurrentWidget(self.main_window.review_tab)
        self.main_window.review_tab.load_data(scanned_data, self.form_combo.currentText())