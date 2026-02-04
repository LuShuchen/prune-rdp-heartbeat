import customtkinter as ctk
from tkinter import colorchooser

# === 全局设置 ===
ctk.set_appearance_mode("Light") 
ctk.set_default_color_theme("blue")

class ModernHeartbeatApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 1. 先把边框去掉
        self.overrideredirect(True) 
        
        # 变量初始化
        self.var_color = ctk.StringVar(value="#00FFFF")
        self.var_size = ctk.IntVar(value=15)
        self.var_opacity = ctk.IntVar(value=80)
        self.var_speed = ctk.IntVar(value=200)
        self.var_top = ctk.BooleanVar(value=True)

        # 2. 先构建 UI (这时候窗口还不可见)
        # 注意：这里我们不再先设定 geometry，而是等 UI 画完
        self.setup_custom_title_bar()
        self.setup_main_ui()

        # 3. 【核心修改】自适应大小与居中逻辑
        self.center_window_adaptive()

    def center_window_adaptive(self):
        # 强制更新一下界面任务，让 tkinter 计算出所有控件实际占用的宽高
        self.update_idletasks()
        
        # 获取界面实际需要的宽度和高度
        # 如果你觉得太窄，可以强制设一个最小宽度，比如 max(self.winfo_reqwidth(), 400)
        width = 400  # 宽度我们还是固定一下比较好看
        height = self.winfo_reqheight() # 高度让它自己算
        
        # 计算屏幕居中位置
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        
        # 应用计算好的大小和位置
        self.geometry(f"{width}x{height}+{x}+{y}")

    def setup_custom_title_bar(self):
        self.title_bar = ctk.CTkFrame(self, height=40, corner_radius=0, fg_color="#2B2B2B")
        self.title_bar.pack(side="top", fill="x")
        
        self.title_bar.bind("<ButtonPress-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.do_move)

        title_label = ctk.CTkLabel(self.title_bar, text="RDP Heartbeat", text_color="white", font=("Roboto Medium", 13))
        title_label.pack(side="left", padx=15)
        title_label.bind("<ButtonPress-1>", self.start_move)
        title_label.bind("<B1-Motion>", self.do_move)

        btn_close = ctk.CTkButton(self.title_bar, text="✕", width=40, height=40, 
                                  fg_color="transparent", hover_color="#C42B1C",
                                  corner_radius=0, command=self.quit_app)
        btn_close.pack(side="right")
        
        btn_min = ctk.CTkButton(self.title_bar, text="—", width=40, height=40, 
                                fg_color="transparent", hover_color="#444444",
                                corner_radius=0, command=self.minimize_app)
        btn_min.pack(side="right")

    def setup_main_ui(self):
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#F0F0F0") 
        self.main_frame.pack(fill="both", expand=True)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # 1. 外观分组
        self.frame_visual = ctk.CTkFrame(self.main_frame, corner_radius=10, fg_color="white") 
        self.frame_visual.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        
        ctk.CTkLabel(self.frame_visual, text="APPEARANCE", font=("Roboto Medium", 11), text_color="gray").grid(row=0, column=0, sticky="w", padx=20, pady=(15, 5))

        ctk.CTkLabel(self.frame_visual, text="Dot Color").grid(row=1, column=0, sticky="w", padx=20, pady=10)
        self.color_preview = ctk.CTkButton(self.frame_visual, text="#00FFFF", width=100, 
                                           fg_color="#00FFFF", text_color="black", hover_color="#00CCCC",
                                           command=self.choose_color)
        self.color_preview.grid(row=1, column=1, sticky="e", padx=20)

        ctk.CTkLabel(self.frame_visual, text="Size").grid(row=2, column=0, sticky="w", padx=20, pady=10)
        self.slider_size = ctk.CTkSlider(self.frame_visual, from_=5, to=50, variable=self.var_size, number_of_steps=45, command=self.update_size_label)
        self.slider_size.grid(row=2, column=1, sticky="ew", padx=(0, 10))
        self.lbl_size_val = ctk.CTkLabel(self.frame_visual, text="15 px", width=40)
        self.lbl_size_val.grid(row=2, column=2, padx=20)

        ctk.CTkLabel(self.frame_visual, text="Opacity").grid(row=3, column=0, sticky="w", padx=20, pady=(10, 20))
        self.slider_op = ctk.CTkSlider(self.frame_visual, from_=10, to=100, variable=self.var_opacity, number_of_steps=90, command=self.update_op_label)
        self.slider_op.grid(row=3, column=1, sticky="ew", padx=(0, 10))
        self.lbl_op_val = ctk.CTkLabel(self.frame_visual, text="80 %", width=40)
        self.lbl_op_val.grid(row=3, column=2, padx=20, pady=(10, 20))
        
        self.frame_visual.grid_columnconfigure(1, weight=1)

        # 2. 行为分组
        self.frame_behavior = ctk.CTkFrame(self.main_frame, corner_radius=10, fg_color="white")
        self.frame_behavior.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        ctk.CTkLabel(self.frame_behavior, text="BEHAVIOR", font=("Roboto Medium", 11), text_color="gray").grid(row=0, column=0, sticky="w", padx=20, pady=(15, 5))

        ctk.CTkLabel(self.frame_behavior, text="Pulse Speed").grid(row=1, column=0, sticky="w", padx=20, pady=10)
        self.slider_speed = ctk.CTkSlider(self.frame_behavior, from_=100, to=2000, variable=self.var_speed, number_of_steps=19, command=self.update_speed_label)
        self.slider_speed.grid(row=1, column=1, sticky="ew", padx=(0, 10))
        self.lbl_speed_val = ctk.CTkLabel(self.frame_behavior, text="200 ms", width=50)
        self.lbl_speed_val.grid(row=1, column=2, padx=20)

        ctk.CTkLabel(self.frame_behavior, text="Always on Top").grid(row=2, column=0, sticky="w", padx=20, pady=10)
        switch_top = ctk.CTkSwitch(self.frame_behavior, text="", variable=self.var_top, onvalue=True, offvalue=False)
        switch_top.grid(row=2, column=1, sticky="w", padx=0)

        ctk.CTkLabel(self.frame_behavior, text="Position").grid(row=3, column=0, sticky="w", padx=20, pady=(10, 20))
        btn_center = ctk.CTkButton(self.frame_behavior, text="Reset to Center", fg_color="transparent", 
                                   border_width=1, border_color=("gray70", "gray30"), text_color="gray20",
                                   height=28, command=self.reset_position)
        btn_center.grid(row=3, column=1, columnspan=2, sticky="w", pady=(10, 20))

        self.frame_behavior.grid_columnconfigure(1, weight=1)

        # 3. 底部按钮
        self.frame_actions = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.frame_actions.grid(row=3, column=0, padx=20, pady=20, sticky="ew")

        btn_restore = ctk.CTkButton(self.frame_actions, text="Restore Defaults", fg_color="transparent", text_color="gray40", hover=False, anchor="w", command=self.restore_defaults)
        btn_restore.pack(side="left")

        btn_save = ctk.CTkButton(self.frame_actions, text="Save Changes", width=120, height=35, command=self.save_settings)
        btn_save.pack(side="right")

        btn_cancel = ctk.CTkButton(self.frame_actions, text="Cancel", fg_color="transparent", 
                                   border_width=1, border_color="gray70", text_color="gray20",
                                   width=80, height=35, command=self.quit_app)
        btn_cancel.pack(side="right", padx=10)

    # === 逻辑处理 ===
    
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

    def minimize_app(self):
        self.overrideredirect(False)
        self.iconify()
        self.bind("<FocusIn>", self.on_deiconify)

    def on_deiconify(self, event):
        if self.state() == 'normal':
            self.overrideredirect(True)
            self.unbind("<FocusIn>")

    def update_size_label(self, value): self.lbl_size_val.configure(text=f"{int(value)} px")
    def update_op_label(self, value): self.lbl_op_val.configure(text=f"{int(value)} %")
    def update_speed_label(self, value): self.lbl_speed_val.configure(text=f"{int(value)} ms")
    def choose_color(self):
        color = colorchooser.askcolor(color=self.var_color.get())[1]
        if color:
            self.var_color.set(color)
            self.color_preview.configure(text=color, fg_color=color)
    def reset_position(self): print("UI: Position reset")
    def restore_defaults(self): pass
    def save_settings(self): print("UI: Settings Saved")

if __name__ == "__main__":
    app = ModernHeartbeatApp()
    app.mainloop()