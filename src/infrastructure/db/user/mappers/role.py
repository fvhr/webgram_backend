from dataclasses import dataclass
from typing import final

from src.application.user.dtos.role import RoleDTO
from src.domain.user.entities.role import Role
from src.domain.user.value_objects.role_name import RoleName
from src.infrastructure.db.models import RoleModel


@final
@dataclass(frozen=True, slots=True)
class RoleDBMapper:
    @staticmethod
    def to_entity(model: RoleModel) -> Role:
        return Role(
            role_uuid=model.role_uuid,
            role_name=RoleName(model.role_name),
        )

    @staticmethod
    def to_model(entity: Role) -> RoleModel:
        return RoleModel(
            role_uuid=entity.role_uuid,
            role_name=entity.role_name.value
        )

    @staticmethod
    def to_dto(model: RoleModel) -> RoleDTO:
        return RoleDTO(
            role_uuid=model.role_uuid,
            role_name=model.role_name,
        )

    @staticmethod
    def update_model_from_entity(
            model: RoleModel, entity: Role
    ) -> None:
        model.role_uuid = entity.role_uuid
        model.role_name = entity.role_name.value
