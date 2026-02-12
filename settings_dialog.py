import customtkinter as ctk
from tkinter import colorchooser
import re
from logger import get_logger
import i18n
from i18n import t

logger = get_logger(__name__)

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
        width = 460  # Increased from 400 to fit new UI elements better
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

        title_label = ctk.CTkLabel(self.title_bar, text=t("settings.title"), text_color="white", font=("Roboto Medium", 13))
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
        self.frame_visual.grid_columnconfigure(0, minsize=150)  # Align labels across groups
        self.frame_visual.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.frame_visual, text=t("settings.appearance"), font=("Roboto Medium", 11), text_color="gray").grid(row=0, column=0, sticky="w", padx=20, pady=(15, 5))

        # Color
        ctk.CTkLabel(self.frame_visual, text=t("settings.dot_color")).grid(row=1, column=0, sticky="w", padx=20, pady=(12, 10))

        # New Color Input Group (adapted from demo.py)
        self.input_group = ctk.CTkFrame(
            self.frame_visual,
            fg_color="white",          # Match parent bg
            border_width=2,
            border_color="#E0E0E0",
            corner_radius=8
        )
        self.input_group.grid(row=1, column=1, columnspan=2, sticky="ew", padx=(0, 20), pady=10)

        # 1. Color Dot
        self.color_dot = ctk.CTkButton(
            self.input_group,
            text="",
            width=24,
            height=24,
            corner_radius=12,
            fg_color=self.var_color.get(),
            hover=False,
            command=None
        )
        self.color_dot.pack(side="left", padx=(10, 5), pady=8)

        # 2. Picker Button (Pack RIGHT before filling center)
        self.btn_picker = ctk.CTkButton(
            self.input_group,
            text="🖊",
            font=("Arial", 16),
            width=36,
            height=36,
            fg_color="transparent",
            text_color="#666666",
            hover_color="#F2F2F2",
            corner_radius=6,
            command=self.choose_color
        )
        self.btn_picker.pack(side="right", padx=(0, 5), pady=2)

        # 3. Hex Entry (Fill remaining space)
        self.entry_hex = ctk.CTkEntry(
            self.input_group,
            textvariable=self.var_color,
            border_width=0,
            fg_color="transparent",
            text_color="#333333",
            font=("Roboto Mono", 12),
            width=100
        )
        self.entry_hex.pack(side="left", fill="both", expand=True, pady=2)
        self.entry_hex.bind("<KeyRelease>", self.on_hex_input)

        # Size
        ctk.CTkLabel(self.frame_visual, text=t("settings.size")).grid(row=2, column=0, sticky="w", padx=20, pady=10)
        self.slider_size = ctk.CTkSlider(self.frame_visual, from_=5, to=64, variable=self.var_size, number_of_steps=59, command=self.update_size_label)
        self.slider_size.grid(row=2, column=1, sticky="ew", padx=(0, 10))
        self.lbl_size_val = ctk.CTkLabel(self.frame_visual, text=f"{self.var_size.get()} px", width=50)
        self.lbl_size_val.grid(row=2, column=2, padx=20)

        # Opacity
        ctk.CTkLabel(self.frame_visual, text=t("settings.max_opacity")).grid(row=3, column=0, sticky="w", padx=20, pady=(10, 20))
        self.slider_op = ctk.CTkSlider(self.frame_visual, from_=10, to=100, variable=self.var_opacity, number_of_steps=90, command=self.update_op_label)
        self.slider_op.grid(row=3, column=1, sticky="ew", padx=(0, 10))
        self.lbl_op_val = ctk.CTkLabel(self.frame_visual, text=f"{self.var_opacity.get()} %", width=50)
        self.lbl_op_val.grid(row=3, column=2, padx=20, pady=(10, 20))

        # Removed redundant columnconfigure(1) here since we moved it up

        # 2. Behavior
        self.frame_behavior = ctk.CTkFrame(self.main_frame, corner_radius=10, fg_color="white")
        self.frame_behavior.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.frame_behavior.grid_columnconfigure(0, minsize=150) # Align labels across groups
        self.frame_behavior.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.frame_behavior, text=t("settings.behavior"), font=("Roboto Medium", 11), text_color="gray").grid(row=0, column=0, sticky="w", padx=20, pady=(15, 5))

        # Speed
        ctk.CTkLabel(self.frame_behavior, text=t("settings.pulse_speed")).grid(row=1, column=0, sticky="w", padx=20, pady=10)
        self.slider_speed = ctk.CTkSlider(self.frame_behavior, from_=10, to=200, variable=self.var_speed, number_of_steps=19, command=self.update_speed_label)
        self.slider_speed.grid(row=1, column=1, sticky="ew", padx=(0, 10))
        self.lbl_speed_val = ctk.CTkLabel(self.frame_behavior, text=f"{self.var_speed.get()} ms", width=50)
        self.lbl_speed_val.grid(row=1, column=2, padx=20)

        # Always on Top
        ctk.CTkLabel(self.frame_behavior, text=t("settings.always_on_top")).grid(row=2, column=0, sticky="w", padx=20, pady=10)
        switch_top = ctk.CTkSwitch(self.frame_behavior, text="", variable=self.var_top, onvalue=True, offvalue=False)
        switch_top.grid(row=2, column=1, sticky="w", padx=0)

        # Language
        ctk.CTkLabel(self.frame_behavior, text=t("settings.language")).grid(row=3, column=0, sticky="w", padx=20, pady=10)
        languages = i18n.get_available_languages()
        lang_display_values = list(languages.values())
        lang_codes = list(languages.keys())
        # Map current config value to display name
        current_lang_config = self.config_manager.get("language")
        if current_lang_config == "auto":
            current_display = "Auto"
        else:
            current_display = languages.get(current_lang_config, "English")
        self.var_language = ctk.StringVar(value=current_display)
        self.lang_menu = ctk.CTkOptionMenu(
            self.frame_behavior,
            variable=self.var_language,
            values=["Auto"] + lang_display_values,
            width=200, height=28, corner_radius=6,
            fg_color="#EEEEEE",
            button_color="#DADADA", button_hover_color="#CCCCCC",
            text_color="#333333",
            dropdown_fg_color="#FFFFFF", dropdown_hover_color="#E8E8E8",
            dropdown_text_color="#333333",
            font=("Roboto", 12)
        )
        self.lang_menu.grid(row=3, column=1, sticky="w", padx=0)

        # Auto-Start
        ctk.CTkLabel(self.frame_behavior, text=t("settings.auto_start")).grid(row=4, column=0, sticky="w", padx=20, pady=10)
        import startup
        if startup.is_msix_package():
            # MSIX: Show button to open Windows Settings
            btn_autostart = ctk.CTkButton(
                self.frame_behavior, text=t("settings.auto_start_manage"),
                fg_color="transparent", border_width=1, border_color=("gray70", "gray30"),
                text_color="gray20", height=28, width=250,
                command=lambda: startup._msix_open_startup_settings()
            )
            btn_autostart.grid(row=4, column=1, columnspan=2, sticky="w")
        else:
            # Non-MSIX: Show toggle switch
            self.var_auto_start = ctk.BooleanVar(value=startup.is_auto_start_enabled() or False)
            self.switch_autostart = ctk.CTkSwitch(
                self.frame_behavior, text="", variable=self.var_auto_start,
                onvalue=True, offvalue=False
            )
            self.switch_autostart.grid(row=4, column=1, sticky="w", padx=0)

        # Position
        ctk.CTkLabel(self.frame_behavior, text=t("settings.position")).grid(row=5, column=0, sticky="w", padx=20, pady=(10, 20))

        self.btn_center_text = ctk.StringVar(value=t("settings.reset_bottom_right"))
        # Check if custom
        if self.config_manager.get("window_x") is not None:
             self.btn_center_text.set(t("settings.reset_default"))

        self.btn_center = ctk.CTkButton(self.frame_behavior, textvariable=self.btn_center_text, fg_color="transparent",
                                   border_width=1, border_color=("gray70", "gray30"), text_color="gray20",
                                   height=28, width=250, command=self.reset_position)
        self.btn_center.grid(row=5, column=1, columnspan=2, sticky="w", pady=(10, 20))

        # Removed redundant columnconfigure(1) here since we moved it up

        # 3. Actions
        self.frame_actions = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.frame_actions.grid(row=3, column=0, padx=20, pady=20, sticky="ew")

        btn_restore = ctk.CTkButton(self.frame_actions, text=t("settings.restore_defaults"), fg_color="transparent", text_color="gray40", hover=False, anchor="w", command=self.restore_defaults)
        btn_restore.pack(side="left")

        btn_save = ctk.CTkButton(self.frame_actions, text=t("settings.save"), width=120, height=35, command=self.save_settings)
        btn_save.pack(side="right")

        btn_cancel = ctk.CTkButton(self.frame_actions, text=t("settings.cancel"), fg_color="transparent",
                                   border_width=1, border_color="gray70", text_color="gray20",
                                   width=100, height=35, command=self.quit_app)
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

    def on_hex_input(self, event):
        hex_code = self.var_color.get()
        if re.match(r"^#[0-9A-Fa-f]{6}$", hex_code):
            self.update_dot_color(hex_code)

    def update_dot_color(self, color):
        try:
            self.color_dot.configure(fg_color=color)
            self.input_group.configure(border_color="#E0E0E0")
        except:
            pass

    def choose_color(self):
        try:
            color = colorchooser.askcolor(color=self.var_color.get(), parent=self)[1]
            if color:
                color = color.upper()
                self.var_color.set(color)
                self.update_dot_color(color)
        except Exception as e:
            logger.error(f"Error picking color: {e}")

    def reset_position(self):
        self.reset_pos_requested = True
        self.btn_center_text.set(t("settings.reset_pending"))

    def restore_defaults(self):
        d = self.config_manager.DEFAULT_CONFIG
        self.var_color.set(d["dot_color"])
        self.update_dot_color(d["dot_color"])

        self.var_size.set(d["dot_size"])
        self.update_size_label(d["dot_size"])

        op_val = int(d["opacity_max"] * 100)
        self.var_opacity.set(op_val)
        self.update_op_label(op_val)

        self.var_speed.set(d["pulse_speed_ms"])
        self.update_speed_label(d["pulse_speed_ms"])

        self.var_top.set(d["always_on_top"])
        self.var_language.set("Auto")

    def save_settings(self):
        self.config_manager.set("dot_color", self.var_color.get())
        self.config_manager.set("dot_size", self.var_size.get())
        self.config_manager.set("opacity_max", self.var_opacity.get() / 100.0)
        self.config_manager.set("pulse_speed_ms", self.var_speed.get())
        self.config_manager.set("always_on_top", self.var_top.get())

        # Language
        lang_display = self.var_language.get()
        if lang_display == "Auto":
            lang_code = "auto"
        else:
            # Reverse lookup: display name → code
            languages = i18n.get_available_languages()
            lang_code = next((k for k, v in languages.items() if v == lang_display), "en")
        self.config_manager.set("language", lang_code)
        i18n.set_language(lang_code)

        # Refresh tray menu labels immediately
        parent = self.master
        if hasattr(parent, 'tray_controller') and parent.tray_controller.icon:
            try:
                parent.tray_controller.icon.update_menu()
            except Exception:
                pass

        # Auto-start (non-MSIX only has the toggle)
        if hasattr(self, 'var_auto_start'):
            import startup
            want_auto = self.var_auto_start.get()
            if want_auto:
                startup.enable_auto_start()
            else:
                startup.disable_auto_start()
            self.config_manager.set("auto_start", want_auto)

        if self.reset_pos_requested:
            self.config_manager.set("window_x", None)
            self.config_manager.set("window_y", None)

        self.config_manager.save()
        self.destroy()
