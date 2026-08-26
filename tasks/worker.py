from __future__ import annotations

import logging
import time
from datetime import datetime
from typing import Optional

from tasks.queue import TaskQueue
from tasks.task import ScheduledTask

logger = logging.getLogger(__name__)


class DeviceWorker:
    """Runs scheduled tasks on a device in chronological order."""

    def __init__(self, device, poll_interval: int = 5):
        self.device = device
        self.poll_interval = poll_interval
        self.queue = TaskQueue()
        self.running = False

    def add(self, task: ScheduledTask) -> ScheduledTask:
        self.queue.push(task)
        return task

    def run_forever(self, stop_when_empty: bool = False) -> None:
        self.running = True
        device_id = getattr(self.device, "serial", repr(self.device))
        logger.info("Worker started  [device=%s  poll=%ss]", device_id, self.poll_interval)

        while self.running:
            self.process_due()

            next_info = self.queue.peek()
            if next_info is None:
                if stop_when_empty:
                    logger.info("Queue empty — worker done.")
                    break
                time.sleep(self.poll_interval)
                continue

            run_at, next_task = next_info
            wait = (run_at - datetime.now()).total_seconds()
            if wait > 0:
                sleep_for = min(wait, self.poll_interval)
                logger.info("Next: '%s' in %.0fs — sleeping %.0fs", next_task.task_id, wait, sleep_for)
                time.sleep(sleep_for)

        self.running = False

    def stop(self) -> None:
        self.running = False

    def process_due(self, now: Optional[datetime] = None) -> list[ScheduledTask]:
        """Execute all tasks due by `now`. Returns the list of processed tasks."""
        processed = []
        for task in self.queue.pop_due(now):
            task.status = "running"
            task.started_at = datetime.now()
            logger.info("[START] %-40s type=%s", task.task_id, task.task_type)

            try:
                task.execute(self.device)
                task.status = "done"
                task.finished_at = datetime.now()
                elapsed = (task.finished_at - task.started_at).total_seconds()
                logger.info("[DONE]  %-40s %.2fs", task.task_id, elapsed)

            except Exception as exc:
                task.error = str(exc)
                if task.retry_count < task.max_retries:
                    task.schedule_retry(delay_seconds=60)
                    self.queue.push(task)
                    logger.warning("[RETRY] %s  attempt=%d  error=%s", task.task_id, task.retry_count, exc)
                else:
                    task.status = "failed"
                    task.finished_at = datetime.now()
                    logger.error("[FAIL]  %s  error=%s", task.task_id, exc)

            processed.append(task)
        return processed

