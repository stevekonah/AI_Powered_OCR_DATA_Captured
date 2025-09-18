import platform

def scan_document():
    system = platform.system()
    if system == "Windows":
        # Try TWAIN first
        try:
            import twain
            from PIL import Image
            import tempfile, os
            sm = twain.SourceManager(0)
            ss = sm.OpenSource()
            ss.RequestAcquire(0, 0)
            rv = ss.XferImageNatively()
            (handle, count) = rv
            if handle:
                import twain
                fd, temp_path = tempfile.mkstemp(suffix=".bmp")
                os.close(fd)
                twain.DIBToBMFile(handle, temp_path)
                return temp_path
            ss.destroy()
            sm.destroy()
        except Exception as e:
            print("TWAIN failed, trying WIA...")
            # Try WIA as fallback
            try:
                import win32com.client
                wia = win32com.client.Dispatch("WIA.CommonDialog")
                image = wia.ShowAcquireImage()
                temp_path = tempfile.mktemp(suffix=".bmp")
                image.SaveFile(temp_path)
                return temp_path
            except Exception as ex:
                print("WIA failed, fallback to file import.")
                return None
    else:
        # Linux: try SANE or fallback to import
        try:
            import sane
            sane.init()
            devices = sane.get_devices()
            if devices:
                dev = sane.open(devices[0][0])
                dev.start()
                im = dev.snap()
                temp_path = tempfile.mktemp(suffix=".png")
                im.save(temp_path)
                return temp_path
        except Exception as e:
            print("SANE failed, fallback to file import.")
            return None
    return None