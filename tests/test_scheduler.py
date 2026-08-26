from datetime import datetime, timedelta

import tasks.handlers  # registers all handlers via @register
from tasks import handlers as _h

from tasks.task import ScheduledTask
from tasks.queue import TaskQueue
from tasks.worker import DeviceWorker

# Run tasks instantly during tests
_h.DEMO_SPEED = 0.0


class DummyDevice:
    def __init__(self):
        self.calls: list = []

    def do_action(self, value):
        self.calls.append(value)


# ------------------------------------------------------------------
# TaskQueue
# ------------------------------------------------------------------

def test_queue_returns_only_due_tasks():
    q = TaskQueue()
    now = datetime(2026, 1, 1, 9, 0, 0)

    q.push(ScheduledTask("t1", "demo", {"value": "a"}, now - timedelta(minutes=1)))
    q.push(ScheduledTask("t2", "demo", {"value": "b"}, now + timedelta(minutes=5)))

    due = q.pop_due(now)

    assert [t.task_id for t in due] == ["t1"]


def test_queue_peek_does_not_remove():
    q = TaskQueue()
    now = datetime(2026, 1, 1, 9, 0, 0)
    q.push(ScheduledTask("t1", "demo", {"value": "a"}, now))

    q.peek()
    assert not q.is_empty()


# ------------------------------------------------------------------
# DeviceWorker
# ------------------------------------------------------------------

def test_worker_runs_only_due_tasks():
    device = DummyDevice()
    worker = DeviceWorker(device=device)
    now = datetime(2026, 1, 1, 9, 0, 0)

    worker.queue.push(ScheduledTask("t1", "demo", {"value": "one"}, now))
    worker.queue.push(ScheduledTask("t2", "demo", {"value": "two"}, now + timedelta(minutes=5)))

    worker.process_due(now)

    assert device.calls == ["one"]


def test_worker_processes_app_session():
    device = DummyDevice()
    worker = DeviceWorker(device=device)
    now = datetime(2026, 1, 1, 9, 0, 0)

    worker.add(ScheduledTask(
        task_id="tiktok_session",
        task_type="app_session",
        payload={"app_name": "TikTok", "duration_seconds": 1},
        run_at=now,
    ))

    processed = worker.process_due(now)

    assert processed[0].status == "done"
    assert processed[0].task_id == "tiktok_session"


def test_worker_marks_task_failed_after_max_retries():
    device = DummyDevice()
    worker = DeviceWorker(device=device)
    now = datetime(2026, 1, 1, 9, 0, 0)

    task = ScheduledTask("bad_task", "nonexistent_type", {}, now, max_retries=0)
    worker.add(task)
    worker.process_due(now)

    assert task.status == "failed"
    assert task.error is not None
