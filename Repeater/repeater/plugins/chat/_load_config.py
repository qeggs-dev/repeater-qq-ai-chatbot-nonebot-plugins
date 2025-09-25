from nonebot import get_plugin_config
from pydantic import BaseModel

class ChatConfig(BaseModel):
    backend_host: str = "127.0.0.1"
    backend_port: int = 8123

config = get_plugin_config(ChatConfig)