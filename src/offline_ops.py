"""Offline operating system automation handlers.

Supports Windows, macOS, and Linux application launching with graceful fallbacks.
"""

import platform
import subprocess
import shutil

# Attempt to import AppOpener on Windows environments
try:
    from AppOpener import open as app_open
except ImportError:
    app_open = None


def _launch_desktop_app(app_name: str) -> tuple[bool, str]:
    """Launches a desktop application in a cross-platform manner.

    Returns:
        tuple[bool, str]: (Success status, descriptive status message)
    """
    system = platform.system()

    # 1. Windows support
    if system == "Windows":
        if app_open is not None:
            try:
                app_open(app_name)
                return True, f"Opening {app_name} via AppOpener"
            except Exception as e:
                pass
        
        # Windows URI/protocol fallback
        win_protocols = {
            "clock": "start ms-clock:",
            "calendar": "start outlookcal:",
            "settings": "start ms-settings:",
            "media player": "start wmplayer",
        }
        cmd = win_protocols.get(app_name.lower())
        if cmd:
            try:
                subprocess.Popen(cmd, shell=True)
                return True, f"Opening {app_name}"
            except Exception as e:
                return False, f"Failed to open {app_name}: {e}"
        return False, f"Unsupported Windows app: {app_name}"

    # 2. macOS support
    elif system == "Darwin":
        mac_apps = {
            "clock": "Clock",
            "calendar": "Calendar",
            "settings": "System Settings",
            "media player": "Music",
        }
        target_app = mac_apps.get(app_name.lower(), app_name.title())
        try:
            # Check if System Settings or System Preferences
            if app_name.lower() == "settings":
                # Try System Settings (macOS 13+), fallback to System Preferences
                res = subprocess.run(["open", "-a", "System Settings"], capture_output=True)
                if res.returncode != 0:
                    subprocess.run(["open", "-a", "System Preferences"])
                return True, "Opening System Settings"

            subprocess.Popen(["open", "-a", target_app])
            return True, f"Opening {target_app}"
        except Exception as e:
            return False, f"Failed to open {app_name} on macOS: {e}"

    # 3. Linux support
    elif system == "Linux":
        linux_apps = {
            "clock": ["gnome-clocks", "kclock"],
            "calendar": ["gnome-calendar", "korganizer"],
            "settings": ["gnome-control-center", "systemsettings"],
            "media player": ["vlc", "rhythmbox", "totem"],
        }
        candidates = linux_apps.get(app_name.lower(), [app_name.lower()])
        for bin_name in candidates:
            if shutil.which(bin_name):
                try:
                    subprocess.Popen([bin_name])
                    return True, f"Opening {bin_name}"
                except Exception as e:
                    return False, f"Failed to launch {bin_name}: {e}"
        return False, f"No installed application found for {app_name} on Linux."

    return False, f"Unsupported operating system: {system}"


def open_clock() -> tuple[bool, str]:
    return _launch_desktop_app("clock")


def open_calendar() -> tuple[bool, str]:
    return _launch_desktop_app("calendar")


def open_settings() -> tuple[bool, str]:
    return _launch_desktop_app("settings")


def open_media_player() -> tuple[bool, str]:
    return _launch_desktop_app("media player")
