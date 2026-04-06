from dishka import Provider

from src.infrastructure.ioc.common_providers import (
    get_common_providers,
)
from src.infrastructure.ioc.providers.agent.agent import get_agent_providers
from src.infrastructure.ioc.providers.domain.domain import get_domain_providers
from src.infrastructure.ioc.providers.extension.extension import get_extension_providers
from src.infrastructure.ioc.providers.queue.queue import get_queue_providers
from src.infrastructure.ioc.providers.user.role import get_role_providers
from src.infrastructure.ioc.providers.user.user import get_user_providers


def get_providers() -> list[Provider]:
    """
    Returns a list of Dishka providers for dependency injection.

    Returns:
        list[Provider]: A list of configured providers.
    """

    return (
            get_common_providers()
            + get_role_providers()
            + get_user_providers()
            + get_domain_providers()
            + get_agent_providers()
            + get_extension_providers()
            + get_queue_providers()
    )
