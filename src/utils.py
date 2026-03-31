from dishka import AsyncContainer
from fastapi import FastAPI

from src.application.user.service.add_default_role_and_user import CreateDefaultRoleAndUserService


async def start_default_functions(_app: FastAPI) -> None:
    container: AsyncContainer = _app.state.dishka_container
    async with container() as request_container:
        create_default_role_and_user_service = await request_container.get(CreateDefaultRoleAndUserService)
        await create_default_role_and_user_service()
