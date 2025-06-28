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
                data={
                    'key': 'time_zone',
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
                data={
                    'key': 'temperature',
                    'value': temperature
                }
            )
        return response.status_code, response.text

    async def set_frequency_penalty(self, frequency_penalty: float=0.0):
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f'{self.url}/{SET_CONFIG_ROUTE}/{self.session_id}/float',
                data={
                    'key': 'frequency_penalty',
                    'value': frequency_penalty
                }
            )
        return response.status_code, response.text

    async def set_presence_penalty(self, presence_penalty: float=0.0):
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f'{self.url}/{SET_CONFIG_ROUTE}/{self.session_id}/float',
                data={
                    'key': 'presence_penalty',
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
                data={
                    'key': 'load_memory',
                    'value': True
                }
            )
        return response.status_code, response.text

    async def disable_memory(self):
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f'{self.url}/{SET_CONFIG_ROUTE}/{self.session_id}/bool',
                data={
                    'key': 'load_memory',
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
                data={
                    'key': 'default_prompt_file',
                    'value': name
                }
            )
        return response.status_code, response.text
    # endregion
    # region render style
    async def set_render_style(self, style: str):
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f'{self.url}/{SET_CONFIG_ROUTE}/{self.session_id}/string',
                data={
                    'key': 'render_style',
                    'value': style
                }
            )
        return response.status_code, response.text
    # endregion

    # region default model
    async def set_default_model_type(self, model_type: str):
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f'{self.url}/{SET_CONFIG_ROUTE}/{self.session_id}/string',
                data={
                    'key': 'model_type',
                    'value': model_type
                }
            )
        return response.status_code, response.text
    # endregion


    # region set top_p
    async def set_top_p(self, top_p: float):
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f'{self.url}/{SET_CONFIG_ROUTE}/{self.session_id}/float',
                data={
                    'key': 'top_p',
                    'value': top_p
                }
            )
        return response.status_code, response.text
    # endregion

    # region set max_tokens
    async def set_max_tokens(self, max_tokens: int):
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f'{self.url}/{SET_CONFIG_ROUTE}/{self.session_id}/int',
                data={
                    'key': 'max_tokens',
                    'value': max_tokens
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