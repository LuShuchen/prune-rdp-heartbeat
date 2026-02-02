import tkinter as tk
import win_utils
from config_manager import ConfigManager

class BreatheWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        win_utils.set_dpi_awareness()

        # Load Config
        self.config_manager = ConfigManager()
        self.cfg = self.config_manager

        self.title("RDP Heartbeat")
        self.overrideredirect(True)
        self.attributes("-topmost", self.cfg.get("always_on_top"))
        self.attributes("-toolwindow", True) # Hide from taskbar

        # Background color for transparency
        self.bg_color = "#000001"
        self.config(bg=self.bg_color)

        # Dimensions
        self.size = self.cfg.get("dot_size")

        # Position (Bottom Right of WORK AREA)
        self.update_position()

        # Canvas for the dot
        self.canvas = tk.Canvas(self, width=self.size, height=self.size,
                                bg=self.bg_color, highlightthickness=0)
        self.canvas.pack()

        # Draw Circle
        self.dot_color = self.cfg.get("dot_color")
        self.draw_dot()

        # Animation State
        self.alpha = 0.8
        self.fading_out = True

        # Bind the Map event to ensure we apply styles exactly when the window appears
        self.bind("<Map>", self.apply_window_styles)

        # Start animation loop
        self.pulse()

    def update_position(self):
        try:
            left, top, right, bottom = win_utils.get_work_area()
        except:
            right = self.winfo_screenwidth()
            bottom = self.winfo_screenheight()

        x = right - self.size - 8
        y = bottom - self.size - 8
        self.geometry(f"{self.size}x{self.size}+{x}+{y}")

    def draw_dot(self):
        self.canvas.delete("all")
        padding = 1
        self.oval = self.canvas.create_oval(padding, padding,
                                            self.size-padding, self.size-padding,
                                            fill=self.dot_color, outline="")

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
        # Reload key config items in case they changed (simple live reload)
        # For a more robust solution, we'd use an observer pattern, but this is lightweight.
        new_color = self.cfg.get("dot_color")
        if new_color != self.dot_color:
            self.dot_color = new_color
            self.draw_dot()

        new_size = self.cfg.get("dot_size")
        if new_size != self.size:
            self.size = new_size
            self.canvas.config(width=self.size, height=self.size)
            self.update_position()
            self.draw_dot()

        # Check Always on Top change
        always_on_top = self.cfg.get("always_on_top")
        # Note: -topmost returns 1/0, config has True/False
        current_top = self.attributes("-topmost")
        if bool(current_top) != always_on_top:
            self.attributes("-topmost", always_on_top)

        step = 0.05
        min_alpha = self.cfg.get("opacity_min")
        max_alpha = self.cfg.get("opacity_max")

        if self.fading_out:
            self.alpha -= step
            if self.alpha <= min_alpha:
                self.alpha = min_alpha
                self.fading_out = False
        else:
            self.alpha += step
            if self.alpha >= max_alpha:
                self.alpha = max_alpha
                self.fading_out = True

        # Re-apply attributes every frame to ensure the alpha updates
        try:
            win_utils.set_layered_attributes(self.winfo_id(), self.bg_color, self.alpha)
        except:
            pass

        speed = self.cfg.get("pulse_speed_ms")
        self.after(speed, self.pulse)

    def show(self):
        self.deiconify()
        # When showing again, we need to re-apply styles
        self.after(10, self.apply_window_styles)

    def hide(self):
        self.withdraw()
