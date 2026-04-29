from dataclasses import dataclass
from typing import final

from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.numbers.ports.repository import NumbersRepositoryProtocol
from src.domain.numbers.entities.numbers import Numbers
from src.infrastructure.db.exceptions import RepositoryError, ConflictRepositoryError
from src.infrastructure.db.models import NumberModel
from src.infrastructure.db.numbers.mappers.number import NumberDBMapper
from src.logger import logger


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class NumberRepositorySQLAlchemy(NumbersRepositoryProtocol):
    session: AsyncSession
    mapper: NumberDBMapper

    async def get_numbers(self) -> list[Numbers]:
        try:
            stmt = select(NumberModel)
            result = await self.session.execute(stmt)
            number_models = result.scalars().all()
            return [self.mapper.to_entity(number_model) for number_model in number_models]
        except SQLAlchemyError as e:
            logger.critical(f'Failed to retrieve numbers: {e}')
            raise RepositoryError(f'Failed to retrieve numbers: {e}') from e

    async def create_number(self, number: Numbers) -> Numbers | None:
        try:
            stmt = select(NumberModel).where(
                NumberModel.number_uuid == number.number_uuid
            )
            result = await self.session.execute(stmt)
            number_model = result.scalar_one_or_none()
            if number_model:
                return None
            number_model = self.mapper.to_model(number)
            self.session.add(number_model)
            await self.session.commit()
            return number
        except IntegrityError as e:
            logger.critical(
                f"Conflict while saving number '{number.number_uuid}': {e}"
            )
            raise ConflictRepositoryError(
                f"Conflict while saving number '{number.number_uuid}': {e}"
            ) from e
        except SQLAlchemyError as e:
            logger.critical(f"Failed to save number '{number.number_uuid}': {e}")
            raise RepositoryError(
                f"Failed to save number '{number.number_uuid}': {e}"
            ) from e

    async def update_number(self, number: Numbers) -> Numbers | None:
        try:
            stmt = select(NumberModel).where(
                NumberModel.number_uuid == number.number_uuid
            )
            result = await self.session.execute(stmt)
            number_model = result.scalar_one_or_none()

            if not number_model:
                return None
            self.mapper.update_model_from_entity(number_model, number)

            await self.session.commit()
            return number
        except IntegrityError as e:
            logger.critical(
                f"Conflict while saving number '{number.number_uuid}': {e}"
            )
            raise ConflictRepositoryError(
                f"Conflict while saving number '{number.number_uuid}': {e}"
            ) from e
        except SQLAlchemyError as e:
            logger.critical(f"Failed to save number '{number.number_uuid}': {e}")
            raise RepositoryError(
                f"Failed to save number '{number.number_uuid}': {e}"
            ) from e

    async def delete_number(self, number_uuid: str) -> None:
        try:
            stmt = delete(NumberModel).where(
                NumberModel.number_uuid == number_uuid
            )
            await self.session.execute(stmt)
            await self.session.commit()
        except SQLAlchemyError as e:
            logger.critical(f"Failed to delete number '{number_uuid}': {e}")
            raise RepositoryError(
                f"Failed to delete number '{number_uuid}': {e}"
            ) from e
