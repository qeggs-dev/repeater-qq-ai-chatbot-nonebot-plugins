from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from .._clients import ConfigCore
from ...assist import StrangerInfo, SendMsg

set_auto_shrink_length = on_command('setAutoShrinkLength', aliases={'sasl', 'set_auto_shrink_length', 'Set_Auto_Shrink_Length', 'SetAutoShrinkLength'}, rule=to_me(), block=True)

@set_auto_shrink_length.handle()
async def handle_set_auto_shrink_length(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot=bot, event=event, args=args)
    sendmsg = SendMsg("Config.Set_Auto_Shrink_Length", set_auto_shrink_length, stranger_info)

    try:
        auto_shrink_length = int(stranger_info.message_str)
    except ValueError:
        await sendmsg.send_error("Message must be a number")

    if sendmsg.is_debug_mode:
        await sendmsg.send_debug_mode()
    else:
        config_core = ConfigCore(stranger_info)
        response = await config_core.set_config("auto_shrink_length", auto_shrink_length)
        await sendmsg.send_response(response, f"Auto shrink length set to {auto_shrink_length}")