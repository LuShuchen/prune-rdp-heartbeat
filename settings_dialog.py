import tkinter as tk
from tkinter import ttk, colorchooser

class SettingsDialog(tk.Toplevel):
    def __init__(self, parent, config_manager):
        super().__init__(parent)
        self.config_manager = config_manager
        self.title("Settings - RDP Heartbeat")
        self.geometry("300x400")
        self.resizable(False, False)

        # Make modal
        self.transient(parent)
        self.grab_set()

        self.create_widgets()

        # Center the window
        self.center_window()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'+{x}+{y}')

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Grid layout
        row = 0

        # Color
        ttk.Label(main_frame, text="Dot Color:").grid(row=row, column=0, sticky="w", pady=5)
        self.color_btn = tk.Button(main_frame, bg=self.config_manager.get("dot_color"),
                                   width=10, command=self.choose_color)
        self.color_btn.grid(row=row, column=1, sticky="e", pady=5)
        row += 1

        # Size
        ttk.Label(main_frame, text="Size (px):").grid(row=row, column=0, sticky="w", pady=5)
        self.size_var = tk.IntVar(value=self.config_manager.get("dot_size"))
        size_scale = ttk.Scale(main_frame, from_=8, to=64, variable=self.size_var,
                               orient="horizontal", command=lambda v: self.update_preview())
        size_scale.grid(row=row, column=1, sticky="we", pady=5)
        row += 1

        # Pulse Speed
        ttk.Label(main_frame, text="Pulse Speed (ms):").grid(row=row, column=0, sticky="w", pady=5)
        self.speed_var = tk.IntVar(value=self.config_manager.get("pulse_speed_ms"))
        speed_scale = ttk.Scale(main_frame, from_=10, to=200, variable=self.speed_var,
                                orient="horizontal")
        speed_scale.grid(row=row, column=1, sticky="we", pady=5)
        row += 1

        # Opacity Max
        ttk.Label(main_frame, text="Max Opacity:").grid(row=row, column=0, sticky="w", pady=5)
        self.opacity_max_var = tk.DoubleVar(value=self.config_manager.get("opacity_max"))
        op_max_scale = ttk.Scale(main_frame, from_=0.1, to=1.0, variable=self.opacity_max_var,
                                 orient="horizontal")
        op_max_scale.grid(row=row, column=1, sticky="we", pady=5)
        row += 1

        # Always on Top
        self.top_var = tk.BooleanVar(value=self.config_manager.get("always_on_top"))
        top_check = ttk.Checkbutton(main_frame, text="Always on Top", variable=self.top_var)
        top_check.grid(row=row, column=0, columnspan=2, sticky="w", pady=10)
        row += 1

        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=row, column=0, columnspan=2, pady=20)

        ttk.Button(btn_frame, text="Save", command=self.save_settings).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.destroy).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Reset Defaults", command=self.reset_settings).pack(side=tk.LEFT, padx=5)

    def choose_color(self):
        # Disable the settings window while color chooser is open
        # This prevents the user from clicking "Save" or "Cancel" while choosing a color
        self.attributes('-disabled', True)
        try:
            color = colorchooser.askcolor(initialcolor=self.config_manager.get("dot_color"),
                                          title="Choose Dot Color", parent=self)
        finally:
             self.attributes('-disabled', False)
             self.focus_force()

        if not self.winfo_exists():
            return

        if color[1]:
            self.color_btn.config(bg=color[1])
            self.current_color = color[1]
        else:
            self.current_color = self.config_manager.get("dot_color")

    def update_preview(self):
        # Could implement live preview logic here if desired
        pass

    def reset_settings(self):
        defaults = self.config_manager.DEFAULT_CONFIG

        # Color
        self.current_color = defaults["dot_color"]
        self.color_btn.config(bg=self.current_color)

        # Variables
        self.size_var.set(defaults["dot_size"])
        self.speed_var.set(defaults["pulse_speed_ms"])
        self.opacity_max_var.set(defaults["opacity_max"])
        self.top_var.set(defaults["always_on_top"])

    def save_settings(self):
        # Update config manager
        # Use current_color if set, else get from button (fallback)
        color = getattr(self, 'current_color', self.config_manager.get("dot_color"))

        self.config_manager.set("dot_color", color)
        self.config_manager.set("dot_size", self.size_var.get())
        self.config_manager.set("pulse_speed_ms", self.speed_var.get())
        self.config_manager.set("opacity_max", self.opacity_max_var.get())
        self.config_manager.set("always_on_top", self.top_var.get())

        self.config_manager.save()
        self.destroy()
