from __future__ import annotations

from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect

from app.core.config import Settings, get_settings
from app.core.errors import ApiError
from app.core.security import ROLE_ORDER, Role, decode_access_token
from app.services.websocket_manager import websocket_manager

router = APIRouter()


@router.websocket("/runs/{run_id}")
async def run_updates(
    websocket: WebSocket,
    run_id: str,
    token: str | None = Query(default=None),
    settings: Settings = Depends(get_settings),
) -> None:
    """Subscribe to realtime updates for a run."""
    if not await _authorize_websocket(websocket, token, settings):
        return
    channel = f"run:{run_id}"
    await websocket_manager.connect(channel, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        websocket_manager.disconnect(channel, websocket)


async def _authorize_websocket(
    websocket: WebSocket,
    token: str | None,
    settings: Settings,
) -> bool:
    """Authorize websocket clients before accepting the connection."""
    bearer_token = token or _authorization_header_token(websocket)
    if bearer_token is None:
        await websocket.close(code=1008)
        return False
    try:
        claims = decode_access_token(bearer_token, settings)
        role = Role(claims.get("role", Role.VIEWER))
    except (ApiError, ValueError):
        await websocket.close(code=1008)
        return False
    if ROLE_ORDER[role] < ROLE_ORDER[Role.VIEWER]:
        await websocket.close(code=1008)
        return False
    return True


def _authorization_header_token(websocket: WebSocket) -> str | None:
    """Extract a bearer token from websocket headers when clients can send one."""
    authorization = websocket.headers.get("authorization")
    if not authorization:
        return None
    scheme, _, value = authorization.partition(" ")
    if scheme.lower() != "bearer" or not value:
        return None
    return value
