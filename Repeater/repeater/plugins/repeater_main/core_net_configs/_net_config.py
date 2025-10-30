from nonebot import get_plugin_config
from pydantic import BaseModel

class ChatConfig(BaseModel):
    backend_host: str = "127.0.0.1"
    backend_port: int = 8123
    repeater_debug_mode: bool = False

net_config: ChatConfig = get_plugin_config(ChatConfig)