from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from ._core import ChatCore, RepeaterDebugMode
from ...assist import StrangerInfo

set_auto_shrink_length = on_command('setAutoShrinkLength', aliases={'sasl', 'set_auto_shrink_length', 'Set_Auto_Shrink_Length', 'SetAutoShrinkLength'}, rule=to_me(), block=True)

@set_auto_shrink_length.handle()
async def handle_set_auto_shrink_length(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot=bot, event=event, args=args)

    msg = stranger_info.message_str.strip()
    reply = MessageSegment.reply(event.message_id)

    try:
        auto_shrink_length = int(msg)
    except ValueError:
        await set_auto_shrink_length.finish(
            reply +
            '====Chat.Set_Auto_Shrink_Length====\n> 设置错误，请输入一个整数'
        )


    chat_core = ChatCore(stranger_info.namespace_str)
    if RepeaterDebugMode:
        await set_auto_shrink_length.finish(reply + f'[Chat.Set_Auto_Shrink_Length|{chat_core.name_space}|{stranger_info.nickname}]:{msg}')
    else:
        code, text = await chat_core.set_config("auto_shrink_length", auto_shrink_length)

        await set_auto_shrink_length.finish(reply + f'====Chat.Set_Auto_Shrink_Length====\n> {chat_core.name_space}\nHTTP Code: {code}\nAuto Shrink Length: {auto_shrink_length}')