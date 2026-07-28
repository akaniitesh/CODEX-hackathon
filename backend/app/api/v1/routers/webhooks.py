from __future__ import annotations

from fastapi import APIRouter, Depends, Header, Request

from app.api.dependencies import get_webhook_service
from app.core.config import Settings, get_settings
from app.core.security import verify_github_signature
from app.schemas.webhook import WebhookAcceptedResponse
from app.services.webhook_service import GitHubWebhookService

router = APIRouter()


@router.post("/github", response_model=WebhookAcceptedResponse)
async def github_webhook(
    request: Request,
    x_github_event: str = Header(alias="X-GitHub-Event"),
    x_github_delivery: str = Header(alias="X-GitHub-Delivery"),
    x_hub_signature_256: str | None = Header(
        default=None,
        alias="X-Hub-Signature-256",
    ),
    settings: Settings = Depends(get_settings),
    service: GitHubWebhookService = Depends(get_webhook_service),
) -> WebhookAcceptedResponse:
    """Verify and process a GitHub webhook delivery."""
    body = await request.body()
    verify_github_signature(body, x_hub_signature_256, settings)
    return await service.handle(body, x_github_event, x_github_delivery)

