from dataclasses import dataclass
from typing import final

from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.agents.ports.repository import AgentRepositoryProtocol
from src.domain.agents.entities.agent import Agent
from src.infrastructure.db.agent.mappers.agent import AgentDBMapper
from src.infrastructure.db.exceptions import RepositoryError, ConflictRepositoryError
from src.infrastructure.db.models.agent import AgentModel
from src.logger import logger


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class AgentRepositorySQLAlchemy(AgentRepositoryProtocol):
    session: AsyncSession
    mapper: AgentDBMapper

    async def create_or_update_all_agents(self, agents: list[Agent]) -> list[Agent]:
        try:
            for agent in agents:
                stmt = select(AgentModel).where(
                    AgentModel.agent_uuid
                    == agent.agent_uuid
                )
                result = await self.session.execute(stmt)
                agent_model = result.scalar_one_or_none()
                if agent_model:
                    self.mapper.update_model_from_entity(agent_model, agent)
                else:
                    agent_model = self.mapper.to_model(agent)
                    self.session.add(agent_model)
            await self.session.commit()
            return agents
        except IntegrityError as e:
            logger.critical(
                f"Conflict while saving or update agents: {e}"
            )
            raise ConflictRepositoryError(
                f"Conflict while saving or update agents: {e}"
            ) from e
        except SQLAlchemyError as e:
            logger.critical(
                f"Failed to save or update agents: {e}"
            )
            raise RepositoryError(
                f"Failed to save or update agents: {e}"
            ) from e

    async def delete_agent(self, agent_uuid: str) -> None:
        try:
            stmt = delete(AgentModel).where(
                AgentModel.agent_uuid == agent_uuid
            )
            await self.session.execute(stmt)
            await self.session.commit()
        except SQLAlchemyError as e:
            logger.critical(
                f"Failed to delete agent '{agent_uuid}': {e}"
            )
            raise RepositoryError(
                f"Failed to delete agent '{agent_uuid}': {e}"
            ) from e

    async def get_agents(self) -> list[Agent]:
        try:
            stmt = select(AgentModel)
            result = await self.session.execute(stmt)
            agent_models = result.scalars().all()
            return [
                self.mapper.to_entity(agent_model)
                for agent_model in agent_models
            ]
        except SQLAlchemyError as e:
            logger.critical(f'Failed to retrieve agents: {e}')
            raise RepositoryError(f'Failed to retrieve agents: {e}') from e

    async def change_status_agent(self, agent_uuid: str, new_status: str) -> Agent:
        try:
            stmt = select(AgentModel).where(
                AgentModel.agent_uuid
                == agent_uuid
            )
            result = await self.session.execute(stmt)
            agent_model = result.scalar_one_or_none()
            if agent_model:
                agent_model.agent_status = new_status
            await self.session.commit()
            return self.mapper.to_entity(agent_model)
        except IntegrityError as e:
            logger.critical(
                f"Conflict while saving new agent status: {e}"
            )
            raise ConflictRepositoryError(
                f"Conflict while saving new agent status: {e}"
            ) from e
        except SQLAlchemyError as e:
            logger.critical(
                f"Failed to save new agent status: {e}"
            )
            raise RepositoryError(
                f"Failed to save new agent status: {e}"
            ) from e
