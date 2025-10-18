from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .._core import ConfigCore
from ...assist import StrangerInfo, SendMsg

set_top_p = on_command('setTopP', aliases={'stp', 'set_top_p', 'Set_Top_P', 'SetTopP'}, rule=to_me(), block=True)

@set_top_p.handle()
async def handle_set_top_p(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot=bot, event=event, args=args)
    sendmsg = SendMsg("Chat.Set_Top_P", set_top_p, stranger_info)

    msg = stranger_info.message_str.strip()

    try:
        if msg.endswith("%"):
            msg = msg[:-1]
            top_p = float(msg) / 100
        else:
            top_p = float(msg)
    except ValueError:
        await sendmsg.send_error("Top_P setting error, please enter a floating-point number or percentage between 0 and 1!")
    if top_p < -2 or top_p > 2:
        await sendmsg.send_error("Top_P setting error, please enter a floating-point number or percentage between 0 and 1!")

    chat_core = ConfigCore(stranger_info.namespace_str)
    if sendmsg.is_debug_mode:
        await sendmsg.send_debug_mode()
    else:
        response = await chat_core.set_config("top_p", top_p)

        await sendmsg.send_response(response, f"Set Top_P to {top_p}")