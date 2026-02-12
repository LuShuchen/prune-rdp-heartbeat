import ctypes
import winreg
import sys
import os
from logger import get_logger

logger = get_logger(__name__)

# Registry path for non-MSIX auto-start
REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
APP_KEY = "RDPHeartbeat"


def is_msix_package():
    """
    Detect if running inside an MSIX container by checking for package identity.
    Uses kernel32.GetCurrentPackageFullName — returns error code 15700
    (APPMODEL_ERROR_NO_PACKAGE) if not running as a packaged app.
    """
    try:
        kernel32 = ctypes.windll.kernel32
        length = ctypes.c_uint32(0)
        result = kernel32.GetCurrentPackageFullName(ctypes.byref(length), None)
        # APPMODEL_ERROR_NO_PACKAGE = 15700
        return result != 15700
    except Exception:
        return False


def _get_exe_path():
    """Get path to the running executable (handles PyInstaller frozen builds)."""
    if getattr(sys, 'frozen', False):
        return sys.executable
    else:
        return os.path.abspath(sys.argv[0])


# ── Registry-based auto-start (non-MSIX) ──

def _reg_is_enabled():
    """Check if auto-start registry key exists."""
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_READ) as key:
            winreg.QueryValueEx(key, APP_KEY)
            return True
    except FileNotFoundError:
        return False
    except Exception as e:
        logger.error(f"Error checking auto-start registry: {e}")
        return False


def _reg_enable():
    """Add auto-start registry key."""
    try:
        exe_path = _get_exe_path()
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, APP_KEY, 0, winreg.REG_SZ, f'"{exe_path}"')
        logger.info(f"Auto-start enabled via registry: {exe_path}")
        return True
    except Exception as e:
        logger.error(f"Error enabling auto-start: {e}")
        return False


def _reg_disable():
    """Remove auto-start registry key."""
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_SET_VALUE) as key:
            winreg.DeleteValue(key, APP_KEY)
        logger.info("Auto-start disabled via registry")
        return True
    except FileNotFoundError:
        return True  # Already removed
    except Exception as e:
        logger.error(f"Error disabling auto-start: {e}")
        return False


# ── MSIX auto-start (opens Windows Settings) ──

def _msix_open_startup_settings():
    """Open Windows Settings → Startup Apps page."""
    try:
        os.startfile("ms-settings:startupapps")
        logger.info("Opened ms-settings:startupapps")
    except Exception as e:
        logger.error(f"Error opening startup settings: {e}")


# ── Public API ──

def enable_auto_start():
    """Enable auto-start. For MSIX, opens Windows Settings."""
    if is_msix_package():
        _msix_open_startup_settings()
    else:
        _reg_enable()


def disable_auto_start():
    """Disable auto-start. For MSIX, opens Windows Settings."""
    if is_msix_package():
        _msix_open_startup_settings()
    else:
        _reg_disable()


def is_auto_start_enabled():
    """
    Check if auto-start is enabled.
    Returns True/False for non-MSIX, None for MSIX (state unknown).
    """
    if is_msix_package():
        return None  # Can't query without winsdk
    else:
        return _reg_is_enabled()


def toggle_auto_start():
    """Toggle auto-start state. For MSIX, opens Windows Settings."""
    if is_msix_package():
        _msix_open_startup_settings()
    else:
        if _reg_is_enabled():
            _reg_disable()
        else:
            _reg_enable()
