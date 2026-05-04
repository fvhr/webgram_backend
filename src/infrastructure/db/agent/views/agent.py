from dataclasses import dataclass
from typing import final

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import selectinload

from src.application.agents.dtos.agent import AgentDTO
from src.application.agents.ports.repository import ViewAgentRepositoryProtocol
from src.infrastructure.db.agent.mappers.agent import AgentDBMapper
from src.infrastructure.db.exceptions import RepositoryError
from src.infrastructure.db.models import AgentModel, TierModel
from src.logger import logger


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class ViewAgentRepositorySQLAlchemy(ViewAgentRepositoryProtocol):
    session_maker: async_sessionmaker[AsyncSession]
    mapper: AgentDBMapper

    async def get_agent(self, agent_uuid: str) -> AgentDTO | None:
        try:
            async with self.session_maker() as session:
                stmt = select(AgentModel).where(
                    AgentModel.agent_uuid == agent_uuid
                ).options(
                    selectinload(AgentModel.tiers).selectinload(TierModel.queue),
                )
                result = await session.execute(stmt)
                user_model = result.scalar_one_or_none()
                if user_model is None:
                    return None
                return self.mapper.to_dto(user_model)
        except SQLAlchemyError as e:
            logger.critical(
                f"Failed to retrieve agent by agent_uuid '{agent_uuid}': {e}")
            raise RepositoryError(
                f"Failed to retrieve agent by agent_uuid '{agent_uuid}': {e}"
            ) from e
