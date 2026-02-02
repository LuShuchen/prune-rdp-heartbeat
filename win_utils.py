import ctypes
import platform
from ctypes import wintypes

# Constants for Windows API
GWL_EXSTYLE = -20
WS_EX_LAYERED = 0x00080000
WS_EX_TRANSPARENT = 0x00000020
SPI_GETWORKAREA = 0x0030
LWA_COLORKEY = 0x00000001
LWA_ALPHA = 0x00000002

def set_click_through(hwnd):
    """
    Makes the window transparent to mouse events (click-through).
    Requires the window to be a layered window.
    """
    if platform.system() != "Windows":
        return

    try:
        user32 = ctypes.windll.user32
        ex_style = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        user32.SetWindowLongW(hwnd, GWL_EXSTYLE, ex_style | WS_EX_LAYERED | WS_EX_TRANSPARENT)
    except Exception as e:
        print(f"Failed to set click-through: {e}")

def set_layered_attributes(hwnd, color_key_hex, alpha_float):
    """
    Directly sets the Layered Window Attributes to handle BOTH transparency (chroma key)
    and translucency (alpha) simultaneously.

    color_key_hex: string like "#000001"
    alpha_float: 0.0 to 1.0
    """
    if platform.system() != "Windows":
        return

    try:
        # Convert hex string to COLORREF (0x00BBGGRR)
        # hex is "#RRGGBB"
        r = int(color_key_hex[1:3], 16)
        g = int(color_key_hex[3:5], 16)
        b = int(color_key_hex[5:7], 16)
        crKey = (b << 16) | (g << 8) | r

        bAlpha = int(alpha_float * 255)

        # Ensure values are within byte range
        bAlpha = max(0, min(255, bAlpha))

        ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, crKey, bAlpha, LWA_COLORKEY | LWA_ALPHA)
    except Exception as e:
        print(f"Failed to set layered attributes: {e}")

def set_dpi_awareness():
    """Sets the process to be DPI aware."""
    if platform.system() != "Windows":
        return
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except:
            pass

def get_work_area():
    """
    Returns the (left, top, right, bottom) of the screen work area
    (excluding taskbar and docked bars).
    """
    if platform.system() != "Windows":
        # Fallback for non-Windows
        user32 = ctypes.windll.user32
        return (0, 0, user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))

    rect = wintypes.RECT()
    ctypes.windll.user32.SystemParametersInfoW(SPI_GETWORKAREA, 0, ctypes.byref(rect), 0)
    return (rect.left, rect.top, rect.right, rect.bottom)

def create_single_instance_mutex(name):
    """
    Tries to create a named mutex.
    Returns the handle if successful and we are the first instance.
    Returns None if the mutex already exists (another instance is running).
    """
    if platform.system() != "Windows":
        return 0 # No-op on non-Windows

    ERROR_ALREADY_EXISTS = 184
    kernel32 = ctypes.windll.kernel32
    mutex = kernel32.CreateMutexW(None, True, name)

    if kernel32.GetLastError() == ERROR_ALREADY_EXISTS:
        # Mutex exists, meaning another instance is running
        # We don't close the handle here, usually the OS cleans it up,
        # but technically we should close this handle since we didn't 'create' the mutex ownership
        # However, for a simple check, returning None is enough signal.
        return None

    return mutex

def release_mutex(handle):
    if handle and platform.system() == "Windows":
        ctypes.windll.kernel32.CloseHandle(handle)
