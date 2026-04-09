import uuid

from fastapi import WebSocket, WebSocketDisconnect


class ConnectionManager:
    def __init__(self) -> None:
        self.connections = {}

    async def connect(self, websocket: WebSocket) -> uuid.UUID:
        await websocket.accept()
        personal_uuid = uuid.uuid4()
        self.connections[personal_uuid] = websocket
        return personal_uuid

    async def broadcast(self, message: dict) -> None:
        for websocket in self.connections.values():
            try:
                await websocket.send_json(message)
            except (RuntimeError, WebSocketDisconnect):
                pass

    async def disconnect(self, personal_uuid: uuid.UUID):
        if personal_uuid in self.connections:
            self.connections.pop(personal_uuid)
