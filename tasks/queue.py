from __future__ import annotations

from datetime import datetime
from queue import PriorityQueue
from typing import Optional, Tuple

from tasks.task import ScheduledTask


class TaskQueue:
    """Priority queue ordered by task.run_at (earliest first)."""

    def __init__(self):
        self._q: PriorityQueue = PriorityQueue()

    def push(self, task: ScheduledTask) -> None:
        self._q.put((task.run_at, task.task_id, task))

    def pop_due(self, now: Optional[datetime] = None) -> list[ScheduledTask]:
        """Remove and return all tasks whose run_at <= now, in order."""
        if now is None:
            now = datetime.now()
        due: list[ScheduledTask] = []
        while not self._q.empty():
            run_at, _, task = self._q.queue[0]
            if run_at > now:
                break
            self._q.get()
            due.append(task)
        return due

    def peek(self) -> Optional[Tuple[datetime, ScheduledTask]]:
        """Return (run_at, task) for the next task without removing it."""
        if self._q.empty():
            return None
        run_at, _, task = self._q.queue[0]
        return run_at, task

    def is_empty(self) -> bool:
        return self._q.empty()
