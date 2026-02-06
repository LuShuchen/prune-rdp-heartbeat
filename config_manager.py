import json
import os
import platform

class ConfigManager:
    DEFAULT_CONFIG = {
        "dot_color": "#00FFFF",  # Cyan
        "dot_size": 16,
        "opacity_max": 1.0,
        "opacity_min": 0.3,
        "pulse_speed_ms": 50,
        "always_on_top": True,
        "window_x": None,
        "window_y": None
    }

    def __init__(self, filename="config.json"):
        self.filename = filename
        self.config = self.DEFAULT_CONFIG.copy()
        self.load()

    def get_config_dir(self):
        """
        Returns the appropriate configuration directory for the platform.
        """
        if platform.system() == "Windows":
            return os.path.join(os.environ.get("APPDATA", "."), "RDPHeartbeat")
        else:
            # Fallback for dev/linux
            return os.path.dirname(os.path.abspath(__file__))

    def get_config_path(self):
        return os.path.join(self.get_config_dir(), self.filename)

    def load(self):
        """Loads config from file, creating it if missing."""
        path = self.get_config_path()
        try:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    user_config = json.load(f)
                    # Update defaults with user config (preserves new keys in defaults)
                    self.config.update(user_config)
            else:
                self.save() # Create default config file
        except Exception as e:
            print(f"Error loading config: {e}")

    def save(self):
        """Saves current config to file."""
        config_dir = self.get_config_dir()
        if not os.path.exists(config_dir):
            try:
                os.makedirs(config_dir)
            except OSError as e:
                print(f"Error creating config directory: {e}")
                return

        path = self.get_config_path()
        try:
            with open(path, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get(self, key):
        return self.config.get(key, self.DEFAULT_CONFIG.get(key))

    def set(self, key, value):
        self.config[key] = value
        self.save()
