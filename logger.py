import logging
import os
import platform
from logging.handlers import RotatingFileHandler


def _get_log_dir():
    """Returns the log directory path."""
    if platform.system() == "Windows":
        base = os.environ.get("APPDATA", ".")
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(base, "RDPHeartbeat", "logs")
    os.makedirs(log_dir, exist_ok=True)
    return log_dir


def get_logger(name):
    """
    Get a configured logger instance.
    Uses RotatingFileHandler: max 1MB per file, 3 backups.
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger  # Already configured

    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # File handler
    try:
        log_path = os.path.join(_get_log_dir(), "rdp_heartbeat.log")
        file_handler = RotatingFileHandler(
            log_path, maxBytes=1_000_000, backupCount=3, encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception:
        pass  # Fail silently if log dir is not writable

    # Console handler (for development)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
