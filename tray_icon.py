from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw

def create_icon():
    # Create an icon image: Black background, Cyan circle
    # Size 64x64
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), color=(0, 0, 0)) # Black bg
    dc = ImageDraw.Draw(image)

    # Draw Cyan Circle
    padding = 8
    # Color: Cyan (#00FFFF)
    dc.ellipse((padding, padding, width-padding, height-padding), fill=(0, 255, 255))

    return image

class TrayController:
    def __init__(self, on_show, on_hide, on_move, on_settings, on_about, on_exit):
        self.on_show = on_show
        self.on_hide = on_hide
        self.on_move = on_move
        self.on_settings = on_settings
        self.on_about = on_about
        self.on_exit = on_exit
        self.icon = None

    def run(self):
        menu = Menu(
            MenuItem('Show', self.on_show_clicked),
            MenuItem('Hide', self.on_hide_clicked),
            MenuItem('Move Window', self.on_move_clicked),
            MenuItem('Settings', self.on_settings_clicked),
            MenuItem('About', self.on_about_clicked),
            MenuItem('Exit', self.on_exit_clicked)
        )

        self.icon = Icon("RDP Heartbeat", create_icon(), "RDP Canary", menu)
        self.icon.run()

    def on_show_clicked(self, icon, item):
        if self.on_show:
            self.on_show()

    def on_hide_clicked(self, icon, item):
        if self.on_hide:
            self.on_hide()

    def on_move_clicked(self, icon, item):
        if self.on_move:
            self.on_move()

    def on_settings_clicked(self, icon, item):
        if self.on_settings:
            self.on_settings()

    def on_about_clicked(self, icon, item):
        if self.on_about:
            self.on_about()

    def on_exit_clicked(self, icon, item):
        icon.stop()
        if self.on_exit:
            self.on_exit()

def start_tray(on_show, on_hide, on_move, on_settings, on_about, on_exit):
    """
    Starts the tray icon controller.
    """
    return TrayController(on_show, on_hide, on_move, on_settings, on_about, on_exit)
