from uuid import UUID

from pydantic import BaseModel


class RoleSchema(BaseModel):
    role_uuid: UUID
    role_name: str


class UserSchema(BaseModel):
    user_uuid: UUID
    user_name: str
    user_password: str
    role_uuid: UUID


class UpdateUserSchema(BaseModel):
    user_uuid: UUID
    user_name: str
    role_uuid: UUID


class UpdateUserPasswordSchema(BaseModel):
    user_password: str


class LoginSchema(BaseModel):
    user_name: str
    user_password: str
