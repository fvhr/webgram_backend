from dataclasses import dataclass
from uuid import UUID

from src.application.user.ports.auth import AuthentificationProtocol
from src.settings import Settings


@dataclass
class AuthentificationAuthX(AuthentificationProtocol):
    _settings: Settings

    def get_user_uuid_access_token(self) -> UUID | None:
        user: dict = self._settings.SECURITY.access_token_required
        user_uuid = getattr(user, "sub", None)
        return user_uuid

    def get_user_uuid_refresh_token(self) -> UUID | None:
        user: dict = self._settings.SECURITY.refresh_token_required
        user_uuid = getattr(user, "sub", None)
        return user_uuid

    def get_access_token(self, user_uuid: str) -> str:
        return self._settings.SECURITY.create_access_token(
            user_uuid=user_uuid,
        )

    def get_refresh_token(self, user_uuid: str) -> str:
        return self._settings.SECURITY.create_refresh_token(
            user_uuid=user_uuid,
        )
