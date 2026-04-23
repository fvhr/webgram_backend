from dishka import provide, Scope, Provider
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.user.mappers import RoleDTOMapper
from src.application.user.ports.mappers import RoleDtoEntityMapperProtocol
from src.application.user.ports.repository import RoleRepositoryProtocol
from src.application.user.use_cases.roles.create_role import CreateRoleUseCase
from src.application.user.use_cases.roles.delete_role import DeleteRoleUseCase
from src.application.user.use_cases.roles.get_role import GetRoleUseCase
from src.application.user.use_cases.roles.get_roles import GetRolesUseCase
from src.application.user.use_cases.roles.update_role import UpdateRoleUseCase
from src.infrastructure.db.user.mappers.role import RoleDBMapper
from src.infrastructure.db.user.repositories.role import RoleRepositorySQLAlchemy


class RoleRepositoryProvider(Provider):
    @provide(scope=Scope.SESSION)
    async def get_role_repository(
            self, session: AsyncSession, db_mapper: RoleDBMapper
    ) -> RoleRepositoryProtocol:
        return RoleRepositorySQLAlchemy(session=session, mapper=db_mapper)


class RoleMapperProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_role_mapper(self) -> RoleDtoEntityMapperProtocol:
        return RoleDTOMapper()

    @provide(scope=Scope.SESSION)
    async def get_role_db_mapper(self) -> RoleDBMapper:
        return RoleDBMapper()


class RoleUseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def create_role_use_case(
            self,
            role_repository: RoleRepositoryProtocol,
            role_mapper: RoleDtoEntityMapperProtocol,
    ) -> CreateRoleUseCase:
        return CreateRoleUseCase(
            _role_repository=role_repository,
            _role_mapper=role_mapper,
        )

    @provide(scope=Scope.REQUEST)
    async def delete_role_use_case(
            self,
            role_repository: RoleRepositoryProtocol,
    ) -> DeleteRoleUseCase:
        return DeleteRoleUseCase(_role_repository=role_repository)

    @provide(scope=Scope.REQUEST)
    async def get_role_use_case(
            self,
            role_repository: RoleRepositoryProtocol,
            role_mapper: RoleDtoEntityMapperProtocol,
    ) -> GetRoleUseCase:
        return GetRoleUseCase(
            _role_repository=role_repository,
            _role_mapper=role_mapper,
        )

    @provide(scope=Scope.REQUEST)
    async def get_roles_use_case(
            self,
            role_repository: RoleRepositoryProtocol,
            role_mapper: RoleDtoEntityMapperProtocol,
    ) -> GetRolesUseCase:
        return GetRolesUseCase(
            _role_repository=role_repository,
            _role_mapper=role_mapper,
        )

    @provide(scope=Scope.REQUEST)
    async def update_role_use_case(
            self,
            role_repository: RoleRepositoryProtocol,
            role_mapper: RoleDtoEntityMapperProtocol,
    ) -> UpdateRoleUseCase:
        return UpdateRoleUseCase(
            _role_repository=role_repository,
            _role_mapper=role_mapper,
        )




def get_role_providers() -> list[Provider]:
    return [
        RoleRepositoryProvider(),
        RoleMapperProvider(),
        RoleUseCaseProvider(),
    ]
