from __future__ import annotations

from datetime import datetime
from typing import Callable

from tasks.task import ScheduledTask


class DailySchedule:
    """Fluent builder for a device daily task schedule.

    Usage:
        schedule = DailySchedule("emulator-5554")
        schedule.watch_tiktok(20, at=now + timedelta(hours=1))
        schedule.upload_tiktok("videos/clip.mp4", at=now + timedelta(hours=2))

        for task in schedule.tasks:
            worker.add(task)
    """

    def __init__(self, device_id: str):
        self.device_id = device_id
        self.tasks: list[ScheduledTask] = []

    def _add(self, task_id: str, task_type: str, payload: dict, at: datetime) -> ScheduledTask:
        task = ScheduledTask(task_id=task_id, task_type=task_type, payload=payload, run_at=at)
        self.tasks.append(task)
        return task

    # ------------------------------------------------------------------
    # Social media
    # ------------------------------------------------------------------

    def watch_tiktok(self, duration_minutes: int, at: datetime) -> ScheduledTask:
        return self._add(
            f"watch_tiktok_{duration_minutes}min",
            "watch_tiktok",
            {"duration_seconds": duration_minutes * 60},
            at,
        )

    def upload_tiktok(self, video_path: str, at: datetime) -> ScheduledTask:
        return self._add(
            f"upload_tiktok_{video_path.replace('/', '_')}",
            "upload_tiktok",
            {"video_path": video_path},
            at,
        )

    def watch_youtube(self, duration_minutes: int, at: datetime) -> ScheduledTask:
        return self._add(
            f"watch_youtube_{duration_minutes}min",
            "watch_youtube",
            {"duration_seconds": duration_minutes * 60},
            at,
        )

    def watch_instagram(self, duration_minutes: int, at: datetime) -> ScheduledTask:
        return self._add(
            f"watch_instagram_{duration_minutes}min",
            "watch_instagram",
            {"duration_seconds": duration_minutes * 60},
            at,
        )

    # ------------------------------------------------------------------
    # Apps
    # ------------------------------------------------------------------

    def download_app(self, app_name: str, at: datetime) -> ScheduledTask:
        return self._add(
            f"download_{app_name.lower().replace(' ', '_')}",
            "download_app",
            {"app_name": app_name},
            at,
        )

    def open_app(self, app_name: str, at: datetime) -> ScheduledTask:
        return self._add(
            f"open_{app_name.lower().replace(' ', '_')}",
            "open_app",
            {"app_name": app_name},
            at,
        )

    # ------------------------------------------------------------------
    # Custom / generic
    # ------------------------------------------------------------------

    def run(self, task_id: str, fn: Callable, at: datetime) -> ScheduledTask:
        """Schedule any callable as a task: fn(device) -> None."""
        task = ScheduledTask.from_callable(task_id=task_id, fn=fn, run_at=at)
        self.tasks.append(task)
        return task

    def custom(self, task_id: str, task_type: str, payload: dict, at: datetime) -> ScheduledTask:
        return self._add(task_id, task_type, payload, at)
