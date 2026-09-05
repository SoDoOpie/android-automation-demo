"""
Android device automator — demo / entry point.

Run:  python main.py

Adjust DEMO_SPEED in tasks/handlers.py to control simulation speed:
  1.0  → real time   (20 min task takes 20 min)
  0.01 → 100x faster (20 min task takes ~12 sec)  ← default
"""
import logging
from datetime import datetime, timedelta
from uiautomator2 import Device
import tasks.handlers  # side-effect: registers all @register handlers
from tasks.schedule import DailySchedule
from tasks.worker import DeviceWorker

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(message)s",
    datefmt="%H:%M:%S",
)


class MockDevice:
    """Fake Android device for running without a physical device connected."""
    serial = "emulator-5554"


if __name__ == "__main__":
    device = Device('emulator-5554')
    worker = DeviceWorker(device=device, poll_interval=5)

    # ------------------------------------------------------------------ #
    # Build today's schedule.  Add / remove / reorder lines freely.       #
    # ------------------------------------------------------------------ #
    now = datetime.now()
    schedule = DailySchedule(device_id=device.serial)
    # schedule.watch_instagram(duration_minutes=20, at=now + timedelta(seconds=5))
    schedule.open_app(app_name="com.zhiliaoapp.musically", at=now + timedelta(seconds=5))
    for task in schedule.tasks:
        worker.add(task)
    worker.run_forever(stop_when_empty=True)


