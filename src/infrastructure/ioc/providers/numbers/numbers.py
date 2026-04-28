from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.numbers.mappers import NumbersDTOMapper
from src.application.numbers.ports.mappers import NumbersDtoEntityMapperProtocol
from src.application.numbers.ports.repository import NumbersRepositoryProtocol
from src.application.numbers.use_cases.create_number import CreateNumberUseCase
from src.application.numbers.use_cases.delete_number import DeleteNumberUseCase
from src.application.numbers.use_cases.get_numbers import GetNumbersUseCase
from src.application.numbers.use_cases.update_number import UpdateNumberUseCase
from src.infrastructure.db.numbers.mappers.number import NumberDBMapper
from src.infrastructure.db.numbers.repositories.number import NumberRepositorySQLAlchemy


class NumberRepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_number_repository(
            self, session: AsyncSession, db_mapper: NumberDBMapper
    ) -> NumbersRepositoryProtocol:
        return NumberRepositorySQLAlchemy(session=session, mapper=db_mapper)


class NumberMapperProvider(Provider):
    @provide(scope=Scope.APP)
    def get_number_mapper(self) -> NumbersDtoEntityMapperProtocol:
        return NumbersDTOMapper()

    @provide(scope=Scope.REQUEST)
    def get_number_db_mapper(self) -> NumberDBMapper:
        return NumberDBMapper()


class UseCaseNumberProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_create_number_use_case(
            self,
            number_repository: NumbersRepositoryProtocol,
            number_mapper: NumbersDtoEntityMapperProtocol,
    ) -> CreateNumberUseCase:
        return CreateNumberUseCase(
            _number_repository=number_repository,
            _number_mapper=number_mapper,
        )

    @provide(scope=Scope.REQUEST)
    def get_delete_number_use_case(
            self,
            number_repository: NumbersRepositoryProtocol,
    ) -> DeleteNumberUseCase:
        return DeleteNumberUseCase(
            _number_repository=number_repository,
        )

    @provide(scope=Scope.REQUEST)
    def get_number_use_case(
            self,
            number_repository: NumbersRepositoryProtocol,
            number_mapper: NumbersDtoEntityMapperProtocol,
    ) -> GetNumbersUseCase:
        return GetNumbersUseCase(
            _number_repository=number_repository,
            _number_mapper=number_mapper,
        )

    @provide(scope=Scope.REQUEST)
    def get_update_number_use_case(
            self,
            number_repository: NumbersRepositoryProtocol,
            number_mapper: NumbersDtoEntityMapperProtocol,
    ) -> UpdateNumberUseCase:
        return UpdateNumberUseCase(
            _number_repository=number_repository,
            _number_mapper=number_mapper,
        )


def get_numbers_providers() -> list[Provider]:
    return [
        NumberRepositoryProvider(),
        NumberMapperProvider(),
        UseCaseNumberProvider(),
    ]
