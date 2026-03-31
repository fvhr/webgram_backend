from dataclasses import dataclass

from src.application.common.exceptions import AlreadyExistsError
from src.application.user.dtos.user import InboundUserDTO, OutboundUserDTO
from src.application.user.ports.mappers import UserDtoEntityMapperProtocol
from src.application.user.ports.repository import UserRepositoryProtocol, ViewUserRepositoryProtocol


@dataclass
class CreateUserUseCase:
    _user_repository: UserRepositoryProtocol
    _user_mapper: UserDtoEntityMapperProtocol
    _user_view: ViewUserRepositoryProtocol

    async def __call__(self, dto: InboundUserDTO) -> OutboundUserDTO:
        entity = self._user_mapper.to_entity(dto)
        user_uuid = await self._user_repository.create_user(entity)
        if user_uuid:
            user_out_dto = await self._user_view.get_user(str(user_uuid))
            return user_out_dto
        raise AlreadyExistsError(f'Entity with user_uuid "{dto.user_uuid}" already exists')
