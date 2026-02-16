"""
Generate MSIX unplated icon assets from icon.ico.

Usage:
    python packaging/msix/generate_unplated_icons.py

This script reads the project's icon.ico file and generates
altform-unplated and altform-lightunplated PNG assets for MSIX packaging.
These assets ensure the app icon displays with a transparent background
in the taskbar, installed apps list, and other Windows Shell surfaces.

Note: The "Settings → Apps → Startup" page always applies a backplate
to MSIX StartupTask icons — this is a known Windows limitation.
"""

from PIL import Image
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
ICO_PATH = os.path.join(PROJECT_ROOT, "icon.ico")
OUT_DIR = os.path.join(SCRIPT_DIR, "Assets")

PREFIX = "RDPHEARTBEAT-Square44x44Logo"
TARGET_SIZES = [16, 24, 32, 44, 48, 256]
VARIANTS = ["altform-unplated", "altform-lightunplated"]


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    ico = Image.open(ICO_PATH)
    ico.size = (256, 256)
    src = ico.copy().convert("RGBA")

    for sz in TARGET_SIZES:
        resized = src.resize((sz, sz), Image.LANCZOS)
        for variant in VARIANTS:
            fname = f"{PREFIX}.targetsize-{sz}_{variant}.png"
            out_path = os.path.join(OUT_DIR, fname)
            resized.save(out_path, "PNG")
            print(f"Created: {fname} ({sz}x{sz}, RGBA)")

    print(f"\nDone! {len(TARGET_SIZES) * len(VARIANTS)} files generated in {OUT_DIR}")


if __name__ == "__main__":
    main()
