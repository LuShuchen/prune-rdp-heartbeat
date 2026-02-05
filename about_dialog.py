import customtkinter as ctk
import webbrowser

class AboutDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Make modal
        self.transient(parent)
        self.grab_set()

        # Window setup
        self.overrideredirect(True)
        self.attributes("-topmost", True)

        # UI Setup
        self.setup_custom_title_bar()
        self.setup_main_ui()
        self.center_window_adaptive()

        # Focus
        self.focus_force()

    def center_window_adaptive(self):
        self.update_idletasks()
        width = 320
        height = 340 # Slightly taller for the content
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        self.geometry(f"{width}x{height}+{x}+{y}")

    def setup_custom_title_bar(self):
        self.title_bar = ctk.CTkFrame(self, height=40, corner_radius=0, fg_color="#2B2B2B")
        self.title_bar.pack(side="top", fill="x")

        self.title_bar.bind("<ButtonPress-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.do_move)

        title_label = ctk.CTkLabel(self.title_bar, text="About", text_color="white", font=("Roboto Medium", 13))
        title_label.pack(side="left", padx=15)
        title_label.bind("<ButtonPress-1>", self.start_move)
        title_label.bind("<B1-Motion>", self.do_move)

        btn_close = ctk.CTkButton(self.title_bar, text="✕", width=40, height=40,
                                  fg_color="transparent", hover_color="#C42B1C",
                                  corner_radius=0, command=self.destroy)
        btn_close.pack(side="right")

    def setup_main_ui(self):
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#F0F0F0")
        self.main_frame.pack(fill="both", expand=True)

        # Content Card
        self.content_frame = ctk.CTkFrame(self.main_frame, corner_radius=10, fg_color="white")
        self.content_frame.pack(padx=20, pady=(20, 10), fill="both", expand=True)

        # Title
        ctk.CTkLabel(self.content_frame, text="RDP Heartbeat", font=("Roboto Medium", 20)).pack(pady=(20, 5))

        # Version
        ctk.CTkLabel(self.content_frame, text="Version 1.0.0", font=("Roboto", 12), text_color="gray50").pack(pady=(0, 15))

        # Description
        desc_text = "Keeps your remote session alive\nwith a subtle visual heartbeat."
        ctk.CTkLabel(self.content_frame, text=desc_text, font=("Roboto", 12), text_color="gray20").pack(pady=(0, 15))

        # Link
        btn_link = ctk.CTkButton(self.content_frame, text="Visit Project Website",
                                 fg_color="transparent", text_color="#1F6AA5", hover_color="#F0F0F0",
                                 font=("Roboto", 12, "underline"),
                                 height=25,
                                 cursor="hand2",
                                 command=lambda: webbrowser.open("https://github.com/LuShuchen/prune-rdp-heartbeat"))
        btn_link.pack(pady=(0, 20))

        # Close Button
        ctk.CTkButton(self.main_frame, text="Close", width=100, height=35, command=self.destroy).pack(pady=(10, 20))

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")
