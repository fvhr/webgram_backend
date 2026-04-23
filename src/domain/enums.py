from enum import StrEnum


class WebsocketMessageTypes(StrEnum):
    AGENT_DATA = 'AGENT_DATA'
    UPDATE_CALLS = 'UPDATE_CALLS'
    CONNECT_CALLS = 'CONNECT_CALLS'
