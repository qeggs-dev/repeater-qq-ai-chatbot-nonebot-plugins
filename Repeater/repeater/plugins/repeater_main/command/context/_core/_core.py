import json
import httpx
from nonebot import logger
from typing import (
    Optional,
    Union
)

from ....core_config import *
from ._response import (
    Response,
    WithdrawResponse,
    ContextTotalLengthResponse
)

class ChatCore:
    _httpx_client = httpx.AsyncClient()

    def __init__(self, namespace: str):
        self.name_space = namespace
    
    # region inject context
    async def inject_context(self, text: str, role: str):
        response = await self._httpx_client.post(
            f'{INJECT_CONTEXT_ROUTE}/{self.name_space}',
            data={
                'text': text,
                'role': role
            }
        )
        return response.status_code, response.text
    # endregion
    
    # region withdraw
    async def withdraw(self) -> Response[WithdrawResponse | None]:
        response = await self._httpx_client.post(
            f'{WIHTDRAW_CONTEXT_ROUTE}/{self.name_space}'
        )
        return Response(
            status_code = response.status_code,
            response_text = response.text,
            response_body = WithdrawResponse(
                **response.json()
            ) if response.status_code == 200 else None
        )
    # endregion
    # region change subsession    
    async def change_context_branch(self, new_branch_id: str):
        response = await self._httpx_client.put(
            f'{CHANGE_CONTEXT_BRANCH_ROUTE}/{self.name_space}',
            data={
                'new_branch_id': new_branch_id
            }
        )
        return response.status_code, response.text
    # endregion
    
    # region delete
    async def delete_session(self):
        response = await self._httpx_client.delete(
            f'{DELETE_CONTEXT_ROUTE}/{self.name_space}'
        )
        return response.status_code, response.text
    
    async def delete_context(self):
        response = await self._httpx_client.delete(
            f'{DELETE_CONTEXT_ROUTE}/{self.name_space}'
        )
        return response.status_code, response.text
    # endregion
    
    async def get_context_total_length(self) -> Response[ContextTotalLengthResponse | None]:
        response = await self._httpx_client.get(
            f'{GET_CONTEXT_LENGTH_ROUTE}/{self.name_space}'
        )
        return Response(
            status_code = response.status_code,
            response_text = response.text,
            response_body = ContextTotalLengthResponse(
                **response.json()
            ) if response.status_code == 200 else None
        )