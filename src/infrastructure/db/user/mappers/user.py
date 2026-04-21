from dataclasses import dataclass
from typing import final

from src.application.user.dtos.user import OutboundUserDTO, UpdateUserDTO, VerifyPasswordDTO
from src.domain.services.password_hash_service import PasswordHashService
from src.domain.user.entities.user import User
from src.infrastructure.db.agent.mappers.agent import AgentDBMapper
from src.infrastructure.db.models import UserModel
from src.infrastructure.db.user.mappers.role import RoleDBMapper


@final
@dataclass(frozen=True, slots=True)
class UserDBMapper:
    _role_mapper: RoleDBMapper
    _agent_mapper: AgentDBMapper
    _password_hash: PasswordHashService

    def to_model(self, entity: User) -> UserModel:
        return UserModel(
            user_uuid=entity.user_uuid,
            user_name=entity.user_name.value,
            user_password=self._password_hash.hash_password(entity.user_password.value),
            role_uuid=entity.role_uuid,
        )

    def to_dto(self, model: UserModel) -> OutboundUserDTO:
        role = self._role_mapper.to_dto(model.role)
        agent = self._agent_mapper.to_dto(model.agent) if model.agent else None
        return OutboundUserDTO(
            user_uuid=model.user_uuid,
            user_name=model.user_name,
            role=role,
            agent=agent,
        )

    @staticmethod
    def update_model_from_dto(
            model: UserModel, dto: UpdateUserDTO
    ) -> None:
        model.user_uuid = dto.user_uuid
        model.user_name = dto.user_name
        model.role_uuid = dto.role_uuid

    def update_password(self, model: UserModel, new_password: str) -> None:
        model.user_password = self._password_hash.hash_password(new_password)

    @staticmethod
    def to_verify_dto(model: UserModel) -> VerifyPasswordDTO:
        return VerifyPasswordDTO(
            user_uuid=model.user_uuid,
            password_hash=model.user_password,
        )
