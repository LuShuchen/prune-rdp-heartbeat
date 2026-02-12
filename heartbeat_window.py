import tkinter as tk
import win_utils
from config_manager import ConfigManager
from logger import get_logger

logger = get_logger(__name__)

class BreatheWindow(tk.Tk):
    def __init__(self):
        super().__init__()

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
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Draw Circle
        self.dot_color = self.cfg.get("dot_color")
        self.draw_dot()

        # Interaction State
        self.move_mode = False

        # State tracking for config changes
        self._last_config_x = self.cfg.get("window_x")

        # Animation State
        self.alpha = 0.8
        self.fading_out = True

        # Bind the Map event to ensure we apply styles exactly when the window appears
        self.bind("<Map>", self.apply_window_styles)

        # Optimization: Track last applied alpha to avoid redundant API calls
        self._last_applied_alpha_int = -1

        # Start animation loop
        self.pulse()

    def update_position(self):
        try:
            left, top, right, bottom = win_utils.get_work_area()
        except:
            left, top = 0, 0
            right = self.winfo_screenwidth()
            bottom = self.winfo_screenheight()

        x = self.cfg.get("window_x")
        y = self.cfg.get("window_y")

        if x is not None and y is not None:
            # Clamp to screen boundaries to prevent clipping
            try:
                x = int(x)
                y = int(y)

                if x + self.size > right:
                    x = right - self.size
                if y + self.size > bottom:
                    y = bottom - self.size
                if x < left:
                    x = left
                if y < top:
                    y = top
            except:
                pass
        else:
            # Default behavior (bottom right with margin)
            x = right - self.size - 8
            y = bottom - self.size - 8

        self.geometry(f"{self.size}x{self.size}+{x}+{y}")
        self.update_idletasks()

    def toggle_move_mode(self):
        self.move_mode = not self.move_mode
        hwnd = getattr(self, '_cached_hwnd', self.winfo_id())

        if self.move_mode:
            win_utils.remove_click_through(hwnd)
            self.canvas.config(highlightthickness=2, highlightbackground="#FF0000")
            self.canvas.bind("<Button-1>", self.start_drag)
            self.canvas.bind("<B1-Motion>", self.on_drag)
            self.canvas.bind("<ButtonRelease-1>", self.end_drag)
        else:
            win_utils.set_click_through(hwnd)
            self.canvas.config(highlightthickness=0)
            self.canvas.unbind("<Button-1>")
            self.canvas.unbind("<B1-Motion>")
            self.canvas.unbind("<ButtonRelease-1>")

    def start_drag(self, event):
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def on_drag(self, event):
        deltax = event.x - self._drag_start_x
        deltay = event.y - self._drag_start_y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")

    def end_drag(self, event):
        self.cfg.set("window_x", self.winfo_x())
        self.cfg.set("window_y", self.winfo_y())

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
            # Try to get the specific HWND for the top-level window by title
            # This ensures we get the correct handle even with overrideredirect
            hwnd = win_utils.find_window_by_title(self.title())
            if not hwnd:
                hwnd = self.winfo_id()

            self._cached_hwnd = hwnd

            # 1. Ensure the window has the WS_EX_LAYERED style
            if self.move_mode:
                win_utils.remove_click_through(hwnd)
            else:
                win_utils.set_click_through(hwnd)

            # 2. Set the transparency key and initial alpha
            win_utils.set_layered_attributes(hwnd, self.bg_color, self.alpha)
        except Exception as e:
            logger.error(f"Error setting window styles: {e}")

    def pulse(self):
        # Reload key config items in case they changed (simple live reload)
        # For a more robust solution, we'd use an observer pattern, but this is lightweight.
        new_color = self.cfg.get("dot_color")
        if new_color != self.dot_color:
            self.dot_color = new_color
            self.draw_dot()

        new_size = self.cfg.get("dot_size")
        size_changed = new_size != self.size

        # Check if position was reset in config (changed from having value to None)
        # We need to track the 'custom position' state to detect this transition
        current_x_config = self.cfg.get("window_x")
        position_reset = (self._last_config_x is not None) and (current_x_config is None)
        self._last_config_x = current_x_config

        if size_changed or position_reset:
            self.size = new_size
            self.update_position()
            self.draw_dot()

        # Check Always on Top change
        always_on_top = self.cfg.get("always_on_top")
        # Note: -topmost returns 1/0, config has True/False
        current_top = self.attributes("-topmost")
        if bool(current_top) != always_on_top:
            self.attributes("-topmost", always_on_top)
            # Re-apply styles as attributes() can reset them on some Windows versions
            self.apply_window_styles()

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

        # Optimization: Only call Windows API if the visible alpha value changes
        current_alpha_int = int(self.alpha * 255)
        current_alpha_int = max(0, min(255, current_alpha_int))

        if current_alpha_int != self._last_applied_alpha_int:
            try:
                # Use cached HWND if available, else fallback
                hwnd = getattr(self, '_cached_hwnd', self.winfo_id())
                win_utils.set_layered_attributes(hwnd, self.bg_color, self.alpha)
                self._last_applied_alpha_int = current_alpha_int
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
