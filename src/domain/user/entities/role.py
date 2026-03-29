from dataclasses import dataclass
from uuid import UUID

from src.domain.user.value_objects.role_name import RoleName


@dataclass
class Role:
    role_uuid: UUID
    role_name: RoleName
