from uuid import UUID

from pydantic import BaseModel

from src.presentation.api.v1.agent.schemas.responses import AgentResponseSchema


class RoleResponseSchema(BaseModel):
    role_uuid: UUID
    role_name: str


class UserResponseSchema(BaseModel):
    user_uuid: UUID
    user_name: str
    role: RoleResponseSchema
    agent: AgentResponseSchema | None


class TokensResponseSchema(BaseModel):
    access_token: str
    refresh_token: str


class AccessTokenResponseSchema(BaseModel):
    access_token: str
