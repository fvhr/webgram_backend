import uuid

from fastapi import WebSocket, WebSocketDisconnect

from src.domain.enums import WebsocketConnectionTypes


class ConnectionManager:
    def __init__(self) -> None:
        self.connections = {}

    async def connect(self, websocket: WebSocket, connection_type: WebsocketConnectionTypes) -> uuid.UUID:
        await websocket.accept()
        personal_uuid = uuid.uuid4()
        self.connections[personal_uuid] = {'websocket': websocket, 'connection_type': connection_type}
        return personal_uuid

    async def broadcast(self, message: dict, connection_type: WebsocketConnectionTypes) -> None:
        for websocket in self.connections.values():
            if websocket.get('connection_type') == connection_type:
                websocket = websocket.get('websocket')
                if websocket:
                    try:
                        await websocket.send_json(message)
                    except (RuntimeError, WebSocketDisconnect):
                        pass

    async def disconnect(self, personal_uuid: uuid.UUID):
        if personal_uuid in self.connections:
            self.connections.pop(personal_uuid)
