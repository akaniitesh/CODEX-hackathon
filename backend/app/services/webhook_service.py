from __future__ import annotations

import json
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import ApiError
from app.models.run import Run
from app.models.webhook_delivery import WebhookDelivery
from app.repositories.repository_repository import RepositoryRepository
from app.repositories.run_repository import RunRepository
from app.repositories.webhook_repository import WebhookDeliveryRepository
from app.schemas.webhook import GitHubWebhookSummary, WebhookAcceptedResponse
from app.workers.tasks import enqueue_run


class GitHubWebhookService:
    """Validate, deduplicate, and enqueue GitHub webhook-triggered runs."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.webhooks = WebhookDeliveryRepository(session)
        self.repositories = RepositoryRepository(session)
        self.runs = RunRepository(session)

    async def handle(
        self,
        body: bytes,
        event_type: str,
        delivery_id: str,
    ) -> WebhookAcceptedResponse:
        """Process an already signature-verified GitHub webhook."""
        if await self.webhooks.get_by_delivery_id(delivery_id):
            return WebhookAcceptedResponse(accepted=True, duplicate=True)

        payload = self._load_payload(body)
        summary = self._summarize_payload(payload, event_type, delivery_id)
        repository = None
        if summary.repository_full_name:
            repository = await self.repositories.get_by_full_name(
                summary.repository_full_name
            )
        if repository is None:
            await self._record_delivery(summary, "ignored")
            await self.session.commit()
            return WebhookAcceptedResponse(accepted=False, duplicate=False)

        duplicate = await self.runs.find_duplicate(
            repository.id,
            summary.commit_sha or "",
            summary.event_type,
            summary.delivery_id,
        )
        if duplicate:
            await self._record_delivery(summary, "duplicate")
            await self.session.commit()
            return WebhookAcceptedResponse(
                accepted=True,
                duplicate=True,
                run_id=duplicate.id,
            )

        run = await self.runs.add(
            Run(
                repository_id=repository.id,
                event_type=summary.event_type,
                commit_sha=summary.commit_sha or "",
                branch=summary.branch,
                webhook_delivery_id=summary.delivery_id,
            )
        )
        await self._record_delivery(summary, "enqueued")
        await self.session.commit()
        enqueue_run.delay(run.id)
        return WebhookAcceptedResponse(accepted=True, duplicate=False, run_id=run.id)

    def _load_payload(self, body: bytes) -> dict[str, Any]:
        """Decode JSON payload after signature verification."""
        try:
            payload = json.loads(body)
        except json.JSONDecodeError as exc:
            raise ApiError("Invalid JSON payload.", 400) from exc
        if not isinstance(payload, dict):
            raise ApiError("Webhook payload must be an object.", 422)
        return payload

    def _summarize_payload(
        self,
        payload: dict[str, Any],
        event_type: str,
        delivery_id: str,
    ) -> GitHubWebhookSummary:
        """Extract a compact trusted summary from a GitHub webhook payload."""
        repository = payload.get("repository") or {}
        head_commit = payload.get("head_commit") or {}
        ref = payload.get("ref")
        branch = ref.removeprefix("refs/heads/") if isinstance(ref, str) else None
        return GitHubWebhookSummary(
            delivery_id=delivery_id,
            event_type=event_type,
            repository_full_name=repository.get("full_name"),
            commit_sha=head_commit.get("id") or payload.get("after"),
            branch=branch,
        )

    async def _record_delivery(
        self,
        summary: GitHubWebhookSummary,
        status: str,
    ) -> None:
        """Persist the idempotency record for a webhook delivery."""
        await self.webhooks.add(
            WebhookDelivery(
                delivery_id=summary.delivery_id,
                event_type=summary.event_type,
                repository_full_name=summary.repository_full_name,
                commit_sha=summary.commit_sha,
                status=status,
                payload_summary=summary.model_dump(),
            )
        )

