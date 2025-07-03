import json
import httpx
from nonebot import logger
from typing import (
    Optional,
    Union
)

from ..core_config import *

class ChatCore:
    def __init__(self, session_id: str):
        self.url = f"{CHAT_API}:{CHAT_PORT}"
        self.session_id = session_id

    
    # region set note  
    async def expand_variable(self, username: str, text: str):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f'{self.url}/{VARIABLE_EXPANSION}/{self.session_id}',
                data={
                    'username': username,
                    'text': text
                }
            )
        return response.status_code, response.text
    # endregion