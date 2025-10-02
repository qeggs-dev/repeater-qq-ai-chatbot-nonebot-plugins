import json
import httpx
from nonebot import logger
from typing import (
    Optional,
    Union,
    Any,
)

# 服务端配置
from ...core_net_configs import *
from ...exit_register import ExitRegister

exit_register = ExitRegister()

class ChatCore:
    _httpx_client = httpx.AsyncClient()

    def __init__(self, namespace: str):
        self.name_space = namespace
    
    # region set config
    async def set_config(self, config_key: str, value: Any, item_type: str = "auto"):
        TYPES = {
            int: "int",
            float: "float",
            str: "string",
            bool: "bool",
            dict: "dict",
            list: "list",
            None: "null"
        }
        if item_type == "auto":
            if type(value) not in TYPES:
                raise ValueError(f"Unsupported type: {type(value)}")
            item_type = TYPES[type(value)]
        else:
            if item_type not in TYPES:
                raise ValueError(f"Unsupported type: {item_type}")
        response = await self._httpx_client.put(
            f'{SET_CONFIG_ROUTE}/{self.name_space}/{item_type}',
            data={
                'key': config_key,
                'value': value
            }
        )
        if response.status_code == 200:
            try:
                response_json = response.json()
                return response.status_code, response_json.get(config_key, response.text)
            except json.JSONDecodeError:
                return response.status_code, response.text
        else:
            return response.status_code, response.text
    # endregion

    # region get config
    async def get_config(self, config_key: str):
        response = await self._httpx_client.get(
            f'{GET_CONFIG_ROUTE}/{self.name_space}'
        )
        if response.status_code == 200:
            return response.json().get(config_key, None)
        else:
            return None
    # endregion

    # region remove config key
    async def remove_config_key(self, config_key: str):
        response = await self._httpx_client.delete(
            f'{REMOVE_CONFIG_KEY_ROUTE}/{self.name_space}/{config_key}'
        )
        return response.status_code, response.text

    # region delete
    async def delete_config(self):
        response = await self._httpx_client.delete(
            f'{DELETE_CONFIG_ROUTE}/{self.name_space}'
        )
        return response.status_code, response.text
    # endregion

    # region clone
    async def clone_config(self, from_session_id:str, to_subsession_id:Optional[str] = None, from_sub_session_id:Optional[str] = None, auto_set_default:bool = True):
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
            f'{CLONE_CONFIG_ROUTE}',
            data=data
        )
        return response.status_code, response.text
    # endregion

    # region close
    def close(self) -> None:
        self._httpx_client.aclose()
    # endregion