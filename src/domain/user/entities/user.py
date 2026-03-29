from dataclasses import dataclass
from uuid import UUID

from src.domain.user.value_objects.user_name import UserName
from src.domain.user.value_objects.user_password import UserPassword


@dataclass
class User:
    user_uuid: UUID
    user_name: UserName
    user_password: UserPassword
    role_uuid: UUID
