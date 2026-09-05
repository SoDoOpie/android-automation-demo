"""
Stub task handlers – each simulates real work with time.sleep.

To add a new task type:
  1. Add @register("your_task_type") decorated function here.
  2. Add a factory method in task_factory.py.
  3. Optionally add a convenience method in schedule.py.

DEMO_SPEED controls how fast simulated time passes:
  1.0  → real time (20 min task takes 20 min)
  0.01 → 100x faster (20 min task takes ~12 sec)
  0.0  → instant (useful in unit tests)
"""
from __future__ import annotations

import logging
import time
import random
from tasks.registry import register
from uiautomator2 import Device

logger = logging.getLogger(__name__)

DEMO_SPEED: float = 0.01


def _sleep(seconds: float, description: str) -> None:
    actual = seconds * DEMO_SPEED
    logger.info("  ↳ %s  (simulated %ds → real %.2fs)", description, int(seconds), actual)
    if actual > 0:
        time.sleep(actual)


# ---------------------------------------------------------------------------
# Social media
# ---------------------------------------------------------------------------

@register("watch_tiktok")
def watch_tiktok(device: Device, payload: dict) -> None:
    duration = payload.get("duration_seconds", 1200)
    duration = duration * DEMO_SPEED
    end_time = time.time() + duration
    while time.time() < end_time:
        ...
    logger.info("Watched TikTok")

@register("upload_tiktok")
def upload_tiktok(device: Device, payload: dict) -> None:
    video = payload.get("video_path", "video.mp4")
    _sleep(45, f"Uploading TikTok video: {video}")


@register("watch_youtube")
def watch_youtube(device: Device, payload: dict) -> None:
    duration = payload.get("duration_seconds", 600)
    _sleep(duration, f"Watching YouTube for {duration // 60} min")


@register("watch_instagram")
def watch_instagram(device: Device, payload: dict) -> None:
    duration = payload.get("duration_seconds", 600)
    _sleep(duration, f"Browsing Instagram Reels for {duration // 60} min")


# ---------------------------------------------------------------------------
# Play Store
# ---------------------------------------------------------------------------

@register("download_app")
def download_app(device: Device, payload: dict) -> None:
    #_sleep(60, f"Downloading '{payload.get('app_name', '?')}' from Play Store")
    app_name = payload.get('app_name', '?')
    if app_name != "?":
        _sleep(60, f"Mock downloading '{app_name}' from Play Store")
    device.press("home")
    device.swipe_ext("up", scale=0.8)
    play_store_icon = device(text="Play Store")
    if play_store_icon.exists:
        play_store_icon.click()
        _sleep(5, "Waiting for Play Store to open")
    else:
        logger.warning("  ↳ Play Store icon not found on the home screen.")
    if device(text="Sign in").exists:
        logger.info("  ↳ Play Store requires sign-in.")

@register("open_app")
def open_app(device: Device, payload: dict) -> None:
    app_name = payload.get('app_name')
    if not app_name:
        logger.error("No app name was provided")
        raise Exception("No app name was provided")

    device.app_start(app_name, wait=True)
    #time.sleep(random.uniform(10, 20)) # wait for a bit

@register("app_session")
def app_session(device: Device, payload: dict) -> None:
    app = payload.get("app_name", "?")
    duration = payload.get("duration_seconds", 300)
    _sleep(duration, f"App session: {app} for {duration // 60} min")


# ---------------------------------------------------------------------------
# Internal / test
# ---------------------------------------------------------------------------

@register("demo")
def demo(device: Device, payload: dict) -> None:
    """Used by unit tests via DummyDevice.do_action."""
    value = payload.get("value")
    if hasattr(device, "do_action"):
        device.do_action(value)
