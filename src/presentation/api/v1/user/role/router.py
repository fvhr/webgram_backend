from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends

from src.application.user.use_cases.roles.create_role import CreateRoleUseCase
from src.application.user.use_cases.roles.delete_role import DeleteRoleUseCase
from src.application.user.use_cases.roles.get_role import GetRoleUseCase
from src.application.user.use_cases.roles.get_roles import GetRolesUseCase
from src.application.user.use_cases.roles.update_role import UpdateRoleUseCase
from src.presentation.api.v1.user.mappers import RolePresentationMapper
from src.presentation.api.v1.user.schemas.responses import RoleResponseSchema
from src.presentation.api.v1.user.schemas.schema import RoleSchema
from src.presentation.api.v1.utils import require_roles

role_router = APIRouter(prefix='', tags=['Roles'], dependencies=[Depends(require_roles(['superadmin']))])


@role_router.get(
    '/roles/{role_uuid}',
    response_model=RoleResponseSchema,
)
@inject
async def get_role(
        role_uuid: UUID,
        use_case: FromDishka[GetRoleUseCase],
) -> RoleResponseSchema:
    role_dto = await use_case(str(role_uuid))
    return RolePresentationMapper.to_response(role_dto)


@role_router.get(
    '/roles',
    response_model=list[RoleResponseSchema],
)
@inject
async def get_roles(use_case: FromDishka[GetRolesUseCase]) -> list[RoleResponseSchema]:
    roles_dto = await use_case()
    return [RolePresentationMapper.to_response(role_dto) for role_dto in roles_dto]


@role_router.post('/roles', response_model=RoleResponseSchema)
@inject
async def create_role(
        role: RoleSchema,
        use_case: FromDishka[CreateRoleUseCase]
) -> RoleResponseSchema:
    role_dto = RolePresentationMapper.to_dto(role)
    role_dto = await use_case(role_dto)
    return RolePresentationMapper.to_response(role_dto)


@role_router.put('/roles/{role_uuid}', response_model=RoleResponseSchema)
@inject
async def update_role(
        role: RoleSchema,
        use_case: FromDishka[UpdateRoleUseCase]
) -> RoleResponseSchema:
    role_dto = RolePresentationMapper.to_dto(role)
    role_dto = await use_case(role_dto)
    return RolePresentationMapper.to_response(role_dto)


@role_router.delete('/roles/{role_uuid}')
@inject
async def delete_role(
        role_uuid: UUID,
        use_case: FromDishka[DeleteRoleUseCase]
) -> None:
    return await use_case(str(role_uuid))
