from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.ports.external import AtcGatewayProtocol
from src.application.extensions.mappers import ExtensionDTOMapper
from src.application.extensions.ports.mapper import ExtensionDtoEntityMapperProtocol
from src.application.extensions.ports.repository import ExtensionRepositoryProtocol
from src.application.extensions.service.sync_extension import SyncExtensionService
from src.infrastructure.db.common.mappers.extension import ExtensionGatewayDBMapper
from src.infrastructure.db.extension.mappers.extension import ExtensionDBMapper
from src.infrastructure.db.extension.repositories.extension import ExtensionRepositorySQLAlchemy


class ExtensionRepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_extension_repository(self, session: AsyncSession, db_mapper: ExtensionDBMapper) \
            -> ExtensionRepositoryProtocol:
        return ExtensionRepositorySQLAlchemy(session=session, mapper=db_mapper)


class ExtensionMapperProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_extension_mapper(self) -> ExtensionDtoEntityMapperProtocol:
        return ExtensionDTOMapper()

    @provide(scope=Scope.REQUEST)
    async def get_extension_db_mapper(self) -> ExtensionDBMapper:
        return ExtensionDBMapper()

    @provide(scope=Scope.REQUEST)
    async def get_extension_gateway_db_mapper(self) -> ExtensionGatewayDBMapper:
        return ExtensionGatewayDBMapper()


class ExtensionServiceProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def start_extension_service(
            self,
            extension_repository: ExtensionRepositoryProtocol,
            atc_gateway: AtcGatewayProtocol,
            extension_mapper: ExtensionDtoEntityMapperProtocol,
    ) -> SyncExtensionService:
        return SyncExtensionService(_extension_repository=extension_repository, _atc_gateway=atc_gateway,
                                    _extension_mapper=extension_mapper)


def get_extension_providers() -> list[Provider]:
    return [
        ExtensionRepositoryProvider(),
        ExtensionMapperProvider(),
        ExtensionServiceProvider(),
    ]
