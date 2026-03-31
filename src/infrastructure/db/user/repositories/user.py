from dataclasses import dataclass
from typing import final
from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.user.dtos.user import UpdateUserDTO, VerifyPasswordDTO
from src.application.user.ports.repository import UserRepositoryProtocol
from src.domain.user.entities.user import User
from src.infrastructure.db.exceptions import ConflictRepositoryError, RepositoryError
from src.infrastructure.db.models import UserModel
from src.infrastructure.db.user.mappers.user import UserDBMapper
from src.logger import logger


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class UserRepositorySQLAlchemy(UserRepositoryProtocol):
    session: AsyncSession
    mapper: UserDBMapper

    async def create_user(self, user: User) -> UUID | None:
        try:
            stmt = select(UserModel).where(
                UserModel.user_uuid == user.user_uuid
            )
            result = await self.session.execute(stmt)
            model = result.scalar_one_or_none()
            if model:
                return None
            model = self.mapper.to_model(user)
            self.session.add(model)
            await self.session.commit()
            return user.user_uuid
        except IntegrityError as e:
            logger.critical(
                f"Conflict while saving user '{user.user_uuid}': {e}")
            raise ConflictRepositoryError(
                f"Conflict while saving user '{user.user_uuid}': {e}"
            ) from e
        except SQLAlchemyError as e:
            logger.critical(f"Failed to save user '{user.user_uuid}': {e}")
            raise RepositoryError(
                f"Failed to save user '{user.user_uuid}': {e}"
            ) from e

    async def delete_user(self, user_uuid: str) -> None:
        try:
            stmt = delete(UserModel).where(
                UserModel.user_uuid == user_uuid)
            await self.session.execute(stmt)
            await self.session.commit()
        except SQLAlchemyError as e:
            logger.critical(f"Failed to delete user '{user_uuid}': {e}")
            raise RepositoryError(
                f"Failed to delete user '{user_uuid}': {e}"
            ) from e

    async def update_user(self, user: UpdateUserDTO) -> UUID | None:
        try:
            stmt = select(UserModel).where(
                UserModel.user_uuid == user.user_uuid
            )
            result = await self.session.execute(stmt)
            model = result.scalar_one_or_none()
            if model:
                return None
            self.mapper.update_model_from_dto(model, user)
            await self.session.commit()
            return user.user_uuid
        except IntegrityError as e:
            logger.critical(
                f"Conflict while update user '{user.user_uuid}': {e}")
            raise ConflictRepositoryError(
                f"Conflict while update user '{user.user_uuid}': {e}"
            ) from e
        except SQLAlchemyError as e:
            logger.critical(f"Failed to update user '{user.user_uuid}': {e}")
            raise RepositoryError(
                f"Failed to update user '{user.user_uuid}': {e}"
            ) from e

    async def change_password(self, user_uuid: str, new_password: str) -> UUID | None:
        try:
            stmt = select(UserModel).where(
                UserModel.user_uuid == user_uuid
            )
            result = await self.session.execute(stmt)
            model = result.scalar_one_or_none()
            if model:
                return None
            self.mapper.update_password(model, new_password)
            await self.session.commit()
            return UUID(user_uuid)
        except IntegrityError as e:
            logger.critical(
                f"Conflict while update password user '{user_uuid}': {e}")
            raise ConflictRepositoryError(
                f"Conflict while update password user '{user_uuid}': {e}"
            ) from e
        except SQLAlchemyError as e:
            logger.critical(f"Failed to update password user '{user_uuid}': {e}")
            raise RepositoryError(
                f"Failed to update password user '{user_uuid}': {e}"
            ) from e
