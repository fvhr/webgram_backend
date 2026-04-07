from dataclasses import dataclass

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.agents.dtos.agent import AgentAtcDTO
from src.application.common.ports.external import AtcGatewayProtocol
from src.application.extensions.dtos.extension import ExtensionAtcDTO
from src.application.queues.dtos.queue import QueueAtcDTO
from src.domain.domain.entities.domain import Domain
from src.infrastructure.db.common.mappers.agent import AgentGatewayDBMapper
from src.infrastructure.db.common.mappers.domain import DomainGatewayDBMapper
from src.infrastructure.db.common.mappers.extension import ExtensionGatewayDBMapper
from src.infrastructure.db.common.mappers.queue import QueueGatewayDBMapper
from src.infrastructure.db.exceptions import RepositoryError
from src.logger import logger
from src.settings import Settings


@dataclass
class SqlAlchemyAtcGateway(AtcGatewayProtocol):
    session: AsyncSession
    settings: Settings
    domain_mapper: DomainGatewayDBMapper
    agent_mapper: AgentGatewayDBMapper
    extension_mapper: ExtensionGatewayDBMapper
    queue_mapper: QueueGatewayDBMapper

    async def get_atc_domains(self) -> list[Domain]:
        try:
            stmt = text(
                f"select domain_uuid, domain_name, domain_enabled, domain_description from {self.settings.DOMAIN_ATC_TABLE_NAME}")
            result = await self.session.execute(stmt)
            domain_models = result.all()
            return [self.domain_mapper.to_entity(domain_model) for domain_model in domain_models]
        except SQLAlchemyError as e:
            logger.critical(f'Failed to retrieve atc domains: {e}')
            raise RepositoryError(
                f'Failed to retrieve atc domains: {e}'
            ) from e

    async def get_atc_agents(self) -> list[AgentAtcDTO]:
        try:
            stmt = text(
                f"select call_center_agent_uuid, agent_name, agent_id, "
                f"agent_password, domain_uuid from {self.settings.AGENT_ATC_TABLE_NAME}")
            result = await self.session.execute(stmt)
            agent_models = result.all()
            return [self.agent_mapper.to_entity(agent_model) for agent_model in agent_models]
        except SQLAlchemyError as e:
            logger.critical(f'Failed to retrieve atc agents: {e}')
            raise RepositoryError(
                f'Failed to retrieve atc agents: {e}'
            ) from e

    async def get_atc_extensions(self) -> list[ExtensionAtcDTO]:
        try:
            stmt = text(
                f"select extension_uuid, extension, password, effective_caller_id_name, "
                f"effective_caller_id_number, domain_uuid from {self.settings.EXTENSION_ATC_TABLE_NAME}")
            result = await self.session.execute(stmt)
            extension_models = result.all()
            return [self.extension_mapper.to_entity(extension_model) for extension_model in extension_models]
        except SQLAlchemyError as e:
            logger.critical(f'Failed to retrieve atc extensions: {e}')
            raise RepositoryError(
                f'Failed to retrieve atc extensions: {e}'
            ) from e

    async def get_atc_queues(self) -> list[QueueAtcDTO]:
        try:
            stmt = text(
                f"select call_center_queue_uuid, queue_name, queue_extension, "
                f"domain_uuid from {self.settings.QUEUE_ATC_TABLE_NAME}")
            result = await self.session.execute(stmt)
            queue_models = result.all()
            return [self.queue_mapper.to_entity(queue_model) for queue_model in queue_models]
        except SQLAlchemyError as e:
            logger.critical(f'Failed to retrieve atc queues: {e}')
            raise RepositoryError(
                f'Failed to retrieve atc queues: {e}'
            ) from e
