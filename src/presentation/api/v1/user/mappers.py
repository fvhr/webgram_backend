from dataclasses import dataclass
from typing import final

from src.application.user.dtos.role import RoleDTO
from src.application.user.dtos.user import InboundUserDTO, OutboundUserDTO, UpdateUserDTO, UpdatePasswordDTO, LoginDTO, \
    TokensDTO, RefreshDTO
from src.presentation.api.v1.user.schemas.responses import RoleResponseSchema, UserResponseSchema, \
    AccessTokenResponseSchema, TokensResponseSchema
from src.presentation.api.v1.user.schemas.schema import RoleSchema, UserSchema, UpdateUserSchema, \
    UpdateUserPasswordSchema, LoginSchema


@final
@dataclass(frozen=True, slots=True)
class RolePresentationMapper:
    @staticmethod
    def to_response(dto: RoleDTO) -> RoleResponseSchema:
        """Convert Application DTO to API Response model."""
        return RoleResponseSchema(
            role_uuid=dto.role_uuid,
            role_name=dto.role_name,
        )

    @staticmethod
    def to_dto(schema: RoleSchema) -> RoleDTO:
        """Convert API Response model to Application DTO."""
        return RoleDTO(
            role_uuid=schema.role_uuid,
            role_name=schema.role_name,
        )


@final
@dataclass(frozen=True, slots=True)
class UserPresentationMapper:
    @staticmethod
    def to_response(dto: OutboundUserDTO) -> UserResponseSchema:
        """Convert Application DTO to API Response model."""
        return UserResponseSchema(
            user_uuid=dto.user_uuid,
            user_name=dto.user_name,
            role=RolePresentationMapper.to_response(dto.role),
        )

    @staticmethod
    def to_dto(schema: UserSchema) -> InboundUserDTO:
        """Convert API Response model to Application DTO."""
        return InboundUserDTO(
            user_uuid=schema.user_uuid,
            user_name=schema.user_name,
            user_password=schema.user_password,
            role_uuid=schema.role_uuid,
        )

    @staticmethod
    def to_update_dto(schema: UpdateUserSchema) -> UpdateUserDTO:
        """Convert API Response model to Application DTO."""
        return UpdateUserDTO(
            user_uuid=schema.user_uuid,
            user_name=schema.user_name,
            role_uuid=schema.role_uuid,
        )

    @staticmethod
    def to_update_password_dto(schema: UpdateUserPasswordSchema) -> UpdatePasswordDTO:
        """Convert API Response model to Application DTO."""
        return UpdatePasswordDTO(
            password=schema.user_password
        )


@final
@dataclass(frozen=True, slots=True)
class AuthPresentationMapper:

    @staticmethod
    def to_login_dto(schema: LoginSchema) -> LoginDTO:
        return LoginDTO(
            user_name=schema.user_name,
            user_password=schema.user_password,
        )

    @staticmethod
    def to_tokens_response(tokens: TokensDTO) -> TokensResponseSchema:
        return TokensResponseSchema(
            access_token=tokens.access_token,
            refresh_token=tokens.refresh_token,
        )

    @staticmethod
    def to_access_token_response(_access_token: RefreshDTO) -> AccessTokenResponseSchema:
        return AccessTokenResponseSchema(
            access_token=_access_token.access_token,
        )
