from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.ports.external import AtcGatewayProtocol
from src.application.queues.event_handlers.heartbeat import QueueHeartbeatEventHandler
from src.application.queues.mappers import QueueDTOMapper
from src.application.queues.ports.mappers import QueueDtoEntityMapperProtocol
from src.application.queues.ports.repository import QueueRepositoryProtocol
from src.application.queues.service.sync_queue_service import SyncQueueService
from src.infrastructure.db.common.mappers.queue import QueueGatewayDBMapper
from src.infrastructure.db.queue.mappers.queue import QueueDBMapper
from src.infrastructure.db.queue.repositories.queue import QueueRepositorySQLAlchemy


class QueueRepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_queue_repository(self, session: AsyncSession, db_mapper: QueueDBMapper) \
            -> QueueRepositoryProtocol:
        return QueueRepositorySQLAlchemy(session=session, mapper=db_mapper)


class QueueMapperProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_queue_mapper(self) -> QueueDtoEntityMapperProtocol:
        return QueueDTOMapper()

    @provide(scope=Scope.REQUEST)
    async def get_queue_db_mapper(self) -> QueueDBMapper:
        return QueueDBMapper()

    @provide(scope=Scope.REQUEST)
    async def get_queue_gateway_db_mapper(self) -> QueueGatewayDBMapper:
        return QueueGatewayDBMapper()


class QueueServiceProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def start_queue_service(
            self,
            queue_repository: QueueRepositoryProtocol,
            atc_gateway: AtcGatewayProtocol,
            queue_mapper: QueueDtoEntityMapperProtocol,
    ) -> SyncQueueService:
        return SyncQueueService(_queue_repository=queue_repository, _atc_gateway=atc_gateway,
                                _queue_mapper=queue_mapper)


class QueueEventHandlersProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def queue_heartbeat_event_handler(
            self,
            sync_queue_service: SyncQueueService,
    ) -> QueueHeartbeatEventHandler:
        return QueueHeartbeatEventHandler(_queue_sync_service=sync_queue_service)


def get_queue_providers() -> list[Provider]:
    return [
        QueueRepositoryProvider(),
        QueueMapperProvider(),
        QueueServiceProvider(),
        QueueEventHandlersProvider(),
    ]
