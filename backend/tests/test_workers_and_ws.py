from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from app.services.websocket_manager import WebSocketManager
from app.workers.tasks import DeadLetterTask, dead_letter, enqueue_run


def test_enqueue_run_task() -> None:
    """enqueue_run task returns queued status payload."""
    result = enqueue_run("run-uuid-123")
    assert result == {"run_id": "run-uuid-123", "status": "queued"}


def test_dead_letter_task() -> None:
    """dead_letter task echoes received operator metadata."""
    metadata = dead_letter(
        source_task_id="task-1",
        source_task_name="enqueue_run",
        error_type="RuntimeError",
    )
    assert metadata == {
        "source_task_id": "task-1",
        "source_task_name": "enqueue_run",
        "error_type": "RuntimeError",
    }


def test_dead_letter_task_on_failure_triggers_send_task() -> None:
    """on_failure hook routes exhausted failures to dead_letter queue."""
    task = DeadLetterTask()
    task.name = "app.workers.tasks.enqueue_run"

    with patch("app.workers.tasks.celery_app.send_task") as mock_send_task:
        task.on_failure(
            exc=ValueError("Test Failure"),
            task_id="task-uuid-456",
            args=(),
            kwargs={},
            einfo=None,
        )
        mock_send_task.assert_called_once_with(
            "app.workers.tasks.dead_letter",
            kwargs={
                "source_task_id": "task-uuid-456",
                "source_task_name": "app.workers.tasks.enqueue_run",
                "error_type": "ValueError",
            },
            queue="dead_letter",
        )


@pytest.mark.asyncio
async def test_websocket_manager_connect_broadcast_disconnect() -> None:
    """WebSocketManager registers connections, broadcasts messages, and disconnects."""
    manager = WebSocketManager()
    ws1 = AsyncMock()
    ws2 = AsyncMock()

    await manager.connect("run:run-1", ws1)
    await manager.connect("run:run-1", ws2)

    assert len(manager._connections["run:run-1"]) == 2

    payload: dict[str, object] = {"event": "status_changed", "status": "running"}
    await manager.broadcast("run:run-1", payload)

    ws1.send_json.assert_called_once_with(payload)
    ws2.send_json.assert_called_once_with(payload)

    manager.disconnect("run:run-1", ws1)
    assert len(manager._connections["run:run-1"]) == 1

    manager.disconnect("run:run-1", ws2)
    assert "run:run-1" not in manager._connections
