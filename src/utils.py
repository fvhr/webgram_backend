from dishka import AsyncContainer
from fastapi import FastAPI

from src.application.agents.service.sync_agent_service import SyncAgentService
from src.application.domain.service.sync_service import SyncDomainService
from src.application.extensions.service.sync_extension import SyncExtensionService
from src.application.user.service.add_default_role_and_user import CreateDefaultRoleAndUserService


async def start_default_functions(_app: FastAPI) -> None:
    container: AsyncContainer = _app.state.dishka_container
    async with container() as request_container:
        create_default_role_and_user_service = await request_container.get(CreateDefaultRoleAndUserService)
        await create_default_role_and_user_service()
        sync_domain_service = await request_container.get(SyncDomainService)
        await sync_domain_service()
        sync_agent_service = await request_container.get(SyncAgentService)
        await sync_agent_service()
        sync_extension_service = await request_container.get(SyncExtensionService)
        await sync_extension_service()
