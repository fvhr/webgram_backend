from dataclasses import dataclass
from typing import final

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.application.tiers.dtos.tier import ViewTierDTO
from src.application.tiers.ports.repository import ViewTierRepositoryProtocol
from src.infrastructure.db.exceptions import RepositoryError
from src.infrastructure.db.models import TierModel, QueueModel
from src.infrastructure.db.tier.mappers.tier import TierDBMapper
from src.logger import logger


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class ViewTierRepositorySQLAlchemy(ViewTierRepositoryProtocol):
    session: AsyncSession
    mapper: TierDBMapper

    async def get_agent_tiers(self, agent_uuid: str) -> list[ViewTierDTO]:
        try:
            stmt = select(TierModel).where(
                TierModel.agent_uuid == agent_uuid).options(
                selectinload(TierModel.queue).selectinload(QueueModel.domain)
            )
            result = await self.session.execute(stmt)
            tier_models = result.scalars().all()
            return [self.mapper.to_dto(tier_model)
                    for tier_model in tier_models]
        except SQLAlchemyError as e:
            logger.critical(
                f"Failed to retrieve tiers by agent_uuid '{agent_uuid}': {e}")
            raise RepositoryError(
                f"Failed to retrieve tiers by agent_uuid '{agent_uuid}': {e}"
            ) from e
