import json
import httpx
from nonebot import logger
from typing import (
    Optional,
    Union
)

from ....core_net_configs import *
from ....assist import StrangerInfo

class UserFileCore:
    def __init__(self, info: StrangerInfo):
        self._info = info
    # region get_utl
    async def get_user_data_file_url(self):
        return f'{DOWNLOAD_USER_DATA_FILE_ROUTE}/{self._info.namespace_str}.zip'
    # endregion