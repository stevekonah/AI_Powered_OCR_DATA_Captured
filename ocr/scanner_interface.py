import platform

def scan_document(parent=None):
    """
    Tries to scan a document from hardware, falling back to file import if no scanner is available.
    Returns the file path of the scanned or imported image, or None if cancelled.
    """
    system = platform.system()
    try:
        if system == "Windows":
            try:
                import twain
                # Example: minimal TWAIN scan, will only work if TWAIN drivers and 32-bit Python
                sm = twain.SourceManager(0)
                ss = sm.OpenSource()
                ss.RequestAcquire(0, 0)
                rv = ss.XferImageNatively()
                if rv:
                    (handle, count) = rv
                    import PIL.Image
                    image = PIL.Image.frombytes('RGB', handle, 'raw')
                    path = "scanned_image_win.jpg"
                    image.save(path)
                    return path
            except Exception:
                pass  # TWAIN not available or scan failed, fallback to file import

        elif system == "Linux":
            try:
                import sane
                sane.init()
                devices = sane.get_devices()
                if devices:
                    dev = sane.open(devices[0][0])
                    dev.start()
                    image = dev.snap()
                    path = "scanned_image_linux.jpg"
                    image.save(path)
                    return path
            except Exception:
                pass  # SANE not available or scan failed, fallback to file import

        # On Mac or unsupported, always fallback
        # Fallback: prompt for file import using PyQt5
        try:
            from PyQt5.QtWidgets import QFileDialog
            file_name, _ = QFileDialog.getOpenFileName(parent, "Open Image", "", "Images (*.png *.jpg *.jpeg *.tiff *.bmp)")
            return file_name
        except Exception:
            print("PyQt5 not available: cannot import file.")
            return None
    except Exception as e:
        print(f"Scanner error: {e}")
        return None