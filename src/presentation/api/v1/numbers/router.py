from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends

from src.application.numbers.use_cases.create_number import CreateNumberUseCase
from src.application.numbers.use_cases.delete_number import DeleteNumberUseCase
from src.application.numbers.use_cases.get_numbers import GetNumbersUseCase
from src.application.numbers.use_cases.update_number import UpdateNumberUseCase
from src.presentation.api.v1.numbers.mappers import NumbersPresentationMapper
from src.presentation.api.v1.numbers.schemas.responses import NumbersResponseSchema
from src.presentation.api.v1.numbers.schemas.schema import NumbersSchema
from src.presentation.api.v1.utils import require_authorization, require_roles

numbers_router = APIRouter(prefix='', tags=['Numbers'], )


@numbers_router.get(
    '/numbers',
    response_model=list[NumbersResponseSchema],
    dependencies=[Depends(require_authorization)]
)
@inject
async def get_numbers(
        use_case: FromDishka[GetNumbersUseCase],
) -> list[NumbersResponseSchema]:
    numbers_dto = await use_case()
    return [NumbersPresentationMapper.to_response(dto) for dto in numbers_dto]


@numbers_router.post('/numbers', response_model=NumbersResponseSchema,
                     dependencies=[Depends(require_roles(['superadmin', 'supervisor']))])
@inject
async def create_numbers(
        number: NumbersSchema, use_case: FromDishka[CreateNumberUseCase]
) -> NumbersResponseSchema | None:
    number_dto = NumbersPresentationMapper.to_dto(number)
    number_dto = await use_case(number_dto)
    if not number_dto:
        return None
    return NumbersPresentationMapper.to_response(number_dto)


@numbers_router.put('/numbers/{number_uuid}', response_model=NumbersResponseSchema,
                    dependencies=[Depends(require_roles(['superadmin', 'supervisor']))])
@inject
async def update_number(
        number: NumbersSchema, use_case: FromDishka[UpdateNumberUseCase]
) -> NumbersResponseSchema | None:
    number_dto = NumbersPresentationMapper.to_dto(number)
    number_dto = await use_case(number_dto)
    if not number_dto:
        return None
    return NumbersPresentationMapper.to_response(number_dto)


@numbers_router.delete('/numbers/{number_uuid}',
                       dependencies=[Depends(require_roles(['superadmin', 'supervisor']))])
@inject
async def delete_number(
        number_uuid: UUID, use_case: FromDishka[DeleteNumberUseCase]
) -> None:
    return await use_case(str(number_uuid))
