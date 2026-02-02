import tkinter as tk
from tkinter import ttk
import webbrowser

class AboutDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("About RDP Heartbeat")
        self.geometry("300x200")
        self.resizable(False, False)

        # Make modal
        self.transient(parent)
        self.grab_set()

        self.create_widgets()
        self.center_window()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'+{x}+{y}')

    def create_widgets(self):
        frame = ttk.Frame(self, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        # Title / Icon placeholder
        title_lbl = ttk.Label(frame, text="RDP Heartbeat", font=("Segoe UI", 16, "bold"))
        title_lbl.pack(pady=(0, 5))

        # Version
        ver_lbl = ttk.Label(frame, text="Version 1.0.0", font=("Segoe UI", 10))
        ver_lbl.pack(pady=(0, 10))

        # Description
        desc_lbl = ttk.Label(frame, text="Keeps your remote session alive\nwith a subtle visual heartbeat.",
                             justify="center")
        desc_lbl.pack(pady=(0, 15))

        # Support Link
        link_lbl = tk.Label(frame, text="Visit Project Website", fg="blue", cursor="hand2")
        link_lbl.pack(pady=(0, 20))
        link_lbl.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/LuShuchen/prune-rdp-heartbeat"))

        # Close Button
        btn = ttk.Button(frame, text="Close", command=self.destroy)
        btn.pack()
