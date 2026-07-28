from __future__ import annotations

from celery import Celery
from kombu import Exchange, Queue

from app.core.config import settings

celery_app = Celery(
    "autonomous_se",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.workers.tasks"],
)

celery_app.conf.update(
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    task_routes={"app.workers.tasks.*": {"queue": "runs"}},
    task_queues=(
        Queue("runs", Exchange("runs"), routing_key="runs"),
        Queue("dead_letter", Exchange("dead_letter"), routing_key="dead_letter"),
    ),
    task_default_queue="runs",
    broker_connection_retry_on_startup=True,
)

