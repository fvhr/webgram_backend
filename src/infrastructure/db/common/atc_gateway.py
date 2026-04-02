from dataclasses import dataclass

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.ports.atc_gateway import AtcGatewayProtocol
from src.domain.domain.entities.domain import Domain
from src.infrastructure.db.common.mappers.domain import DomainGatewayDBMapper
from src.infrastructure.db.exceptions import RepositoryError
from src.logger import logger
from src.settings import Settings


@dataclass
class SqlAlchemyAtcGateway(AtcGatewayProtocol):
    session: AsyncSession
    settings: Settings
    mapper: DomainGatewayDBMapper

    async def get_atc_domains(self) -> list[Domain]:
        try:
            stmt = text(
                f"select domain_uuid, domain_name, domain_enabled, domain_description from {self.settings.DOMAIN_ATC_TABLE_NAME}")
            result = await self.session.execute(stmt)
            domain_models = result.all()
            return [self.mapper.to_entity(domain_model) for domain_model in domain_models]
        except SQLAlchemyError as e:
            logger.critical(f'Failed to retrieve sip profiles: {e}')
            raise RepositoryError(
                f'Failed to retrieve sip profiles: {e}'
            ) from e
