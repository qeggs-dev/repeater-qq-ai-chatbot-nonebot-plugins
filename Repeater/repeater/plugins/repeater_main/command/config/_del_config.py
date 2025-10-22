from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from .._clients import ConfigCore
from ...assist import StrangerInfo, SendMsg

del_config = on_command('delConfig', aliases={'dcfg', 'delete_config', 'Delete_Config', 'DeleteConfig'}, rule=to_me(), block=True)

@del_config.handle()
async def handle_del_config(bot: Bot, event: MessageEvent):
    stranger_info = StrangerInfo(bot, event)
    sendmsg = SendMsg("Config.Delete_Config", del_config, stranger_info)

    config_core = ConfigCore(stranger_info)
    if sendmsg.is_debug_mode:
        await sendmsg.send_debug_mode()
    else:
        response = await config_core.delete_config()
        await sendmsg.send_response(response, f"Delete Config {stranger_info.namespace_str}")
