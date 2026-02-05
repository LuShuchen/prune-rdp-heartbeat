import customtkinter as ctk
from tkinter import colorchooser

# Initialize theme (matches demo.py)
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class SettingsDialog(ctk.CTkToplevel):
    def __init__(self, parent, config_manager):
        super().__init__(parent)
        self.config_manager = config_manager

        # Make modal
        self.transient(parent)
        self.grab_set()

        # Window setup
        self.overrideredirect(True)
        self.attributes("-topmost", True)

        # Variables initialization from ConfigManager
        self.var_color = ctk.StringVar(value=self.config_manager.get("dot_color"))
        self.var_size = ctk.IntVar(value=self.config_manager.get("dot_size"))

        # Opacity: Config is 0.0-1.0, UI is 10-100
        op_val = int(self.config_manager.get("opacity_max") * 100)
        self.var_opacity = ctk.IntVar(value=op_val)

        self.var_speed = ctk.IntVar(value=self.config_manager.get("pulse_speed_ms"))
        self.var_top = ctk.BooleanVar(value=self.config_manager.get("always_on_top"))

        # Position reset flag
        self.reset_pos_requested = False

        # UI Setup
        self.setup_custom_title_bar()
        self.setup_main_ui()
        self.center_window_adaptive()

        # Focus
        self.focus_force()

    def center_window_adaptive(self):
        self.update_idletasks()
        width = 400
        # Ensure we have a reasonable height even if calculation is off initially
        height = max(self.winfo_reqheight(), 500)
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

        title_label = ctk.CTkLabel(self.title_bar, text="Settings", text_color="white", font=("Roboto Medium", 13))
        title_label.pack(side="left", padx=15)
        title_label.bind("<ButtonPress-1>", self.start_move)
        title_label.bind("<B1-Motion>", self.do_move)

        btn_close = ctk.CTkButton(self.title_bar, text="✕", width=40, height=40,
                                  fg_color="transparent", hover_color="#C42B1C",
                                  corner_radius=0, command=self.quit_app)
        btn_close.pack(side="right")

    def setup_main_ui(self):
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#F0F0F0")
        self.main_frame.pack(fill="both", expand=True)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # 1. Appearance
        self.frame_visual = ctk.CTkFrame(self.main_frame, corner_radius=10, fg_color="white")
        self.frame_visual.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        ctk.CTkLabel(self.frame_visual, text="APPEARANCE", font=("Roboto Medium", 11), text_color="gray").grid(row=0, column=0, sticky="w", padx=20, pady=(15, 5))

        # Color
        ctk.CTkLabel(self.frame_visual, text="Dot Color").grid(row=1, column=0, sticky="w", padx=20, pady=10)
        self.color_preview = ctk.CTkButton(self.frame_visual, text=self.var_color.get(), width=100,
                                           fg_color=self.var_color.get(), text_color="black", hover_color=self.var_color.get(),
                                           command=self.choose_color)
        self.color_preview.grid(row=1, column=1, sticky="e", padx=20)

        # Size
        ctk.CTkLabel(self.frame_visual, text="Size").grid(row=2, column=0, sticky="w", padx=20, pady=10)
        self.slider_size = ctk.CTkSlider(self.frame_visual, from_=5, to=64, variable=self.var_size, number_of_steps=59, command=self.update_size_label)
        self.slider_size.grid(row=2, column=1, sticky="ew", padx=(0, 10))
        self.lbl_size_val = ctk.CTkLabel(self.frame_visual, text=f"{self.var_size.get()} px", width=40)
        self.lbl_size_val.grid(row=2, column=2, padx=20)

        # Opacity
        ctk.CTkLabel(self.frame_visual, text="Max Opacity").grid(row=3, column=0, sticky="w", padx=20, pady=(10, 20))
        self.slider_op = ctk.CTkSlider(self.frame_visual, from_=10, to=100, variable=self.var_opacity, number_of_steps=90, command=self.update_op_label)
        self.slider_op.grid(row=3, column=1, sticky="ew", padx=(0, 10))
        self.lbl_op_val = ctk.CTkLabel(self.frame_visual, text=f"{self.var_opacity.get()} %", width=40)
        self.lbl_op_val.grid(row=3, column=2, padx=20, pady=(10, 20))

        self.frame_visual.grid_columnconfigure(1, weight=1)

        # 2. Behavior
        self.frame_behavior = ctk.CTkFrame(self.main_frame, corner_radius=10, fg_color="white")
        self.frame_behavior.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        ctk.CTkLabel(self.frame_behavior, text="BEHAVIOR", font=("Roboto Medium", 11), text_color="gray").grid(row=0, column=0, sticky="w", padx=20, pady=(15, 5))

        # Speed
        ctk.CTkLabel(self.frame_behavior, text="Pulse Speed").grid(row=1, column=0, sticky="w", padx=20, pady=10)
        self.slider_speed = ctk.CTkSlider(self.frame_behavior, from_=10, to=200, variable=self.var_speed, number_of_steps=19, command=self.update_speed_label)
        self.slider_speed.grid(row=1, column=1, sticky="ew", padx=(0, 10))
        self.lbl_speed_val = ctk.CTkLabel(self.frame_behavior, text=f"{self.var_speed.get()} ms", width=50)
        self.lbl_speed_val.grid(row=1, column=2, padx=20)

        # Always on Top
        ctk.CTkLabel(self.frame_behavior, text="Always on Top").grid(row=2, column=0, sticky="w", padx=20, pady=10)
        switch_top = ctk.CTkSwitch(self.frame_behavior, text="", variable=self.var_top, onvalue=True, offvalue=False)
        switch_top.grid(row=2, column=1, sticky="w", padx=0)

        # Position
        ctk.CTkLabel(self.frame_behavior, text="Position").grid(row=3, column=0, sticky="w", padx=20, pady=(10, 20))

        self.btn_center_text = ctk.StringVar(value="Reset to Center (Default)")
        # Check if custom
        if self.config_manager.get("window_x") is not None:
             self.btn_center_text.set("Reset to Default Position")

        self.btn_center = ctk.CTkButton(self.frame_behavior, textvariable=self.btn_center_text, fg_color="transparent",
                                   border_width=1, border_color=("gray70", "gray30"), text_color="gray20",
                                   height=28, command=self.reset_position)
        self.btn_center.grid(row=3, column=1, columnspan=2, sticky="w", pady=(10, 20))

        self.frame_behavior.grid_columnconfigure(1, weight=1)

        # 3. Actions
        self.frame_actions = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.frame_actions.grid(row=3, column=0, padx=20, pady=20, sticky="ew")

        btn_restore = ctk.CTkButton(self.frame_actions, text="Restore Defaults", fg_color="transparent", text_color="gray40", hover=False, anchor="w", command=self.restore_defaults)
        btn_restore.pack(side="left")

        btn_save = ctk.CTkButton(self.frame_actions, text="Save", width=100, height=35, command=self.save_settings)
        btn_save.pack(side="right")

        btn_cancel = ctk.CTkButton(self.frame_actions, text="Cancel", fg_color="transparent",
                                   border_width=1, border_color="gray70", text_color="gray20",
                                   width=80, height=35, command=self.quit_app)
        btn_cancel.pack(side="right", padx=10)

    # Logic
    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")

    def quit_app(self):
        self.destroy()

    def update_size_label(self, value): self.lbl_size_val.configure(text=f"{int(value)} px")
    def update_op_label(self, value): self.lbl_op_val.configure(text=f"{int(value)} %")
    def update_speed_label(self, value): self.lbl_speed_val.configure(text=f"{int(value)} ms")

    def choose_color(self):
        try:
            color = colorchooser.askcolor(color=self.var_color.get(), parent=self)[1]
            if color:
                self.var_color.set(color)
                self.color_preview.configure(text=color, fg_color=color)
        except Exception as e:
            print(f"Error picking color: {e}")

    def reset_position(self):
        self.reset_pos_requested = True
        self.btn_center_text.set("Position Reset Pending")

    def restore_defaults(self):
        d = self.config_manager.DEFAULT_CONFIG
        self.var_color.set(d["dot_color"])
        self.color_preview.configure(text=d["dot_color"], fg_color=d["dot_color"])

        self.var_size.set(d["dot_size"])
        self.update_size_label(d["dot_size"])

        op_val = int(d["opacity_max"] * 100)
        self.var_opacity.set(op_val)
        self.update_op_label(op_val)

        self.var_speed.set(d["pulse_speed_ms"])
        self.update_speed_label(d["pulse_speed_ms"])

        self.var_top.set(d["always_on_top"])

    def save_settings(self):
        self.config_manager.set("dot_color", self.var_color.get())
        self.config_manager.set("dot_size", self.var_size.get())
        self.config_manager.set("opacity_max", self.var_opacity.get() / 100.0)
        self.config_manager.set("pulse_speed_ms", self.var_speed.get())
        self.config_manager.set("always_on_top", self.var_top.get())

        if self.reset_pos_requested:
            self.config_manager.set("window_x", None)
            self.config_manager.set("window_y", None)

        self.config_manager.save()
        self.destroy()
