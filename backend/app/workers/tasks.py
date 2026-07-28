from __future__ import annotations

from celery import Task

from app.workers.celery_app import celery_app


class DeadLetterTask(Task):  # type: ignore[misc]
    """Task base that sends exhausted failures to a dead-letter queue."""

    autoretry_for = (Exception,)
    max_retries = 3
    retry_backoff = True
    retry_jitter = True

    def on_failure(
        self,
        exc: BaseException,
        task_id: str,
        args: tuple[object, ...],
        kwargs: dict[str, object],
        einfo: object,
    ) -> None:
        """Publish exhausted failures without exposing sensitive payloads."""
        celery_app.send_task(
            "app.workers.tasks.dead_letter",
            kwargs={
                "source_task_id": task_id,
                "source_task_name": self.name,
                "error_type": type(exc).__name__,
            },
            queue="dead_letter",
        )


@celery_app.task(bind=True, base=DeadLetterTask, name="app.workers.tasks.enqueue_run")  # type: ignore[untyped-decorator]
def enqueue_run(self: DeadLetterTask, run_id: str) -> dict[str, str]:
    """Queue placeholder for Phase 3/4 orchestration entrypoint."""
    return {"run_id": run_id, "status": "queued"}


@celery_app.task(name="app.workers.tasks.dead_letter")  # type: ignore[untyped-decorator]
def dead_letter(**kwargs: object) -> dict[str, object]:
    """Record dead-lettered task metadata for operators."""
    return kwargs

