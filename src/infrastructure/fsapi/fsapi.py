import json
import re
from dataclasses import dataclass
from json import JSONDecodeError
from typing import Optional, Any
from urllib.parse import quote

import aiohttp
from aiohttp import BasicAuth

from src.application.common.dtos.fsapi import ShowCallsDTO
from src.application.common.exceptions import FSAPIError
from src.application.common.ports.external import FreeswitchAPIProtocol
from src.application.common.ports.mapper import FSAPIDtoEntityMapperProtocol
from src.logger import logger
from src.settings import Settings


@dataclass
class ASyncFSAPI(FreeswitchAPIProtocol):
    settings: Settings
    _mapper: FSAPIDtoEntityMapperProtocol

    async def send_command(self, command: str, params: str) -> bool:
        auth = BasicAuth(self.settings.FSAPI_USERNAME, self.settings.FSAPI_PASSWORD)
        encoded_params = quote(params)
        full_url = f'{self.settings.FSAPI_URL}/{command}?{encoded_params}'
        async with aiohttp.ClientSession() as session:
            async with session.get(full_url, auth=auth) as response:
                res = await response.text()
                if 'OK' not in res:
                    return False
                return True

    async def get_calls_json(self) -> list[ShowCallsDTO]:
        auth = BasicAuth(self.settings.FSAPI_USERNAME, self.settings.FSAPI_PASSWORD)
        encoded_params = quote('calls as json')
        full_url = f'{self.settings.FSAPI_URL}/show?{encoded_params}'
        async with aiohttp.ClientSession() as session:
            async with session.get(full_url, auth=auth) as response:
                text = await response.text()
                _json = self.extract_json_from_html(text)
                if _json and 'rows' in _json:
                    calls = _json['rows']
                    return [self._mapper.to_calls_dto(call) for call in calls]
                return []

    @staticmethod
    def extract_json_from_html(html_text: str) -> Optional[Any]:
        """
        Извлекает первый JSON объект из HTML текста
        """
        match = re.search(r'(\{.*\})', html_text, re.DOTALL)

        if not match:
            return None

        json_str = match.group(1)

        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            logger.critical('Не удалось раскодировать вызовы: invalid json')
            return None
