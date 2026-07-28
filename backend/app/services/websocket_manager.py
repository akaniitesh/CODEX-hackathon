from __future__ import annotations

from collections import defaultdict

from fastapi import WebSocket


class WebSocketManager:
    """In-process WebSocket connection manager for realtime updates."""

    def __init__(self) -> None:
        self._connections: dict[str, set[WebSocket]] = defaultdict(set)

    async def connect(self, channel: str, websocket: WebSocket) -> None:
        """Accept and register a WebSocket connection on a channel."""
        await websocket.accept()
        self._connections[channel].add(websocket)

    def disconnect(self, channel: str, websocket: WebSocket) -> None:
        """Remove a WebSocket connection from a channel."""
        self._connections[channel].discard(websocket)
        if not self._connections[channel]:
            del self._connections[channel]

    async def broadcast(self, channel: str, payload: dict[str, object]) -> None:
        """Broadcast a JSON payload to every connection on a channel."""
        stale: list[WebSocket] = []
        for websocket in self._connections.get(channel, set()):
            try:
                await websocket.send_json(payload)
            except RuntimeError:
                stale.append(websocket)
        for websocket in stale:
            self.disconnect(channel, websocket)


websocket_manager = WebSocketManager()

