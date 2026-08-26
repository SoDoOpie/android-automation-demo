"""Real uiautomator2 implementations for home screen interactions."""
from __future__ import annotations


def open_app(device, app_name: str) -> bool:
    """Open an app by name or package. Returns True on success."""
    try:
        device.app_start(app_name)
        return True
    except Exception:
        pass
    try:
        device(text=app_name).click()
        return True
    except Exception:
        pass
    return False
