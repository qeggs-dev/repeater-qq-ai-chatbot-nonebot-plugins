import json
import httpx
from nonebot import logger
from typing import (
    Optional,
    Union
)

from ..core_config import *

class ChatCore:
    _httpx_client = httpx.AsyncClient()

    def __init__(self, session_id: str):
        self.url = f"{CHAT_API}:{CHAT_PORT}"
        self.session_id = session_id
    
    # region set note  
    async def expand_variable(self, username: str, text: str):
        response = await self._httpx_client.post(
            f'{self.url}/{VARIABLE_EXPANSION}/{self.session_id}',
            data={
                'username': username,
                'text': text
            }
        )
        return response.status_code, response.text
    # endregion