from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from ._core import ChatCore, RepeaterDebugMode
from ...assist import StrangerInfo

set_frequency_penalty = on_command('setFrequencyPenalty', aliases={'sfp', 'set_frequency_penalty', 'Set_Frequency_Penalty', 'SetFrequencyPenalty'}, rule=to_me(), block=True)

@set_frequency_penalty.handle()
async def handle_set_frequency_penalty(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot, event, args)

    msg = stranger_info.message_str.strip()
    reply = MessageSegment.reply(event.message_id)

    try:
        if msg.endswith("%"):
            msg = msg[:-1]
            frequency_penalty = float(msg) / 100
        else:
            frequency_penalty = float(msg)
    except ValueError:
        await set_frequency_penalty.finish(
            reply +
            '====Chat.Set_Frequency_Penalty====\n> 频率惩罚设置错误，请输入-2~2之间的浮点数或百分比'
        )
    if frequency_penalty < -2 or frequency_penalty > 2:
        await set_frequency_penalty.finish(
            reply +
            '====Chat.Set_Frequency_Penalty====\n> 频率惩罚设置错误，请输入-2~2之间的浮点数或百分比'
        )


    chat_core = ChatCore(stranger_info.name_space.namespace)
    if RepeaterDebugMode:
        await set_frequency_penalty.finish(reply + f'[Chat.Set_Frequency_Penalty|{chat_core.name_space}|{stranger_info.nickname}]:{msg}')
    else:
        code, text = await chat_core.set_config("frequency_penalty", frequency_penalty)

        await set_frequency_penalty.finish(reply + f'====Chat.Set_Frequency_Penalty====\n> {chat_core.name_space}\nHTTP Code: {code}\n\nFrequency_Penalty: {frequency_penalty}')