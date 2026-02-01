import threading
import tkinter as tk
from heartbeat_window import BreatheWindow
from tray_icon import start_tray

def main():
    # 1. Create the GUI on the Main Thread
    app = BreatheWindow()

    # Thread-safe callbacks for the tray icon
    # Tkinter requires GUI updates to happen on the main thread
    # We use app.after(0, callback) to schedule them from the tray thread

    def safe_show():
        app.after(0, app.show)

    def safe_hide():
        app.after(0, app.hide)

    def safe_exit():
        app.after(0, app.destroy)

    # 2. Start the System Tray in a Background Thread
    # pystray blocks its calling thread, so we must use a separate thread
    # to let Tkinter's mainloop run on the main thread.
    def run_tray():
        tray = start_tray(safe_show, safe_hide, safe_exit)
        tray.run()

    tray_thread = threading.Thread(target=run_tray, daemon=True)
    tray_thread.start()

    # 3. Start GUI Event Loop (Blocks Main Thread)
    try:
        app.mainloop()
    except KeyboardInterrupt:
        app.destroy()

if __name__ == "__main__":
    main()
