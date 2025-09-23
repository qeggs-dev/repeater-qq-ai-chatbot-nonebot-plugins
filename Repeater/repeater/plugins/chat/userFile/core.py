import json
import httpx
from nonebot import logger
from typing import (
    Optional,
    Union
)

from ..core_config import *

class ChatCore:
    def __init__(self, namespace: str):
        self.name_space = namespace
    # region get_utl
    async def get_user_data_file_url(self):
        return f'{DOWNLOAD_USER_DATA_FILE_ROUTE}/{self.name_space}.zip'
    # endregion