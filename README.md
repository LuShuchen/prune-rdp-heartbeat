# RDP Heartbeat

**A subtle, visual heartbeat for your remote desktop sessions.**

<a href="https://apps.microsoft.com/detail/9pc7fzmd5xkv?mode=mini">
  <img src="https://get.microsoft.com/images/en-us%20dark.svg" width="200"/>
</a>

> **[点击查看中文说明 (Chinese Readme)](README_zh.md)**

## Why this tool?

I work remotely via RDP extensively. My RDP connection runs over UDP, which is fast but can be unreliable. Often, when running long tasks like compiling code or waiting for AI coding tools, the screen would freeze silently. I'd be left wondering:

> *"Is the tool just thinking, or has my RDP connection dropped?"*

This uncertainty is frustrating. I created **RDP Heartbeat** to solve this. It places a small, unobtrusive "breathing" light on your screen.

*   **If the light is pulsing:** Your connection is alive.
*   **If the light freezes:** Your RDP connection has stalled.

It's a simple visual cue that saves sanity by letting you know immediately if you're actually disconnected, regardless of what's happening on screen.

## Features

*   **Visual Heartbeat:** A smooth, pulsing dot that indicates an active display stream.
*   **Modern UI:** Clean, frameless settings and about dialogs.
*   **Highly Customizable:**
    *   **Color:** Pick any color to match your wallpaper or preference.
    *   **Size:** Adjust from a tiny dot to a large indicator.
    *   **Opacity:** Control transparency so it doesn't block your work.
    *   **Speed:** Adjust the pulse speed.
    *   **Position:** Drag and drop the dot anywhere on your screen.
*   **Unobtrusive:** "Always on Top" mode ensures it's always visible but stays out of your way.
*   **System Tray:** Minimizes to the system tray for a clutter-free experience.
*   **Start on Boot:** Automatically starts with Windows, so you can set it and forget it. (New in v1.1)
*   **Multi-language:** Supports English and Simplified Chinese.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/LuShuchen/prune-rdp-heartbeat.git
    cd prune-rdp-heartbeat
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    ```bash
    python main.py
    ```

## Usage

*   **Launch:** Run the app. A pulsing dot will appear on your screen (default: bottom right).
*   **Move:** Click the system tray icon -> **Enable Move Mode** (or toggle via Settings) to enable drag-and-drop. The dot will show a border. Drag it to your desired spot. Click **Disable Move Mode** to lock it in place (click-through enabled).
*   **Configure:** Right-click the system tray icon -> **Settings**. Adjust color, size, speed, etc.
*   **Exit:** Right-click the system tray icon -> **Exit**.

## Building from Source

To create a standalone executable:

```bash
python build_release.py
```

The executable will be located in the `dist` folder.

---

*Created to make remote work a little less stressful.*
