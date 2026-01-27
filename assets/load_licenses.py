import os, sys, customtkinter

def license_path(relative_path):
    # for PyInstaller
    if hasattr(sys, 'frozen'):
        base_path = sys._MEIPASS
    # for development
    else:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


    return os.path.join(base_path, "assets", relative_path)

def license_window(self):
    win = customtkinter.CTkToplevel(self)
    win.title("Licenses")
    win.geometry("640x360")

    # Bring window to front
    win.lift()
    win.focus_force()
    win.grab_set()

    # Load license text
    license_file = license_path("licenses.txt")

    try:
        with open(license_file, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception as e:
        text = f"Could not load license file:\n{e}"

    # Scrollable textbox
    textbox = customtkinter.CTkTextbox(win, wrap="word")
    textbox.pack(fill="both", expand=True, padx=20, pady=20)
    textbox.insert("0.0", text)
    textbox.configure(state="disabled")