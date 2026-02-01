import tkinter as tk
import win_utils

class BreatheWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        win_utils.set_dpi_awareness()

        self.title("RDP Heartbeat")
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.attributes("-toolwindow", True) # Hide from taskbar

        # Background color for transparency
        self.bg_color = "#000001"
        self.config(bg=self.bg_color)

        # Dimensions (Small discrete dot)
        self.size = 16

        # Position (Bottom Right of WORK AREA)
        try:
            left, top, right, bottom = win_utils.get_work_area()
        except:
            right = self.winfo_screenwidth()
            bottom = self.winfo_screenheight()

        x = right - self.size - 8
        y = bottom - self.size - 8
        self.geometry(f"{self.size}x{self.size}+{x}+{y}")

        # Canvas for the dot
        self.canvas = tk.Canvas(self, width=self.size, height=self.size,
                                bg=self.bg_color, highlightthickness=0)
        self.canvas.pack()

        # Draw Cyan Circle
        self.dot_color = "#00FFFF"
        padding = 1
        self.oval = self.canvas.create_oval(padding, padding,
                                            self.size-padding, self.size-padding,
                                            fill=self.dot_color, outline="")

        # Animation State
        self.alpha = 0.8
        self.fading_out = True

        # Bind the Map event to ensure we apply styles exactly when the window appears
        self.bind("<Map>", self.apply_window_styles)

        # Start animation loop
        self.pulse()

    def apply_window_styles(self, event=None):
        """
        Applies the Windows-specific styles for transparency and click-through.
        This must be called AFTER the window is mapped by the OS.
        """
        try:
            hwnd = self.winfo_id()
            # 1. Ensure the window has the WS_EX_LAYERED style
            win_utils.set_click_through(hwnd)
            # 2. Set the transparency key and initial alpha
            win_utils.set_layered_attributes(hwnd, self.bg_color, self.alpha)
        except Exception as e:
            print(f"Error setting window styles: {e}")

    def pulse(self):
        step = 0.05
        if self.fading_out:
            self.alpha -= step
            if self.alpha <= 0.3:
                self.alpha = 0.3
                self.fading_out = False
        else:
            self.alpha += step
            if self.alpha >= 1.0:
                self.alpha = 1.0
                self.fading_out = True

        # Re-apply attributes every frame to ensure the alpha updates
        # and to persist the transparency key if Windows resets it.
        try:
            win_utils.set_layered_attributes(self.winfo_id(), self.bg_color, self.alpha)
        except:
            pass

        self.after(50, self.pulse)

    def show(self):
        self.deiconify()
        # When showing again, we need to re-apply styles
        self.after(10, self.apply_window_styles)

    def hide(self):
        self.withdraw()
