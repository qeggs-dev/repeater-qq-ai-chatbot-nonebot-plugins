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
    
    # region inject context
    async def inject_context(self, text: str, role: str):
        response = await self._httpx_client.post(
            f'{self.url}/{INJECT_CONTEXT_ROUTE}/{self.session_id}',
            data={
                'text': text,
                'role': role
            }
        )
        return response.status_code, response.text
    # endregion
    
    # region withdraw
    async def withdraw(self):
        response = await self._httpx_client.post(
            f'{self.url}/{WIHTDRAW_CONTEXT_ROUTE}/{self.session_id}/lastmsg'
        )
        return response.status_code, response.text
    # endregion
    # region change subsession    
    async def change_context_branch(self, new_branch_id: str):
        response = await self._httpx_client.put(
            f'{self.url}/{CHANGE_CONTEXT_BRANCH_ROUTE}/{self.session_id}',
            params={
                'new_branch_id': new_branch_id
            }
        )
        return response.status_code, response.text
    # endregion
    
    # region delete
    async def delete_session(self):
        response = await self._httpx_client.delete(
            f'{self.url}/{DELETE_CONTEXT_ROUTE}/{self.session_id}'
        )
        return response.status_code, response.text
    
    async def delete_context(self):
        response = await self._httpx_client.delete(
            f'{self.url}/{DELETE_CONTEXT_ROUTE}/{self.session_id}'
        )
        return response.status_code, response.text
        
    async def delete_subsession(self):
        response = await self._httpx_client.delete(
            f'{self.url}/{DELETE_SUBSESSION_ROUTE}',
            params={'session_id': self.session_id}
        )
        return response.status_code, response.text
    # endregion
    
    async def get_context_total_length(self):
        response = await self._httpx_client.get(
            f'{self.url}/{GET_CONTEXT_LENGTH_ROUTE}/{self.session_id}'
        )
        return response.status_code, response.json()
    
    # region clone
    async def clone_session(self, from_session_id:str, to_subsession_id:Optional[str] = None, from_sub_session_id:Optional[str] = None, auto_set_default:bool = True):
        data = {
            'from_session_id': from_session_id,
            'to_session_id': self.session_id,
            'auto_set_default': True
        }
        if from_sub_session_id:
            data['from_subsession_id'] = from_sub_session_id
        if to_subsession_id:
            data['to_subsession_id'] = to_subsession_id
        
        response = await self._httpx_client.post(
            f'{self.url}/{CLONE_SESSION_ROUTE}',
            data=data
        )
        return response.status_code, response.text
    # endregion
    
    # region get_utl
    async def get_session_file_url(self):
        return f'{self.url}/{DOWNLOAD_SESSION_ROUTE}/{self.session_id}.zip'
    # endregion