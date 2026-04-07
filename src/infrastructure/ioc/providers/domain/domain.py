from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.ports.external import AtcGatewayProtocol
from src.application.domain.mappers import DomainDTOMapper
from src.application.domain.ports.mappers import DomainDtoEntityMapperProtocol
from src.application.domain.ports.repository import DomainRepositoryProtocol
from src.application.domain.service.sync_service import SyncDomainService
from src.infrastructure.db.common.mappers.domain import DomainGatewayDBMapper
from src.infrastructure.db.domain.mappers.domain import DomainDBMapper
from src.infrastructure.db.domain.repositories.domain import DomainRepositorySQLAlchemy


class DomainRepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_domain_repository(self, session: AsyncSession, db_mapper: DomainDBMapper) \
            -> DomainRepositoryProtocol:
        return DomainRepositorySQLAlchemy(session=session, mapper=db_mapper)


class DomainMapperProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_domain_mapper(self) -> DomainDtoEntityMapperProtocol:
        return DomainDTOMapper()

    @provide(scope=Scope.REQUEST)
    async def get_domain_db_mapper(self) -> DomainDBMapper:
        return DomainDBMapper()

    @provide(scope=Scope.REQUEST)
    async def get_domain_gateway_db_mapper(self) -> DomainGatewayDBMapper:
        return DomainGatewayDBMapper()


class DomainServiceProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def start_domain_service(
            self,
            domain_repository: DomainRepositoryProtocol,
            atc_gateway: AtcGatewayProtocol,
    ) -> SyncDomainService:
        return SyncDomainService(_domain_repository=domain_repository, _atc_gateway=atc_gateway)


def get_domain_providers() -> list[Provider]:
    return [
        DomainRepositoryProvider(),
        DomainMapperProvider(),
        DomainServiceProvider(),
    ]
