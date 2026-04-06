from dataclasses import dataclass
from typing import final

from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.queues.ports.repository import QueueRepositoryProtocol
from src.domain.queues.entities.queue import Queue
from src.infrastructure.db.exceptions import RepositoryError, ConflictRepositoryError
from src.infrastructure.db.models.queues import QueueModel
from src.infrastructure.db.queue.mappers.queue import QueueDBMapper
from src.logger import logger


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class QueueRepositorySQLAlchemy(QueueRepositoryProtocol):
    session: AsyncSession
    mapper: QueueDBMapper

    async def create_or_update_queue(self, queue: Queue) -> Queue | None:
        try:
            stmt = select(QueueModel).where(
                QueueModel.queue_uuid
                == queue.queue_uuid
            )
            result = await self.session.execute(stmt)
            queue_model = result.scalar_one_or_none()
            if queue_model:
                self.mapper.update_model_from_entity(queue_model, queue)
            else:
                queue_model = self.mapper.to_model(queue)
                self.session.add(queue_model)
            await self.session.commit()
            return queue
        except IntegrityError as e:
            logger.critical(
                f"Conflict while saving or update queue '{queue.queue_uuid}': {e}"
            )
            raise ConflictRepositoryError(
                f"Conflict while saving or update queue'{queue.queue_uuid}': {e}"
            ) from e
        except SQLAlchemyError as e:
            logger.critical(
                f"Failed to save or update queue'{queue.queue_uuid}': {e}"
            )
            raise RepositoryError(
                f"Failed to save or update queue'{queue.queue_uuid}': {e}"
            ) from e

    async def delete_queue(self, queue_uuid: str) -> None:
        try:
            stmt = delete(QueueModel).where(
                QueueModel.queue_uuid == queue_uuid
            )
            await self.session.execute(stmt)
            await self.session.commit()
        except SQLAlchemyError as e:
            logger.critical(
                f"Failed to delete queue '{queue_uuid}': {e}"
            )
            raise RepositoryError(
                f"Failed to delete queue '{queue_uuid}': {e}"
            ) from e

    async def get_queues(self) -> list[Queue]:
        try:
            stmt = select(QueueModel)
            result = await self.session.execute(stmt)
            queue_models = result.scalars().all()
            return [
                self.mapper.to_entity(queue_model)
                for queue_model in queue_models
            ]
        except SQLAlchemyError as e:
            logger.critical(f'Failed to retrieve queues: {e}')
            raise RepositoryError(f'Failed to retrieve queues: {e}') from e
