import locale
from logger import get_logger

logger = get_logger(__name__)

LANGUAGES = {"en": "English", "zh": "中文"}

STRINGS = {
    "en": {
        # Tray menu
        "tray.show": "Show",
        "tray.hide": "Hide",
        "tray.move_enable": "Enable Move Mode",
        "tray.move_disable": "Disable Move Mode",
        "tray.settings": "Settings",
        "tray.about": "About",
        "tray.exit": "Exit",

        # Settings dialog
        "settings.title": "Settings",
        "settings.appearance": "APPEARANCE",
        "settings.dot_color": "Dot Color",
        "settings.size": "Size",
        "settings.max_opacity": "Max Opacity",
        "settings.behavior": "BEHAVIOR",
        "settings.pulse_speed": "Pulse Speed",
        "settings.always_on_top": "Always on Top",
        "settings.position": "Position",
        "settings.reset_default": "Reset to Default Position",
        "settings.reset_bottom_right": "Reset to Bottom Right (Default)",
        "settings.reset_pending": "Position Reset Pending",
        "settings.restore_defaults": "Restore Defaults",
        "settings.save": "Save",
        "settings.cancel": "Cancel",
        "settings.language": "Language",
        "settings.auto_start": "Start with Windows",
        "settings.auto_start_manage": "Manage in Windows Settings →",

        # About dialog
        "about.title": "About",
        "about.app_name": "RDP Heartbeat",
        "about.description": "A visual heartbeat to detect\nsilent RDP freezes and connection drops.",
        "about.visit_website": "Visit Project Website",
        "about.close": "Close",
    },
    "zh": {
        # Tray menu
        "tray.show": "显示",
        "tray.hide": "隐藏",
        "tray.move_enable": "拖动模式",
        "tray.move_disable": "锁定位置",
        "tray.settings": "设置",
        "tray.about": "关于",
        "tray.exit": "退出",

        # Settings dialog
        "settings.title": "设置",
        "settings.appearance": "外观",
        "settings.dot_color": "光点颜色",
        "settings.size": "大小",
        "settings.max_opacity": "最大不透明度",
        "settings.behavior": "行为",
        "settings.pulse_speed": "脉冲速度",
        "settings.always_on_top": "始终置顶",
        "settings.position": "位置",
        "settings.reset_default": "重置到默认位置",
        "settings.reset_bottom_right": "重置到右下角（默认）",
        "settings.reset_pending": "位置重置待生效",
        "settings.restore_defaults": "恢复默认",
        "settings.save": "保存",
        "settings.cancel": "取消",
        "settings.language": "语言",
        "settings.auto_start": "开机自启动",
        "settings.auto_start_manage": "在 Windows 设置中管理 →",

        # About dialog
        "about.title": "关于",
        "about.app_name": "RDP Heartbeat",
        "about.description": "用于检测远程桌面\n连接中断的可视化心跳工具。",
        "about.visit_website": "访问项目网站",
        "about.close": "关闭",
    }
}

_current_lang = "en"
_config_manager = None


def init(config_manager):
    """Initialize i18n from config. 'auto' detects system locale."""
    global _current_lang, _config_manager
    _config_manager = config_manager
    lang = config_manager.get("language")
    if lang == "auto" or lang not in LANGUAGES:
        _current_lang = _detect_system_language()
    else:
        _current_lang = lang
    logger.info(f"Language initialized: {_current_lang}")


def _detect_system_language():
    """Detect system language, return 'zh' if Chinese, else 'en'."""
    try:
        system_locale = locale.getdefaultlocale()[0]  # e.g. 'zh_CN', 'en_US'
        if system_locale and system_locale.startswith("zh"):
            return "zh"
    except Exception:
        pass
    return "en"


def t(key):
    """Translate a string key. Falls back to English, then returns key itself."""
    lang_strings = STRINGS.get(_current_lang, STRINGS["en"])
    return lang_strings.get(key, STRINGS["en"].get(key, key))


def get_language():
    """Get current language code."""
    return _current_lang


def set_language(lang):
    """Set language and persist to config."""
    global _current_lang
    if lang in LANGUAGES or lang == "auto":
        _current_lang = lang if lang != "auto" else _detect_system_language()
        if _config_manager:
            _config_manager.set("language", lang)
        logger.info(f"Language changed to: {_current_lang}")


def get_available_languages():
    """Return dict of available languages {code: display_name}."""
    return LANGUAGES.copy()
