import customtkinter as ctk
from tkinter import colorchooser
import re

# 设置主题
ctk.set_appearance_mode("System") 
ctk.set_default_color_theme("blue")

class ColorInputDemo(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Color Input Group Demo")
        self.geometry("400x300")
        
        # 变量：存储当前颜色
        self.var_color = ctk.StringVar(value="#00FFFF")

        # === 核心代码开始：构建超级输入框 ===
        
        # 1. 外层容器 (模拟一个完整的输入框背景)
        # 这里的 border_color 和 border_width 决定了“输入框”的边框样式
        self.input_group = ctk.CTkFrame(
            self, 
            fg_color="white",          # 输入框内部背景色
            border_width=2,            # 边框宽度
            border_color="#E0E0E0",    # 边框颜色
            corner_radius=8            # 圆角
        )
        self.input_group.pack(pady=50, padx=50, fill="x")

        # 2. 左侧：颜色指示圆点 (用 Button 模拟圆形，hover=False 禁止交互效果)
        self.color_dot = ctk.CTkButton(
            self.input_group,
            text="", 
            width=24, 
            height=24, 
            corner_radius=12,          # 半径=宽度的一半，即为圆形
            fg_color=self.var_color.get(), # 初始颜色
            hover=False,               # 关掉鼠标悬停变色
            command=None               # 只是个指示器，不响应点击
        )
        self.color_dot.pack(side="left", padx=(10, 5), pady=8)

        # 3. 中间：真正的输入框 (去掉边框！)
        self.entry_hex = ctk.CTkEntry(
            self.input_group,
            textvariable=self.var_color,
            border_width=0,            # 关键：去掉自带边框
            fg_color="transparent",    # 透明背景，透出 Frame 的白色
            text_color="#333333",      # 文字颜色
            font=("Roboto Mono", 14),  # 等宽字体，显示代码更专业
            width=100
        )
        self.entry_hex.pack(side="left", fill="both", expand=True, pady=2)
        
        # 绑定键盘事件：松开按键时触发预览更新
        self.entry_hex.bind("<KeyRelease>", self.on_hex_input)

        # 4. 右侧：取色器按钮 (用 Unicode 字符模拟图标)
        self.btn_picker = ctk.CTkButton(
            self.input_group,
            text="🖊",                 # 笔图标，也可以换成 🎨
            font=("Arial", 16),
            width=36, 
            height=36,
            fg_color="transparent",    # 按钮背景透明
            text_color="#666666",      # 图标颜色
            hover_color="#F2F2F2",     # 鼠标悬停时的浅灰背景
            corner_radius=6,
            command=self.choose_color
        )
        self.btn_picker.pack(side="right", padx=(0, 5), pady=2)

        # === 核心代码结束 ===

        # 添加一个说明标签
        label = ctk.CTkLabel(self, text="试一试：\n1. 点击右边的笔选颜色\n2. 或者直接输入 #FF0000", text_color="gray")
        label.pack(pady=10)

    def choose_color(self):
        # 弹出系统取色盘
        color_code = colorchooser.askcolor(color=self.var_color.get())[1]
        if color_code:
            self.var_color.set(color_code.upper()) # 转大写更好看
            self.update_dot_color(color_code)

    def on_hex_input(self, event):
        # 监听手动输入
        hex_code = self.var_color.get()
        # 正则验证：简单的 Hex 颜色格式 (#RRGGBB)
        if re.match(r"^#[0-9A-Fa-f]{6}$", hex_code):
            self.update_dot_color(hex_code)

    def update_dot_color(self, color):
        try:
            self.color_dot.configure(fg_color=color)
            # 也可以在这里把 input_group 的边框变色，作为验证成功的反馈
            self.input_group.configure(border_color="#E0E0E0") 
        except:
            pass

if __name__ == "__main__":
    app = ColorInputDemo()
    app.mainloop()