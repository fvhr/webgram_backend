from dataclasses import dataclass
from typing import final

from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.tiers.ports.repository import TierRepositoryProtocol
from src.domain.tiers.entities.tier import Tier
from src.infrastructure.db.exceptions import ConflictRepositoryError, RepositoryError
from src.infrastructure.db.models import TierModel
from src.infrastructure.db.tier.mappers.tier import TierDBMapper
from src.logger import logger


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class TierRepositorySQLAlchemy(TierRepositoryProtocol):
    session: AsyncSession
    mapper: TierDBMapper

    async def create_tier(self, tier: Tier) -> Tier:
        try:
            stmt = select(TierModel).where(
                TierModel.agent_uuid == tier.agent_uuid,
                TierModel.queue_uuid == tier.queue_uuid,
            )
            result = await self.session.execute(stmt)
            model = result.scalar_one_or_none()
            if model:
                return self.mapper.to_entity(model)
            model = self.mapper.to_model(tier)
            self.session.add(model)
            await self.session.commit()
            return self.mapper.to_entity(model)
        except IntegrityError as e:
            logger.critical(
                f"Conflict while saving tier '{tier}': {e}")
            raise ConflictRepositoryError(
                f"Conflict while saving tier '{tier}': {e}"
            ) from e
        except SQLAlchemyError as e:
            logger.critical(f"Failed to save tier '{tier}': {e}")
            raise RepositoryError(
                f"Failed to save tier '{tier}': {e}"
            ) from e

    async def delete_tier(self, agent_uuid: str, queue_uuid: str) -> None:
        try:
            stmt = delete(TierModel).where(
                TierModel.agent_uuid == agent_uuid,
                TierModel.queue_uuid == queue_uuid,
            )
            await self.session.execute(stmt)
            await self.session.commit()
        except SQLAlchemyError as e:
            logger.critical(f"Failed to delete tier '{agent_uuid}', '{queue_uuid}': {e}")
            raise RepositoryError(
                f"Failed to delete tier '{agent_uuid}', '{queue_uuid}': {e}"
            ) from e
