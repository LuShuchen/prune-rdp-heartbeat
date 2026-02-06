import sys
import threading
import tkinter as tk
import win_utils
from heartbeat_window import BreatheWindow
from tray_icon import start_tray
from settings_dialog import SettingsDialog
from about_dialog import AboutDialog

def main():
    # Set DPI awareness as early as possible (before Tk initialization)
    win_utils.set_dpi_awareness()

    # 0. Single Instance Check
    # We use a Global mutex to ensure it works across sessions if needed,
    # though "Local\" is safer for per-user session.
    # For a heartbeat tool, per-user is likely what we want.
    mutex_name = "Local\\RDPHeartbeatInstance"
    mutex = win_utils.create_single_instance_mutex(mutex_name)
    if mutex is None:
        # Another instance is running
        print("Another instance is already running. Exiting.")
        sys.exit(0)

    # 1. Create the GUI on the Main Thread
    app = BreatheWindow()

    # Thread-safe callbacks for the tray icon
    # Tkinter requires GUI updates to happen on the main thread
    # We use app.after(0, callback) to schedule them from the tray thread

    def safe_show():
        app.after(0, app.show)

    def safe_hide():
        app.after(0, app.hide)

    def safe_toggle_move():
        app.after(0, app.toggle_move_mode)

    def safe_open_settings():
        def open_settings_dialog():
            # Only open if not already open (basic check, can be improved)
            # For now, just create a new dialog
            dialog = SettingsDialog(app, app.config_manager)
            dialog.focus_force()

        app.after(0, open_settings_dialog)

    def safe_open_about():
        def open_about_dialog():
            dialog = AboutDialog(app)
            dialog.focus_force()
        app.after(0, open_about_dialog)

    def safe_exit():
        app.after(0, app.destroy)

    # 2. Start the System Tray in a Background Thread
    # pystray blocks its calling thread, so we must use a separate thread
    # to let Tkinter's mainloop run on the main thread.
    def run_tray():
        tray = start_tray(safe_show, safe_hide, safe_toggle_move, safe_open_settings, safe_open_about, safe_exit)
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
