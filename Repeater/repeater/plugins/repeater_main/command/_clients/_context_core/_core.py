import json
import httpx
from nonebot import logger
from typing import (
    Optional,
    Union
)

from ....core_net_configs import *
from ....assist import StrangerInfo, Response
from ._response import (
    WithdrawResponse,
    ContextTotalLengthResponse
)

class ContextCore:
    _httpx_client = httpx.AsyncClient()

    def __init__(self, info: StrangerInfo):
        self._info = info
    
    # region inject context
    async def inject_context(self, text: str, role: str) -> Response[None]:
        response = await self._httpx_client.post(
            f'{INJECT_CONTEXT_ROUTE}/{self._info.namespace_str}',
            data={
                'text': text,
                'role': role
            }
        )
        return Response(
            code = response.status_code,
            text = response.text,
            data = None
        )
    # endregion
    
    # region withdraw
    async def withdraw(self) -> Response[WithdrawResponse | None]:
        response = await self._httpx_client.post(
            f'{WIHTDRAW_CONTEXT_ROUTE}/{self._info.namespace_str}'
        )
        return Response(
            code = response.status_code,
            text = response.text,
            data = WithdrawResponse(
                **response.json()
            ) if response.status_code == 200 else None
        )
    # endregion
    # region change subsession    
    async def change_context_branch(self, new_branch_id: str) -> Response[None]:
        response = await self._httpx_client.put(
            f'{CHANGE_CONTEXT_BRANCH_ROUTE}/{self._info.namespace_str}',
            data={
                'new_branch_id': new_branch_id
            }
        )
        return Response(
            code = response.status_code,
            text = response.text,
            data = None
        )
    # endregion
    
    # region delete
    async def delete_session(self) -> Response[None]:
        response = await self._httpx_client.delete(
            f'{DELETE_CONTEXT_ROUTE}/{self._info.namespace_str}'
        )
        return Response(
            code = response.status_code,
            text = response.text,
            data = None
        )
    
    async def delete_context(self) -> Response[None]:
        response = await self._httpx_client.delete(
            f'{DELETE_CONTEXT_ROUTE}/{self._info.namespace_str}'
        )
        return Response(
            code = response.status_code,
            text = response.text,
            data = None
        )
    # endregion
    
    async def get_context_total_length(self) -> Response[ContextTotalLengthResponse | None]:
        response = await self._httpx_client.get(
            f'{GET_CONTEXT_LENGTH_ROUTE}/{self._info.namespace_str}'
        )
        return Response(
            status_code = response.status_code,
            response_text = response.text,
            response_body = ContextTotalLengthResponse(
                **response.json()
            ) if response.status_code == 200 else None
        )