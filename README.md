# AI-Powered OCR Data Capture System

## Features

- User authentication (user/supervisor/admin, bcrypt-hashed)
- Advanced ML field extraction (with HuggingFace Donut/Classic OCR fallback)
- Multi-threaded scanner support (hardware or file import)
- Tabbed PyQt5 GUI (Scan, Review, Supervisor, Random Validation, Reports)
- Real-time validation with correction feedback for ML retraining
- Supervisor random spot-checks for quality
- Audit trail, batch reporting

## Scanner Support

- **Windows**: Will use TWAIN if available (32-bit only; most modern Windows users will fallback to file import).
- **Linux**: Will use SANE if `python-sane` and a compatible scanner are available.
- **macOS & all platforms**: Always allows file import.

> If no scanner is found or supported, you can always import an image file.

## Setup

1. Install requirements:  
   `pip install -r requirements.txt`
2. (Optional) On Linux, install scanner backends and `python-sane`.
3. Run the app:  
   `python main.py`

...