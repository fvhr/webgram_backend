import uuid

from fastapi import WebSocket, WebSocketDisconnect

from src.domain.enums import WebsocketRoles


class ConnectionManager:
    def __init__(self) -> None:
        self.connections = {}

    async def connect(self, websocket: WebSocket, ws_role: WebsocketRoles,
                      agent_uuid: str | None = None) -> str:
        await websocket.accept()
        personal_uuid = str(uuid.uuid4())
        self.connections[personal_uuid] = {'websocket': websocket, 'ws_role': ws_role, 'agent_uuid': agent_uuid}
        return personal_uuid

    async def broadcast_to_role(self, message: dict, ws_role: WebsocketRoles) -> None:
        for websocket in self.connections.values():
            if websocket.get('ws_role') == ws_role:
                websocket = websocket.get('websocket')
                if websocket:
                    try:
                        await websocket.send_json(message)
                    except (RuntimeError, WebSocketDisconnect):
                        pass

    async def personal_to_agent(self, message: dict, agent_uuid: str) -> None:
        for websocket in self.connections.values():
            if websocket.get('agent_uuid') == agent_uuid:
                websocket = websocket.get('websocket')
                if websocket:
                    try:
                        await websocket.send_json(message)
                    except (RuntimeError, WebSocketDisconnect):
                        pass

    async def upgrade_agent_socket(self, agent_uuid: str) -> bool:
        upgrade_role = False
        for websocket in self.connections.values():
            if websocket.get('agent_uuid') == agent_uuid:
                websocket['ws_role'] = WebsocketRoles.ADMIN
                upgrade_role = True
        return upgrade_role

    async def disconnect(self, personal_uuid: str):
        if personal_uuid in self.connections:
            self.connections.pop(personal_uuid)
