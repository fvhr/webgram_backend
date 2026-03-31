from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.user.mappers import UserDTOMapper
from src.application.user.ports.auth import AuthentificationProtocol
from src.application.user.ports.mappers import UserDtoEntityMapperProtocol
from src.application.user.ports.repository import UserRepositoryProtocol, ViewUserRepositoryProtocol, \
    RoleRepositoryProtocol
from src.application.user.service.add_default_role_and_user import CreateDefaultRoleAndUserService
from src.application.user.service.login_service import LoginService
from src.application.user.service.require_role_service import RequireRoleService
from src.application.user.service.resfresh_service import RefreshService
from src.application.user.use_cases.users.change_password import ChangePasswordUseCase
from src.application.user.use_cases.users.create_user import CreateUserUseCase
from src.application.user.use_cases.users.delete_user import DeleteUserUseCase
from src.application.user.use_cases.users.get_current_user import GetCurrentUserUseCase
from src.application.user.use_cases.users.get_user import GetUserUseCase
from src.application.user.use_cases.users.get_users import GetUsersUseCase
from src.application.user.use_cases.users.update_user import UpdateUserUseCase
from src.domain.services.password_hash_service import PasswordHashService
from src.infrastructure.db.user.mappers.role import RoleDBMapper
from src.infrastructure.db.user.mappers.user import UserDBMapper
from src.infrastructure.db.user.repositories.user import UserRepositorySQLAlchemy
from src.infrastructure.db.user.views.user import ViewUserRepositorySQLAlchemy
from src.settings import Settings


class UserRepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_user_repository(self, session: AsyncSession, db_mapper: UserDBMapper) \
            -> UserRepositoryProtocol:
        return UserRepositorySQLAlchemy(session=session, mapper=db_mapper)

    @provide(scope=Scope.REQUEST)
    async def get_user_view_repository(self, session: AsyncSession, db_mapper: UserDBMapper) \
            -> ViewUserRepositoryProtocol:
        return ViewUserRepositorySQLAlchemy(session=session, mapper=db_mapper)


class UserMapperProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_user_mapper(self) -> UserDtoEntityMapperProtocol:
        return UserDTOMapper()

    @provide(scope=Scope.REQUEST)
    async def get_user_db_mapper(self, role_db_mapper: RoleDBMapper,
                                 password_hash_service: PasswordHashService) -> UserDBMapper:
        return UserDBMapper(role_db_mapper, password_hash_service)


class UserUseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def create_user_use_case(
            self,
            user_repository: UserRepositoryProtocol,
            user_mapper: UserDtoEntityMapperProtocol,
            user_view: ViewUserRepositoryProtocol
    ) -> CreateUserUseCase:
        return CreateUserUseCase(_user_repository=user_repository,
                                 _user_mapper=user_mapper,
                                 _user_view=user_view)

    @provide(scope=Scope.REQUEST)
    async def delete_user_use_case(
            self,
            user_repository: UserRepositoryProtocol,
    ) -> DeleteUserUseCase:
        return DeleteUserUseCase(_user_repository=user_repository)

    @provide(scope=Scope.REQUEST)
    async def get_user_use_case(
            self,
            user_view_repo: ViewUserRepositoryProtocol,
    ) -> GetUserUseCase:
        return GetUserUseCase(_user_view_repo=user_view_repo, )

    @provide(scope=Scope.REQUEST)
    async def get_users_use_case(
            self,
            user_view_repo: ViewUserRepositoryProtocol,
    ) -> GetUsersUseCase:
        return GetUsersUseCase(_user_view_repo=user_view_repo, )

    @provide(scope=Scope.REQUEST)
    async def change_password_user_use_case(
            self,
            user_repository: UserRepositoryProtocol,
            user_view: ViewUserRepositoryProtocol
    ) -> ChangePasswordUseCase:
        return ChangePasswordUseCase(_user_repo=user_repository,
                                     _user_view_repo=user_view)

    @provide(scope=Scope.REQUEST)
    async def update_user_use_case(
            self,
            user_repository: UserRepositoryProtocol,
            user_view: ViewUserRepositoryProtocol
    ) -> UpdateUserUseCase:
        return UpdateUserUseCase(_user_repository=user_repository,
                                 _user_view_repo=user_view)

    @provide(scope=Scope.REQUEST)
    async def get_current_user_use_case(
            self,
            user_view_repo: ViewUserRepositoryProtocol,
            authentication: AuthentificationProtocol
    ) -> GetCurrentUserUseCase:
        return GetCurrentUserUseCase(_user_view_repo=user_view_repo, _authentication=authentication)


class UserServiceProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def create_default_user_service(
            self,
            settings: Settings,
            user_repo: UserRepositoryProtocol,
            user_view_repo: ViewUserRepositoryProtocol,
            role_repo: RoleRepositoryProtocol
    ) -> CreateDefaultRoleAndUserService:
        return CreateDefaultRoleAndUserService(_settings=settings,
                                               _user_repo=user_repo,
                                               _user_view_repo=user_view_repo,
                                               _role_repo=role_repo)

    @provide(scope=Scope.REQUEST)
    async def require_role_service(
            self,
            get_current_user_use_case: GetCurrentUserUseCase,
    ) -> RequireRoleService:
        return RequireRoleService(_get_current_user_use_case=get_current_user_use_case)

    @provide(scope=Scope.REQUEST)
    async def login_service(
            self,
            authentication: AuthentificationProtocol,
            password_hash: PasswordHashService,
            user_view_repo: ViewUserRepositoryProtocol,
    ) -> LoginService:
        return LoginService(_authentication=authentication, _password_hash=password_hash,
                            _user_view_repo=user_view_repo)

    @provide(scope=Scope.REQUEST)
    async def refresh_service(self, authentication: AuthentificationProtocol) -> RefreshService:
        return RefreshService(_authentication=authentication)


def get_user_providers() -> list[Provider]:
    return [
        UserRepositoryProvider(),
        UserMapperProvider(),
        UserUseCaseProvider(),
        UserServiceProvider(),
    ]
