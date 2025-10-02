import json
import httpx
from nonebot import logger
from typing import (
    Optional,
    Union
)

from ...core_config import *

class ChatCore:
    _httpx_client = httpx.AsyncClient()

    def __init__(self, name_space: str):
        self.name_space = name_space
    
    # region set prompt  
    async def set_prompt(self, prompt: str):
        response = await self._httpx_client.post(
            f'{SET_PROMPT_ROUTE}/{self.name_space}',
            data={
                'prompt': prompt
            }
        )
        return response.status_code, response.text
    # endregion
    
    # region delete
    async def delete_prompt(self):
        response = await self._httpx_client.delete(
            f'{DELETE_PROMPT_ROUTE}/{self.name_space}'
        )
        return response.status_code, response.text
    
    async def delete_subprompt(self):
        response = await self._httpx_client.delete(
            f'{DELETE_SUBSESSION_PROMPT_ROUTE}',
            params={'session_id': self.name_space}
        )
        return response.status_code, response.text
    # endregion

    # region change subsession
    async def change_prompt_branch(self, new_branch_id: str):
        response = await self._httpx_client.put(
            f'{CHANGE_PROMPT_BRANCH_ROUTE}/{self.name_space}',
            params={
                'new_branch_id': new_branch_id
            }
        )
        return response.status_code, response.text
    # endregion
    
    # region clone
    async def clone_prompt(self, from_session_id:str, to_subsession_id:Optional[str] = None, from_sub_session_id:Optional[str] = None, auto_set_default:bool = True):
        data = {
            'from_session_id': from_session_id,
            'to_session_id': self.name_space,
            'auto_set_default': True
        }
        if from_sub_session_id:
            data['from_subsession_id'] = from_sub_session_id
        if to_subsession_id:
            data['to_subsession_id'] = to_subsession_id

        response = await self._httpx_client.post(
            f'{CLONE_PROMPT_ROUTE}',
            data=data
        )
        return response.status_code, response.text
    # endregion