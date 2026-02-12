import os
import subprocess
import shutil
import sys
import re
from version import APP_VERSION

def patch_setup_iss():
    """Patch setup.iss with the current version from version.py."""
    iss_path = "setup.iss"
    if not os.path.exists(iss_path):
        print(f"⚠️ {iss_path} not found, skipping version patch.")
        return
    with open(iss_path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = re.sub(
        r'#define MyAppVersion ".*?"',
        f'#define MyAppVersion "{APP_VERSION}"',
        content
    )
    with open(iss_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Patched {iss_path} with version {APP_VERSION}")

def run_build():
    print(f"🚀 Starting Build Process for RDP Heartbeat v{APP_VERSION}...")

    # 0. Patch setup.iss with current version
    patch_setup_iss()

    # 1. Clean previous builds
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")

    # 2. PyInstaller Command
    # --noconsole: Don't show a terminal window
    # --onefile: Bundle everything into a single .exe
    # --name: Output filename
    # --clean: Clean PyInstaller cache
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconsole",
        "--onefile",
        "--name=RDPHeartbeat",
        "--clean",
        # Icon configuration
        "--icon=icon.ico",
        "--add-data=icon.ico;.",
        # Explicitly import hidden imports if needed (sometimes pystray/PIL needs help)
        "--hidden-import=PIL._tkinter_finder",
        "--hidden-import=pystray",
        "main.py"
    ]

    print(f"📦 Running PyInstaller: {' '.join(cmd)}")
    try:
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        sys.exit(1)

    # 3. Verify Output
    exe_path = os.path.join("dist", "RDPHeartbeat.exe")
    if os.path.exists(exe_path):
        print(f"✅ Build Successful!")
        print(f"📁 Executable location: {os.path.abspath(exe_path)}")
        print("You can now run this EXE to test the application.")
    else:
        print("❌ Build finished but EXE was not found.")

if __name__ == "__main__":
    # Check if pyinstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("⚠️ PyInstaller is not installed. Installing it now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    run_build()
