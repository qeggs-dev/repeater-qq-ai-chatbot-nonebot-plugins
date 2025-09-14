import json
import httpx
from nonebot import logger
from typing import (
    Optional,
    Union
)

from ..core_config import *
from ..assist import StrangerInfo

class ChatCore:
    _httpx_client = httpx.AsyncClient()

    def __init__(self, name_space: str):
        self.url = f"{CHAT_API}:{CHAT_PORT}"
        self.name_space = name_space
    
    # region set note  
    async def expand_variable(self, user_info: StrangerInfo, text: str):
        response = await self._httpx_client.post(
            f'{self.url}/{VARIABLE_EXPANSION}/{self.name_space}',
            json={
                'user_info':{
                    'username': user_info.nickname,
                    'nickname': user_info.display_name,
                    'gender': user_info.gender,
                    'age': user_info.age,
                },
                'text': text
            }
        )
        return response.status_code, response.text
    # endregion