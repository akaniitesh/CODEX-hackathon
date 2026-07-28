from __future__ import annotations

from sqlalchemy import select

from app.models.webhook_delivery import WebhookDelivery
from app.repositories.base import BaseRepository


class WebhookDeliveryRepository(BaseRepository[WebhookDelivery]):
    """Persistence operations for webhook idempotency records."""

    model = WebhookDelivery

    async def get_by_delivery_id(self, delivery_id: str) -> WebhookDelivery | None:
        """Fetch a delivery ledger record by GitHub delivery id."""
        result = await self.session.scalars(
            select(WebhookDelivery).where(WebhookDelivery.delivery_id == delivery_id)
        )
        return result.first()

