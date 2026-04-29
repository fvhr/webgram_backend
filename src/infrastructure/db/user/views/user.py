from dataclasses import dataclass
from typing import final

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.application.user.dtos.user import OutboundUserDTO, VerifyPasswordDTO
from src.application.user.ports.repository import ViewUserRepositoryProtocol
from src.infrastructure.db.exceptions import RepositoryError
from src.infrastructure.db.models import UserModel, AgentModel, TierModel
from src.infrastructure.db.user.mappers.user import UserDBMapper
from src.logger import logger


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class ViewUserRepositorySQLAlchemy(ViewUserRepositoryProtocol):
    session: AsyncSession
    mapper: UserDBMapper

    async def get_user(self, user_uuid: str) -> OutboundUserDTO | None:
        try:
            stmt = select(UserModel).where(
                UserModel.user_uuid == user_uuid
            ).options(
                selectinload(UserModel.role),
                selectinload(UserModel.agent).selectinload(AgentModel.tiers).selectinload(TierModel.queue),
                selectinload(UserModel.agent).selectinload(AgentModel.domain),
            )
            result = await self.session.execute(stmt)
            user_model = result.scalar_one_or_none()
            if user_model is None:
                return None
            return self.mapper.to_dto(user_model)
        except SQLAlchemyError as e:
            logger.critical(
                f"Failed to retrieve user by user_uuid '{user_uuid}': {e}")
            raise RepositoryError(
                f"Failed to retrieve user by user_uuid '{user_uuid}': {e}"
            ) from e

    async def get_user_by_user_name(self, user_name: str) -> OutboundUserDTO | None:
        try:
            stmt = select(UserModel).where(
                UserModel.user_name == user_name).options(
                selectinload(UserModel.role)
            )
            result = await self.session.execute(stmt)
            user_model = result.scalar_one_or_none()
            if user_model is None:
                return None
            return self.mapper.to_dto(user_model)
        except SQLAlchemyError as e:
            logger.critical(
                f"Failed to retrieve user by user_name '{user_name}': {e}")
            raise RepositoryError(
                f"Failed to retrieve user by user_name '{user_name}': {e}"
            ) from e

    async def get_users(self) -> list[OutboundUserDTO]:
        try:
            stmt = select(UserModel).options(
                selectinload(UserModel.role)
            )
            result = await self.session.execute(stmt)
            user_models = result.scalars().all()
            return [self.mapper.to_dto(user_model)
                    for user_model in user_models]
        except SQLAlchemyError as e:
            logger.critical(f'Failed to retrieve users: {e}')
            raise RepositoryError(
                f'Failed to retrieve users: {e}'
            ) from e

    async def get_verify_password_data(self, user_name: str) -> VerifyPasswordDTO | None:
        try:
            stmt = select(UserModel).where(
                UserModel.user_name == user_name)
            result = await self.session.execute(stmt)
            user_model = result.scalar_one_or_none()
            if user_model is None:
                return None
            return self.mapper.to_verify_dto(user_model)
        except SQLAlchemyError as e:
            logger.critical(
                f"Failed to retrieve user by user_name '{user_name}': {e}")
            raise RepositoryError(
                f"Failed to retrieve user by user_name '{user_name}': {e}"
            ) from e
