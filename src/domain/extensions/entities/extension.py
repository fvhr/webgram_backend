from dataclasses import dataclass
from uuid import UUID

from src.domain.extensions.value_objects.caller_id_number import CallerIdNumber
from src.domain.extensions.value_objects.extension_number import ExtensionNumber


@dataclass
class Extension:
    extension_uuid: UUID
    extension_number: ExtensionNumber
    extension_password: str
    caller_id_name: str
    caller_id_number: CallerIdNumber
    domain_uuid: UUID
