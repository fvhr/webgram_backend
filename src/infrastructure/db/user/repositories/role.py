from dataclasses import dataclass
from typing import final

from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.user.ports.repository import RoleRepositoryProtocol
from src.domain.user.entities.role import Role
from src.infrastructure.db.exceptions import RepositoryError, ConflictRepositoryError
from src.infrastructure.db.models import RoleModel
from src.infrastructure.db.user.mappers.role import RoleDBMapper
from src.logger import logger


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class RoleRepositorySQLAlchemy(RoleRepositoryProtocol):
    session: AsyncSession
    mapper: RoleDBMapper

    async def get_role(self, role_uuid: str) -> Role | None:
        try:
            stmt = select(RoleModel).where(RoleModel.role_uuid == role_uuid)
            result = await self.session.execute(stmt)
            role_model = result.scalar_one_or_none()
            if role_model is None:
                return None
            return self.mapper.to_entity(role_model)
        except SQLAlchemyError as e:
            logger.critical(f"Failed to retrieve role by role_uuid '{role_uuid}': {e}")
            raise RepositoryError(
                f"Failed to retrieve role by role_uuid '{role_uuid}': {e}"
            ) from e

    async def get_role_by_role_name(self, role_name: str) -> Role | None:
        try:
            stmt = select(RoleModel).where(RoleModel.role_name == role_name)
            result = await self.session.execute(stmt)
            role_model = result.scalar_one_or_none()
            if role_model is None:
                return None
            return self.mapper.to_entity(role_model)
        except SQLAlchemyError as e:
            logger.critical(f"Failed to retrieve role by role_name '{role_name}': {e}")
            raise RepositoryError(
                f"Failed to retrieve role by role_name '{role_name}': {e}"
            ) from e

    async def get_roles(self) -> list[Role]:
        try:
            stmt = select(RoleModel)
            result = await self.session.execute(stmt)
            role_models = result.scalars().all()
            return [self.mapper.to_entity(role_model) for role_model in role_models]
        except SQLAlchemyError as e:
            logger.critical(f'Failed to retrieve role: {e}')
            raise RepositoryError(
                f'Failed to retrieve role: {e}'
            ) from e

    async def create_role(self, role: Role) -> Role | None:
        try:
            stmt = select(RoleModel).where(
                RoleModel.role_uuid == role.role_uuid
            )
            result = await self.session.execute(stmt)
            model = result.scalar_one_or_none()
            if model:
                return None
            model = self.mapper.to_model(role)
            self.session.add(model)
            await self.session.commit()
            return role
        except IntegrityError as e:
            logger.critical(f"Conflict while saving role '{role.role_uuid}': {e}")
            raise ConflictRepositoryError(
                f"Conflict while saving role '{role.role_uuid}': {e}"
            ) from e
        except SQLAlchemyError as e:
            logger.critical(f"Failed to save role '{role.role_uuid}': {e}")
            raise RepositoryError(
                f"Failed to save role '{role.role_uuid}': {e}"
            ) from e

    async def update_role(self, role: Role) -> Role | None:
        try:
            stmt = select(RoleModel).where(
                RoleModel.role_uuid == role.role_uuid
            )
            result = await self.session.execute(stmt)
            model = result.scalar_one_or_none()

            if not model:
                return None
            self.mapper.update_model_from_entity(model, role)
            await self.session.commit()
            return role
        except IntegrityError as e:
            logger.critical(f"Conflict while saving role '{role.role_uuid}': {e}")
            raise ConflictRepositoryError(
                f"Conflict while saving role '{role.role_uuid}': {e}"
            ) from e
        except SQLAlchemyError as e:
            logger.critical(f"Failed to save role '{role.role_uuid}': {e}")
            raise RepositoryError(
                f"Failed to save role '{role.role_uuid}': {e}"
            ) from e

    async def delete_role(self, role_uuid: str) -> None:
        try:
            stmt = delete(RoleModel).where(RoleModel.role_uuid == role_uuid)
            await self.session.execute(stmt)
            await self.session.commit()
        except SQLAlchemyError as e:
            logger.critical(f"Failed to delete role '{role_uuid}': {e}")
            raise RepositoryError(
                f"Failed to delete role '{role_uuid}': {e}"
            ) from e
