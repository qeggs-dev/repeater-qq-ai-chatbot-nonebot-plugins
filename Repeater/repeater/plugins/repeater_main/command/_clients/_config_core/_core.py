import httpx
from ....logger import logger as base_logger
from typing import (
    Optional,
    Union,
    Any,
)

from ....assist import Response, StrangerInfo
# 服务端配置
from ....core_net_configs import *
from ....exit_register import ExitRegister

exit_register = ExitRegister()
logger = base_logger.bind(module = "Config.Core")

class ConfigCore:
    _httpx_client = httpx.AsyncClient()

    def __init__(self, info: StrangerInfo):
        self._info = info
    
    # region set config
    async def set_config(self, config_key: str, value: Any, item_type: str = "auto") -> Response[Any]:
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
                raise TypeError(f"Unsupported type: {type(value).__name__}")
            item_type = TYPES[type(value)]
        else:
            if item_type not in TYPES:
                raise TypeError(f"Unsupported type: {item_type}")
        logger.info("Set config: {config_key} = {value}({item_type})", config_key=config_key, value=value, item_type=item_type)
        response = await self._httpx_client.put(
            f'{SET_CONFIG_ROUTE}/{self._info.namespace_str}/{item_type}',
            data={
                'key': config_key,
                'value': value
            }
        )
        try:
            data = response.json()
        except Exception as e:
            logger.error(f"Error: {e}")
            data = None
        return Response(
            code = response.status_code,
            text = response.text,
            data = data
        )
    # endregion

    # region cache config
    async def cache_config(self, branch_id: str) -> Response[None]:
        logger.info("Cache config: {branch_id}", branch_id=branch_id)
        response = await self._httpx_client.put(
            url = f"{CHANGE_CONFIG_BRANCH_ROUTE}/{self._info.namespace_str}",
            data = {
                'new_branch_id': branch_id
            }
        )
        return Response(
            code = response.status_code,
            text = response.text,
            data = None
        )


    # region get config
    async def get_config(self, config_key: str) -> Response[Any]:
        logger.info("Get config: {config_key}", config_key=config_key)
        response = await self._httpx_client.get(
            f'{GET_CONFIG_ROUTE}/{self._info.namespace_str}'
        )
        try:
            data = response.json()
        except Exception as e:
            logger.error(f"Error: {e}")
            data = None
        return Response(
            code = response.status_code,
            text = response.text,
            data = data
        )
    # endregion

    # region remove config key
    async def remove_config_key(self, config_key: str) -> Response[None]:
        logger.info("Remove config key: {config_key}", config_key=config_key)
        response = await self._httpx_client.delete(
            f'{REMOVE_CONFIG_KEY_ROUTE}/{self._info.namespace_str}/{config_key}'
        )
        return Response(
            code = response.status_code,
            text = response.text,
            data = None
        )

    # region delete
    async def delete_config(self) -> Response[None]:
        logger.info("Delete config")
        response = await self._httpx_client.delete(
            f'{DELETE_CONFIG_ROUTE}/{self._info.namespace_str}'
        )
        return Response(
            code = response.status_code,
            text = response.text,
            data = None
        )
    # endregion

    # region close
    def close(self) -> None:
        self._httpx_client.aclose()
    # endregion