import json
import httpx
from typing import (
    Optional,
    Union
)

from ....core_net_configs import *
from ....assist import Response, StrangerInfo

class PromptCore:
    _httpx_client = httpx.AsyncClient()

    def __init__(self, info: StrangerInfo):
        self._info = info
    
    # region set prompt  
    async def set_prompt(self, prompt: str) -> Response[None]:
        response = await self._httpx_client.put(
            f'{SET_PROMPT_ROUTE}/{self._info.namespace_str}',
            data={
                'prompt': prompt
            }
        )
        return Response(
            code = response.status_code,
            text = response.text,
            data = None
        )
    # endregion
    
    # region delete
    async def delete_prompt(self) -> Response[None]:
        response = await self._httpx_client.delete(
            f'{DELETE_PROMPT_ROUTE}/{self._info.namespace_str}'
        )
        return Response(
            code = response.status_code,
            text = response.text,
            data = None
        )
    
    async def delete_subprompt(self) -> Response[None]:
        response = await self._httpx_client.delete(
            f'{DELETE_SUBSESSION_PROMPT_ROUTE}',
            params={'session_id': self._info.namespace_str}
        )
        return Response(
            code = response.status_code,
            text = response.text,
            data = None
        )
    # endregion

    # region change subsession
    async def change_prompt_branch(self, new_branch_id: str) -> Response[None]:
        response = await self._httpx_client.put(
            f'{CHANGE_PROMPT_BRANCH_ROUTE}/{self._info.namespace_str}',
            params={
                'new_branch_id': new_branch_id
            }
        )
        return Response(
            code = response.status_code,
            text = response.text,
            data = None
        )
    # endregion