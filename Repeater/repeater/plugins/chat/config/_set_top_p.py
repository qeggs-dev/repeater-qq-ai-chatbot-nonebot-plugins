from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from ._core import ChatCore, RepeaterDebugMode
from ..assist import StrangerInfo

set_top_p = on_command('setTopP', aliases={'stp', 'set_top_p', 'Set_Top_P', 'SetTopP'}, rule=to_me(), block=True)

@set_top_p.handle()
async def handle_set_top_p(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot=bot, event=event, args=args)

    msg = stranger_info.message_str.strip()
    reply = MessageSegment.reply(event.message_id)

    try:
        if msg.endswith("%"):
            msg = msg[:-1]
            top_p = float(msg) / 100
        else:
            top_p = float(msg)
    except ValueError:
        await set_top_p.finish(
            reply +
            '====Chat.Set_Top_P====\n> Top_P设置错误，请输入0~1之间的浮点数'
        )
    if top_p < -2 or top_p > 2:
        await set_top_p.finish(
            reply +
            '====Chat.Set_Top_P====\n> Top_P设置错误，请输入0~1之间的浮点数'
        )

    chat_core = ChatCore(stranger_info.name_space.namespace)
    if RepeaterDebugMode:
        await set_top_p.finish(reply + f'[Chat.Set_Top_P|{chat_core.name_space}|{stranger_info.nickname}]:{msg}')
    else:
        code, text = await chat_core.set_config("top_p", top_p)

        await set_top_p.finish(reply + f'====Chat.Set_Top_P====\n> {chat_core.name_space}\nHTTP Code: {code}\n\nTop_P: {top_p}')