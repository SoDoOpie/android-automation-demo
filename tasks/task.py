from __future__ import annotations

from datetime import datetime, timedelta
from typing import Callable, Optional


class ScheduledTask:
    def __init__(
        self,
        task_id: str,
        task_type: str,
        payload: Optional[dict] = None,
        run_at: Optional[datetime] = None,
        max_retries: int = 3,
    ):
        self.task_id = task_id
        self.task_type = task_type
        self.payload = payload or {}
        self.run_at = run_at or datetime.now()
        self.max_retries = max_retries
        self.retry_count = 0
        self.status = "queued"
        self.error: Optional[str] = None
        self.created_at = datetime.now()
        self.started_at: Optional[datetime] = None
        self.finished_at: Optional[datetime] = None

    def execute(self, device) -> None:
        from tasks.registry import get_handler

        # Inline callable in payload takes priority (allows one-off lambdas)
        inline = self.payload.get("handler") or self.payload.get("action")
        if callable(inline):
            inline(device)
            return

        handler = get_handler(self.task_type)
        if handler is None:
            raise NotImplementedError(
                f"No handler for task type '{self.task_type}'. "
                f"Add @register(\"{self.task_type}\") in tasks/handlers.py."
            )
        handler(device, self.payload)

    def schedule_retry(self, delay_seconds: int = 60) -> None:
        self.retry_count += 1
        self.status = "queued"
        self.run_at = datetime.now() + timedelta(seconds=delay_seconds)
        self.error = None

    @classmethod
    def from_callable(
        cls,
        task_id: str,
        fn: Callable,
        run_at: Optional[datetime] = None,
        max_retries: int = 3,
    ) -> ScheduledTask:
        """Create a task from any callable: fn(device) -> None."""
        return cls(
            task_id=task_id,
            task_type="callable",
            payload={"handler": fn},
            run_at=run_at,
            max_retries=max_retries,
        )
