import json
import httpx
from environs import Env
from nonebot import logger
from typing import (
    Optional,
    Union
)

# 服务端配置
from ..core_config import *

class ChatCore:
    def __init__(self, session_id: str):
        self.url = f"{CHAT_API}:{CHAT_PORT}"
        self.session_id = session_id

    # region set timezone
    async def set_time_zone(self, timezone: float=1.0):
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f'{self.url}/{SET_CONFIG_ROUTE}/{self.session_id}/float',
                params={
                    'key': 'time_zone'
                },
                data={
                    'value': timezone
                }
            )
        return response.status_code, response.text
    # endregion

    # region change subsession
    async def change_subsession(self, sub_session_id: str):
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f'{self.url}/{CHANGE_SUBSESSION_CONFIG_ROUTE}',
                params={
                    'session_id': self.session_id,
                    'subsession_id': sub_session_id
                }
            )
        return response.status_code, response.text
    # endregion

    # region set model argument
    async def set_temperature(self, temperature: float=1.0):
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f'{self.url}/{SET_CONFIG_ROUTE}/{self.session_id}/float',
                params={
                    'key': 'temperature'
                },
                data={
                    'value': temperature
                }
            )
        return response.status_code, response.text

    async def set_frequency_penalty(self, frequency_penalty: float=0.0):
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f'{self.url}/{SET_CONFIG_ROUTE}/{self.session_id}/float',
                params={
                    'key': 'frequency_penalty'
                },
                data={
                    'value': frequency_penalty
                }
            )
        return response.status_code, response.text

    async def set_presence_penalty(self, presence_penalty: float=0.0):
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f'{self.url}/{SET_CONFIG_ROUTE}/{self.session_id}/float',
                params={
                    'key': 'presence_penalty'
                },
                data={
                    'value': presence_penalty
                }
            )
        return response.status_code, response.text
    # endregion

    # region memory switch
    async def enable_memory(self):
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f'{self.url}/{SET_CONFIG_ROUTE}/{self.session_id}/bool',
                params={
                    'key': 'load_memory'
                },
                data={
                    'value': True
                }
            )
        return response.status_code, response.text

    async def disable_memory(self):
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f'{self.url}/{SET_CONFIG_ROUTE}/{self.session_id}/bool',
                params={
                    'key': 'load_memory'
                },
                data={
                    'value': False
                }
            )
        return response.status_code, response.text
    # endregion
    # region set personality
    async def set_default_personality(self, name: str):
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f'{self.url}/{SET_CONFIG_ROUTE}/{self.session_id}/string',
                params={
                    'key': 'default_prompt_file'
                },
                data={
                    'value': name
                }
            )
        return response.status_code, response.text
    # endregion

    # region delete
    async def delete_config(self):
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f'{self.url}/{DELETE_CONFIG_ROUTE}/{self.session_id}'
            )
        return response.status_code, response.text
    # endregion

    # region clone
    async def clone_config(self, from_session_id:str, to_subsession_id:Optional[str] = None, from_sub_session_id:Optional[str] = None, auto_set_default:bool = True):
        async with httpx.AsyncClient() as client:
            data = {
                'from_session_id': from_session_id,
                'to_session_id': self.session_id,
                'auto_set_default': True
            }
            if from_sub_session_id:
                data['from_subsession_id'] = from_sub_session_id
            if to_subsession_id:
                data['to_subsession_id'] = to_subsession_id

            response = await client.post(
                f'{self.url}/{CLONE_CONFIG_ROUTE}',
                data=data
            )
        return response.status_code, response.text
    # endregion