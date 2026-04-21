from dataclasses import dataclass
from urllib.parse import quote

import aiohttp
from aiohttp import BasicAuth

from src.application.common.ports.external import FreeswitchAPIProtocol
from src.settings import Settings


@dataclass
class ASyncFSAPI(FreeswitchAPIProtocol):
    settings: Settings

    async def send_command(self, command: str, params: str) -> str:
        auth = BasicAuth(self.settings.FSAPI_USERNAME, self.settings.FSAPI_PASSWORD)
        encoded_params = quote(params)
        full_url = f'{self.settings.FSAPI_URL}/{command}?{encoded_params}'
        async with aiohttp.ClientSession() as session:
            async with session.get(full_url, auth=auth) as response:

                text = await response.text()
                print(text)
                return await response.text()
