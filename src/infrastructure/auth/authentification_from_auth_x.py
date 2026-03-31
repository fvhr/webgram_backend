from dataclasses import dataclass
from uuid import UUID

from src.application.user.ports.auth import AuthentificationProtocol
from src.settings import Settings


@dataclass
class AuthentificationAuthX(AuthentificationProtocol):
    _settings: Settings

    def get_user_uuid_by_token(self, token: str | None) -> UUID | None:
        if token is None:
            return None
        try:
            payload = self._settings.SECURITY._decode_token(token)
            return UUID(payload.sub)
        except Exception:
            return None

    def get_access_token(self, user_uuid: str) -> str:
        return self._settings.SECURITY.create_access_token(
            uid=user_uuid,
        )

    def get_refresh_token(self, user_uuid: str) -> str:
        return self._settings.SECURITY.create_refresh_token(
            uid=user_uuid,
        )
