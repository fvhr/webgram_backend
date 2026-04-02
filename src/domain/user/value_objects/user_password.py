import re
from dataclasses import dataclass

from src.domain.common import ValueObject
from src.domain.exceptions import ValidateError


@dataclass(frozen=True)
class UserPassword(ValueObject[str]):
    value: str

    def _validate(self) -> None:
        if len(self.value) < 8:
            raise ValidateError("Минимум 8 символов")
        if not re.match(r'^[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};:\'"\\|,.<>\/?`~]+$', self.value):
            raise ValidateError("Только латинские буквы, цифры и спецсимволы")
        if not re.search(r'[A-Z]', self.value):
            raise ValidateError("Минимум 1 заглавная буква")
        if not re.search(r'[a-z]', self.value):
            raise ValidateError("Минимум 1 строчная буква")
