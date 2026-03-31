from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends

from src.application.user.use_cases.users.change_password import ChangePasswordUseCase
from src.application.user.use_cases.users.create_user import CreateUserUseCase
from src.application.user.use_cases.users.delete_user import DeleteUserUseCase
from src.application.user.use_cases.users.get_current_user import GetCurrentUserUseCase
from src.application.user.use_cases.users.get_user import GetUserUseCase
from src.application.user.use_cases.users.get_users import GetUsersUseCase
from src.application.user.use_cases.users.update_user import UpdateUserUseCase
from src.presentation.api.v1.user.mappers import UserPresentationMapper
from src.presentation.api.v1.user.schemas.responses import UserResponseSchema
from src.presentation.api.v1.user.schemas.schema import UserSchema, UpdateUserSchema, UpdateUserPasswordSchema
from src.presentation.api.v1.utils import require_roles

user_router = APIRouter(prefix='', tags=['Users'], dependencies=[Depends(require_roles(['superadmin']))])


@user_router.post('/users', response_model=UserResponseSchema)
@inject
async def create_user(
        user: UserSchema,
        use_case: FromDishka[CreateUserUseCase]
) -> UserResponseSchema:
    user_dto = UserPresentationMapper.to_dto(user)
    user_dto = await use_case(user_dto)
    return UserPresentationMapper.to_response(user_dto)


@user_router.delete('/users/{user_uuid}')
@inject
async def delete_user(
        user_uuid: UUID,
        use_case: FromDishka[DeleteUserUseCase]
) -> None:
    return await use_case(str(user_uuid))


@user_router.get(
    '/users',
    response_model=list[UserResponseSchema],
)
@inject
async def get_users(use_case: FromDishka[GetUsersUseCase]) -> \
        list[UserResponseSchema]:
    users_dto = await use_case()
    return [UserPresentationMapper.to_response(user_dto) for user_dto in
            users_dto]


@user_router.get(
    '/users/{user_uuid}',
    response_model=UserResponseSchema,
)
@inject
async def get_user(
        user_uuid: UUID,
        use_case: FromDishka[GetUserUseCase],
) -> UserResponseSchema:
    user_dto = await use_case(str(user_uuid))
    return UserPresentationMapper.to_response(user_dto)


@user_router.put(
    '/users',
    response_model=UserResponseSchema,
)
@inject
async def update_user(
        user: UpdateUserSchema,
        use_case: FromDishka[UpdateUserUseCase],
) -> UserResponseSchema:
    user_update_dto = UserPresentationMapper.to_update_dto(user)
    user_dto = await use_case(user_update_dto)
    return UserPresentationMapper.to_response(user_dto)


@user_router.patch(
    '/users/{user_uuid}',
    response_model=UserResponseSchema,
)
@inject
async def update_user_password(
        user_uuid: UUID,
        user: UpdateUserPasswordSchema,
        use_case: FromDishka[ChangePasswordUseCase],
) -> UserResponseSchema:
    user_update_dto = UserPresentationMapper.to_update_password_dto(user)
    user_dto = await use_case(str(user_uuid), user_update_dto)
    return UserPresentationMapper.to_response(user_dto)


@user_router.get('/users/show/me')
@inject
async def get_current_user(use_case: FromDishka[GetCurrentUserUseCase]):
    user_dto = await use_case()
    return UserPresentationMapper.to_response(user_dto)
