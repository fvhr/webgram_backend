import asyncio

from dishka import AsyncContainer
from fastapi import FastAPI

from src.application.agents.service.sync_agent_service import SyncAgentService
from src.application.common.service.send_call_count_event_service import SendCallCountService
from src.application.common.service.send_system_events_service import SendSystemEventsService
from src.application.domain.service.sync_service import SyncDomainService
from src.application.extensions.service.sync_extension import SyncExtensionService
from src.application.queues.service.sync_queue_service import SyncQueueService
from src.application.user.service.add_default_role_and_user import CreateDefaultRoleAndUserService
from src.infrastructure.fs_events.fs_events import FreeSwitchEventListen
from src.utils import scheduler


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
        sync_queue_service = await request_container.get(SyncQueueService)
        await sync_queue_service()
        send_system_events_service = await request_container.get(SendSystemEventsService)
        send_call_count_event_service = await request_container.get(SendCallCountService)
        asyncio.create_task(scheduler(send_system_events_service))
        asyncio.create_task(scheduler(send_call_count_event_service))
        freeswitch_events = await request_container.get(FreeSwitchEventListen)
        await freeswitch_events()
