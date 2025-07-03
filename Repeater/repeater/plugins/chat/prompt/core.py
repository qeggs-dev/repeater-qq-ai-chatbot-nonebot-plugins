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
    
    # region set prompt  
    async def set_prompt(self, prompt: str):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f'{self.url}/{SET_PROMPT_ROUTE}/{self.session_id}',
                data={
                    'prompt': prompt
                }
            )
        return response.status_code, response.text
    # endregion
    
    # region delete
    async def delete_prompt(self):
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f'{self.url}/{DELETE_PROMPT_ROUTE}/{self.session_id}'
            )
        return response.status_code, response.text
    
    async def delete_subprompt(self):
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f'{self.url}/{DELETE_SUBSESSION_PROMPT_ROUTE}',
                params={'session_id': self.session_id}
            )
        return response.status_code, response.text
    # endregion

    # region change subsession
    async def change_subsession(self, sub_session_id: str):
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f'{self.url}/{CHANGE_SUBSESSION_PROMPT_ROUTE}',
                params={
                    'session_id': self.session_id,
                    'subsession_id': sub_session_id
                }
            )
        return response.status_code, response.text
    # endregion
    
    # region clone
    async def clone_prompt(self, from_session_id:str, to_subsession_id:Optional[str] = None, from_sub_session_id:Optional[str] = None, auto_set_default:bool = True):
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
                f'{self.url}/{CLONE_PROMPT_ROUTE}',
                data=data
            )
        return response.status_code, response.text
    # endregion