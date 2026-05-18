import asyncio
import os
import sys
from datetime import timedelta
from typing import Generator
from unittest.mock import AsyncMock, Mock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.application.user.dtos.user import LoginDTO, TokensDTO, VerifyPasswordDTO
from src.application.user.service.login_service import LoginService
from src.application.user.service.require_role_service import RequireRoleService
from src.application.user.use_cases.users.get_current_user import GetCurrentUserUseCase
from src.domain.services.password_hash_service import PasswordHashService
from src.infrastructure.auth.authentification_from_auth_x import AuthentificationAuthX
from src.main import app
from src.presentation.api.v1.user.mappers import AuthPresentationMapper, UserPresentationMapper, RolePresentationMapper
from src.presentation.api.v1.user.schemas.schema import LoginSchema, UserSchema, UpdateUserSchema
from src.presentation.api.v1.user.schemas.responses import UserResponseSchema, TokensResponseSchema, \
    AccessTokenResponseSchema, RoleResponseSchema
from src.settings.config import Settings


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Создает event loop для асинхронных тестов."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_uuid() -> UUID:
    """Возвращает фиксированный UUID для тестов."""
    return uuid4()


@pytest.fixture
def test_user_name() -> str:
    """Возвращает тестовое имя пользователя."""
    return "test_user"


@pytest.fixture
def test_password() -> str:
    """Возвращает тестовый пароль."""
    return "SecurePassword123!"


@pytest.fixture
def password_hash_service() -> PasswordHashService:
    """Создает сервис хеширования паролей для тестов."""
    return PasswordHashService()


@pytest.fixture
def mock_settings() -> Settings:
    """Создает мок настроек для тестов."""
    settings = Mock(spec=Settings)
    settings.JWT_SECRET_KEY = "test_secret_key_for_testing_only"
    settings.DEVELOP_MODE = "dev"

    # Создаем тестовую конфигурацию AuthX
    from authx import AuthXConfig
    config = AuthXConfig()
    config.JWT_SECRET_KEY = settings.JWT_SECRET_KEY
    config.JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    config.JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)
    config.JWT_COOKIE_CSRF_PROTECT = False
    config.JWT_TOKEN_LOCATION = ["cookies"]
    config.JWT_ACCESS_COOKIE_NAME = "auth_token"
    config.JWT_REFRESH_COOKIE_NAME = "refresh_token"

    from authx import AuthX
    settings.SECURITY = AuthX(config=config)
    settings.CONFIG = config

    return settings


@pytest.fixture
def authentification_service(mock_settings: Settings) -> AuthentificationAuthX:
    """Создает сервис аутентификации для тестов."""
    return AuthentificationAuthX(_settings=mock_settings)


@pytest.fixture
def mock_user_repository() -> AsyncMock:
    """Создает мок репозитория пользователей."""
    repo = AsyncMock()
    repo.create_user = AsyncMock()
    repo.update_user = AsyncMock()
    repo.delete_user = AsyncMock()
    repo.change_password = AsyncMock()
    return repo


@pytest.fixture
def mock_view_user_repository() -> AsyncMock:
    """Создает мок view репозитория пользователей."""
    repo = AsyncMock()
    repo.get_user = AsyncMock()
    repo.get_user_by_user_name = AsyncMock()
    repo.get_users = AsyncMock()
    repo.get_verify_password_data = AsyncMock()
    return repo


@pytest.fixture
def mock_role_repository() -> AsyncMock:
    """Создает мок репозитория ролей."""
    repo = AsyncMock()
    repo.get_role = AsyncMock()
    repo.get_role_by_role_name = AsyncMock()
    repo.get_roles = AsyncMock()
    repo.create_role = AsyncMock()
    repo.update_role = AsyncMock()
    repo.delete_role = AsyncMock()
    return repo


class TestPasswordHashService:
    """Тесты для сервиса хеширования паролей."""

    def test_hash_password_returns_string(
            self,
            password_hash_service: PasswordHashService,
            test_password: str
    ) -> None:
        """Тест: хеширование пароля возвращает строку."""
        hashed = password_hash_service.hash_password(test_password)
        assert isinstance(hashed, str)
        assert len(hashed) > 0

    def test_hash_password_different_hashes_for_same_password(
            self,
            password_hash_service: PasswordHashService,
            test_password: str
    ) -> None:
        """Тест: одинаковые пароли дают разные хеши (из-за соли)."""
        hash1 = password_hash_service.hash_password(test_password)
        hash2 = password_hash_service.hash_password(test_password)
        assert hash1 != hash2

    def test_verify_password_correct_password(
            self,
            password_hash_service: PasswordHashService,
            test_password: str
    ) -> None:
        """Тест: проверка правильного пароля возвращает True."""
        hashed = password_hash_service.hash_password(test_password)
        assert password_hash_service.verify_password(test_password, hashed) is True

    def test_verify_password_incorrect_password(
            self,
            password_hash_service: PasswordHashService,
            test_password: str
    ) -> None:
        """Тест: проверка неправильного пароля возвращает False."""
        hashed = password_hash_service.hash_password(test_password)
        assert password_hash_service.verify_password("wrong_password", hashed) is False

    def test_verify_password_empty_password(
            self,
            password_hash_service: PasswordHashService
    ) -> None:
        """Тест: проверка пустого пароля."""
        hashed = password_hash_service.hash_password("")
        assert password_hash_service.verify_password("", hashed) is True
        assert password_hash_service.verify_password("not_empty", hashed) is False


class TestLoginService:
    """Тесты для сервиса входа."""

    @pytest.mark.asyncio
    async def test_login_success(
            self,
            mock_user_repository: AsyncMock,
            authentification_service: AuthentificationAuthX,
            password_hash_service: PasswordHashService,
            test_user_name: str,
            test_password: str,
            mock_uuid: UUID
    ) -> None:
        """Тест: успешный вход пользователя."""
        # Arrange
        hashed_password = password_hash_service.hash_password(test_password)
        verify_data = VerifyPasswordDTO(user_uuid=mock_uuid, password_hash=hashed_password)

        mock_view_repo = AsyncMock()
        mock_view_repo.get_verify_password_data = AsyncMock(return_value=verify_data)

        login_service = LoginService(
            _authentication=authentification_service,
            _password_hash=password_hash_service,
            _user_view_repo=mock_view_repo
        )

        login_dto = LoginDTO(user_name=test_user_name, user_password=test_password)

        # Act
        result = await login_service(login_dto)

        # Assert
        assert isinstance(result, TokensDTO)
        assert isinstance(result.access_token, str)
        assert isinstance(result.refresh_token, str)
        assert len(result.access_token) > 0
        assert len(result.refresh_token) > 0
        mock_view_repo.get_verify_password_data.assert_called_once_with(test_user_name)

    @pytest.mark.asyncio
    async def test_login_incorrect_password(
            self,
            password_hash_service: PasswordHashService,
            test_user_name: str,
            test_password: str,
            mock_uuid: UUID
    ) -> None:
        """Тест: вход с неправильным паролем выбрасывает ForbiddenError."""
        # Arrange
        wrong_password = "wrong_password"
        correct_hashed = password_hash_service.hash_password(test_password)
        verify_data = VerifyPasswordDTO(user_uuid=mock_uuid, password_hash=correct_hashed)

        mock_view_repo = AsyncMock()
        mock_view_repo.get_verify_password_data = AsyncMock(return_value=verify_data)

        mock_auth = AsyncMock()

        login_service = LoginService(
            _authentication=mock_auth,
            _password_hash=password_hash_service,
            _user_view_repo=mock_view_repo
        )

        login_dto = LoginDTO(user_name=test_user_name, user_password=wrong_password)

        # Act & Assert
        from src.application.common.exceptions import ForbiddenError
        with pytest.raises(ForbiddenError, match="Incorrect username or password"):
            await login_service(login_dto)

    @pytest.mark.asyncio
    async def test_login_user_not_found(
            self,
            authentification_service: AuthentificationAuthX,
            password_hash_service: PasswordHashService,
            test_user_name: str,
            test_password: str
    ) -> None:
        """Тест: вход несуществующего пользователя выбрасывает ForbiddenError."""
        # Arrange
        mock_view_repo = AsyncMock()
        mock_view_repo.get_verify_password_data = AsyncMock(return_value=None)

        login_service = LoginService(
            _authentication=authentification_service,
            _password_hash=password_hash_service,
            _user_view_repo=mock_view_repo
        )

        login_dto = LoginDTO(user_name=test_user_name, user_password=test_password)

        # Act & Assert
        from src.application.common.exceptions import ForbiddenError
        with pytest.raises(ForbiddenError, match="Incorrect username or password"):
            await login_service(login_dto)


class TestGetCurrentUserUseCase:
    """Тесты для use case получения текущего пользователя."""

    @pytest.mark.asyncio
    async def test_get_current_user_success(
            self,
            mock_view_user_repository: AsyncMock,
            authentification_service: AuthentificationAuthX,
            mock_uuid: UUID
    ) -> None:
        """Тест: успешное получение текущего пользователя."""
        # Arrange
        from src.application.user.dtos.role import RoleDTO
        from src.application.user.dtos.user import OutboundUserDTO

        role_dto = RoleDTO(role_uuid=uuid4(), role_name="user")
        user_dto = OutboundUserDTO(
            user_uuid=mock_uuid,
            user_name="test_user",
            role=role_dto,
            agent=None
        )

        mock_view_user_repository.get_user = AsyncMock(return_value=user_dto)

        # Создаем токен
        token = authentification_service.get_access_token(str(mock_uuid))

        use_case = GetCurrentUserUseCase(
            _user_view_repo=mock_view_user_repository,
            _authentication=authentification_service
        )

        # Act
        result = await use_case(token)

        # Assert
        assert result == user_dto
        mock_view_user_repository.get_user.assert_called_once_with(str(mock_uuid))

    @pytest.mark.asyncio
    async def test_get_current_user_invalid_token(
            self,
            mock_view_user_repository: AsyncMock,
            authentification_service: AuthentificationAuthX
    ) -> None:
        """Тест: получение пользователя с невалидным токеном."""
        # Arrange
        use_case = GetCurrentUserUseCase(
            _user_view_repo=mock_view_user_repository,
            _authentication=authentification_service
        )

        invalid_token = "invalid.token.here"

        # Act & Assert
        from src.application.common.exceptions import ForbiddenError
        with pytest.raises(ForbiddenError, match="Authentification required"):
            await use_case(invalid_token)

    @pytest.mark.asyncio
    async def test_get_current_user_none_token(
            self,
            mock_view_user_repository: AsyncMock,
            authentification_service: AuthentificationAuthX
    ) -> None:
        """Тест: получение пользователя с None токеном."""
        # Arrange
        use_case = GetCurrentUserUseCase(
            _user_view_repo=mock_view_user_repository,
            _authentication=authentification_service
        )

        # Act & Assert
        from src.application.common.exceptions import ForbiddenError
        with pytest.raises(ForbiddenError, match="Authentification required"):
            await use_case(None)

    @pytest.mark.asyncio
    async def test_get_current_user_not_found(
            self,
            mock_view_user_repository: AsyncMock,
            authentification_service: AuthentificationAuthX,
            mock_uuid: UUID
    ) -> None:
        """Тест: получение несуществующего пользователя."""
        # Arrange
        mock_view_user_repository.get_user = AsyncMock(return_value=None)

        token = authentification_service.get_access_token(str(mock_uuid))

        use_case = GetCurrentUserUseCase(
            _user_view_repo=mock_view_user_repository,
            _authentication=authentification_service
        )

        # Act & Assert
        from src.application.common.exceptions import NotFoundError
        with pytest.raises(NotFoundError, match=f'User with "{mock_uuid}" not found'):
            await use_case(token)


class TestRequireRoleService:
    """Тесты для сервиса проверки ролей."""

    @pytest.mark.asyncio
    async def test_require_role_success(
            self,
            mock_uuid: UUID
    ) -> None:
        """Тест: пользователь имеет требуемую роль."""
        # Arrange
        from src.application.user.dtos.role import RoleDTO
        from src.application.user.dtos.user import OutboundUserDTO

        role_dto = RoleDTO(role_uuid=uuid4(), role_name="admin")
        user_dto = OutboundUserDTO(
            user_uuid=mock_uuid,
            user_name="admin_user",
            role=role_dto,
            agent=None
        )

        mock_get_current_user = AsyncMock(return_value=user_dto)

        service = RequireRoleService(_get_current_user_use_case=mock_get_current_user)

        # Act
        await service(["admin", "superadmin"], "valid_token")

        # Assert - исключение не должно быть выброшено
        mock_get_current_user.assert_called_once_with("valid_token")

    @pytest.mark.asyncio
    async def test_require_role_insufficient_permissions(
            self,
            mock_uuid: UUID
    ) -> None:
        """Тест: пользователь не имеет требуемой роли."""
        # Arrange
        from src.application.user.dtos.role import RoleDTO
        from src.application.user.dtos.user import OutboundUserDTO

        role_dto = RoleDTO(role_uuid=uuid4(), role_name="user")
        user_dto = OutboundUserDTO(
            user_uuid=mock_uuid,
            user_name="regular_user",
            role=role_dto,
            agent=None
        )

        mock_get_current_user = AsyncMock(return_value=user_dto)

        service = RequireRoleService(_get_current_user_use_case=mock_get_current_user)

        # Act & Assert
        from src.application.common.exceptions import ForbiddenError
        with pytest.raises(ForbiddenError, match="Insufficient permissions"):
            await service(["admin", "superadmin"], "valid_token")


class TestAuthPresentationMapper:
    """Тесты для маппера аутентификации."""

    def test_to_login_dto(self, test_user_name: str, test_password: str) -> None:
        """Тест: маппинг LoginSchema в LoginDTO."""
        schema = LoginSchema(user_name=test_user_name, user_password=test_password)
        dto = AuthPresentationMapper.to_login_dto(schema)

        assert isinstance(dto, LoginDTO)
        assert dto.user_name == test_user_name
        assert dto.user_password == test_password

    def test_to_tokens_response(self) -> None:
        """Тест: маппинг TokensDTO в TokensResponseSchema."""
        dto = TokensDTO(access_token="access_123", refresh_token="refresh_456")
        schema = AuthPresentationMapper.to_tokens_response(dto)

        assert isinstance(schema, TokensResponseSchema)
        assert schema.access_token == "access_123"
        assert schema.refresh_token == "refresh_456"

    def test_to_access_token_response(self) -> None:
        """Тест: маппинг RefreshDTO в AccessTokenResponseSchema."""
        from src.application.user.dtos.user import RefreshDTO

        dto = RefreshDTO(access_token="new_access_789")
        schema = AuthPresentationMapper.to_access_token_response(dto)

        assert isinstance(schema, AccessTokenResponseSchema)
        assert schema.access_token == "new_access_789"


class TestUserPresentationMapper:
    """Тесты для маппера пользователей."""

    def test_to_dto(self, mock_uuid: UUID) -> None:
        """Тест: маппинг UserSchema в InboundUserDTO."""
        role_uuid = uuid4()
        schema = UserSchema(
            user_uuid=mock_uuid,
            user_name="test_user",
            user_password="password123",
            role_uuid=role_uuid
        )

        dto = UserPresentationMapper.to_dto(schema)

        from src.application.user.dtos.user import InboundUserDTO
        assert isinstance(dto, InboundUserDTO)
        assert dto.user_uuid == mock_uuid
        assert dto.user_name == "test_user"
        assert dto.user_password == "password123"
        assert dto.role_uuid == role_uuid

    def test_to_update_dto(self, mock_uuid: UUID) -> None:
        """Тест: маппинг UpdateUserSchema в UpdateUserDTO."""
        role_uuid = uuid4()
        schema = UpdateUserSchema(
            user_uuid=mock_uuid,
            user_name="updated_user",
            role_uuid=role_uuid
        )

        dto = UserPresentationMapper.to_update_dto(schema)

        from src.application.user.dtos.user import UpdateUserDTO
        assert isinstance(dto, UpdateUserDTO)
        assert dto.user_uuid == mock_uuid
        assert dto.user_name == "updated_user"
        assert dto.role_uuid == role_uuid


class TestRolePresentationMapper:
    """Тесты для маппера ролей."""

    def test_to_response(self) -> None:
        """Тест: маппинг RoleDTO в RoleResponseSchema."""
        from src.application.user.dtos.role import RoleDTO

        role_uuid = uuid4()
        dto = RoleDTO(role_uuid=role_uuid, role_name="admin")
        schema = RolePresentationMapper.to_response(dto)

        assert isinstance(schema, RoleResponseSchema)
        assert schema.role_uuid == role_uuid
        assert schema.role_name == "admin"

    def test_to_dto(self) -> None:
        """Тест: маппинг RoleSchema в RoleDTO."""
        from src.presentation.api.v1.user.schemas.schema import RoleSchema

        role_uuid = uuid4()
        schema = RoleSchema(role_uuid=role_uuid, role_name="user")
        dto = RolePresentationMapper.to_dto(schema)

        from src.application.user.dtos.role import RoleDTO
        assert isinstance(dto, RoleDTO)
        assert dto.role_uuid == role_uuid
        assert dto.role_name == "user"


class TestAuthentificationAuthX:
    """Тесты для сервиса аутентификации."""

    def test_get_access_token_returns_string(
            self,
            authentification_service: AuthentificationAuthX,
            mock_uuid: UUID
    ) -> None:
        """Тест: получение access токена."""
        token = authentification_service.get_access_token(str(mock_uuid))
        assert isinstance(token, str)
        assert len(token) > 0

    def test_get_refresh_token_returns_string(
            self,
            authentification_service: AuthentificationAuthX,
            mock_uuid: UUID
    ) -> None:
        """Тест: получение refresh токена."""
        token = authentification_service.get_refresh_token(str(mock_uuid))
        assert isinstance(token, str)
        assert len(token) > 0

    def test_get_user_uuid_by_token_valid_token(
            self,
            authentification_service: AuthentificationAuthX,
            mock_uuid: UUID
    ) -> None:
        """Тест: извлечение UUID из валидного токена."""
        token = authentification_service.get_access_token(str(mock_uuid))
        extracted_uuid = authentification_service.get_user_uuid_by_token(token)

        assert extracted_uuid is not None
        assert extracted_uuid == mock_uuid

    def test_get_user_uuid_by_token_invalid_token(
            self,
            authentification_service: AuthentificationAuthX
    ) -> None:
        """Тест: извлечение UUID из невалидного токена."""
        result = authentification_service.get_user_uuid_by_token("invalid.token.here")
        assert result is None

    def test_get_user_uuid_by_token_none(
            self,
            authentification_service: AuthentificationAuthX
    ) -> None:
        """Тест: извлечение UUID из None токена."""
        result = authentification_service.get_user_uuid_by_token(None)
        assert result is None


class TestAPIIntegration:
    """Интеграционные тесты для API endpoints."""

    @pytest.fixture
    def client(self) -> Generator[TestClient, None, None]:
        """Создает тестовый клиент для FastAPI приложения."""
        with TestClient(app=app, base_url="http://test") as client:
            yield client

    @pytest.mark.asyncio
    async def test_docs_endpoint_available(self) -> None:
        """Тест: документация API доступна."""
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test"
        ) as ac:
            response = await ac.get("/backend/api/docs")
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_redoc_endpoint_available(self) -> None:
        """Тест: Redoc документация доступна."""
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test"
        ) as ac:
            response = await ac.get("/backend/api/redoc")
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_openapi_schema_available(self) -> None:
        """Тест: OpenAPI схема доступна."""
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test"
        ) as ac:
            response = await ac.get("/backend/api/openapi.json")
            assert response.status_code == 200
            data = response.json()
            assert "openapi" in data
            assert "info" in data
            assert "paths" in data


class TestParametrized:
    """Параметризованные тесты для различных сценариев."""

    @pytest.mark.parametrize("password,expected_valid", [
        ("short", True),
        ("", True),
        ("very_long_password_" + "a" * 100, True),
        ("password with spaces", True),
        ("пароль на русском", True),
        ("p@$$w0rd!", True),
    ])
    def test_password_hashing_various_passwords(
            self,
            password_hash_service: PasswordHashService,
            password: str,
            expected_valid: bool
    ) -> None:
        """Тест: хеширование различных паролей."""
        hashed = password_hash_service.hash_password(password)
        assert password_hash_service.verify_password(password, hashed) is True
        assert password_hash_service.verify_password("wrong", hashed) is False

    @pytest.mark.parametrize("role,user_roles,expected_allowed", [
        (["admin"], ["admin"], True),
        (["admin", "superadmin"], ["superadmin"], True),
        (["admin"], ["user"], False),
        (["admin", "manager"], ["user"], False),
        (["user"], ["user"], True),
    ])
    @pytest.mark.asyncio
    async def test_role_checking_various_scenarios(
            self,
            mock_uuid: UUID,
            role: list[str],
            user_roles: list[str],
            expected_allowed: bool
    ) -> None:
        """Тест: проверка ролей в различных сценариях."""
        from src.application.user.dtos.role import RoleDTO
        from src.application.user.dtos.user import OutboundUserDTO

        # Берем первую роль из списка как роль пользователя
        user_role_name = user_roles[0]

        role_dto = RoleDTO(role_uuid=uuid4(), role_name=user_role_name)
        user_dto = OutboundUserDTO(
            user_uuid=mock_uuid,
            user_name="test_user",
            role=role_dto,
            agent=None
        )

        mock_get_current_user = AsyncMock(return_value=user_dto)
        service = RequireRoleService(_get_current_user_use_case=mock_get_current_user)

        if expected_allowed:
            await service(role, "token")
            assert True  # Исключение не выброшено
        else:
            from src.application.common.exceptions import ForbiddenError
            with pytest.raises(ForbiddenError):
                await service(role, "token")


class TestEdgeCases:
    """Тесты для граничных случаев и крайних сценариев."""

    def test_empty_user_name_login_schema(self) -> None:
        """Тест: схема логина с пустым именем пользователя."""
        schema = LoginSchema(user_name="", user_password="password")
        assert schema.user_name == ""
        assert schema.user_password == "password"

    def test_very_long_user_name(self) -> None:
        """Тест: схема с очень длинным именем пользователя."""
        long_name = "a" * 1000
        schema = LoginSchema(user_name=long_name, user_password="password")
        assert len(schema.user_name) == 1000

    def test_special_characters_in_password(self) -> None:
        """Тест: специальные символы в пароле."""
        special_password = "!@#$%^&*()_+-=[]{}|;:',.<>?/`~"
        schema = LoginSchema(user_name="user", user_password=special_password)
        assert schema.user_password == special_password

    @pytest.mark.asyncio
    async def test_concurrent_login_attempts(
            self,
            password_hash_service: PasswordHashService,
            authentification_service: AuthentificationAuthX,
            mock_uuid: UUID
    ) -> None:
        """Тест: одновременные попытки входа."""
        hashed_password = password_hash_service.hash_password("password")
        verify_data = VerifyPasswordDTO(user_uuid=mock_uuid, password_hash=hashed_password)

        mock_view_repo = AsyncMock()
        mock_view_repo.get_verify_password_data = AsyncMock(return_value=verify_data)

        login_service = LoginService(
            _authentication=authentification_service,
            _password_hash=password_hash_service,
            _user_view_repo=mock_view_repo
        )

        login_dto = LoginDTO(user_name="user", user_password="password")

        # Запускаем несколько одновременных запросов
        tasks = [login_service(login_dto) for _ in range(5)]
        results = await asyncio.gather(*tasks)

        assert len(results) == 5
        assert all(isinstance(r, TokensDTO) for r in results)


# =============================================================================
# Конфигурация pytest
# =============================================================================

def pytest_configure(config: pytest.Config) -> None:
    """Настройка конфигурации pytest."""
    config.addinivalue_line(
        "markers", "asyncio: mark test as an asyncio test."
    )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
