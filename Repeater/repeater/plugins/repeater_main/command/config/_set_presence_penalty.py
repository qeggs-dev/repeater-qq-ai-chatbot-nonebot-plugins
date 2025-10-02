from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from ._core import ChatCore, RepeaterDebugMode
from ...assist import StrangerInfo

set_presence_penalty = on_command('setPresencePenalty', aliases={'spp', 'set_presence_penalty', 'Set_Presence_Penalty', 'SetPresencePpenalty'}, rule=to_me(), block=True)

@set_presence_penalty.handle()
async def handle_set_presence_penalty(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot=bot, event=event, args=args)

    msg = stranger_info.message_str.strip()
    reply = MessageSegment.reply(event.message_id)

    try:
        if msg.endswith("%"):
            msg = msg[:-1]
            presence_penalty = float(msg) / 100
        else:
            presence_penalty = float(msg)
    except ValueError:
        await set_presence_penalty.finish(
            reply +
            '====Chat.Set_Presence_Penalty====\n> 存在惩罚设置错误，请输入-2~2之间的浮点数或百分比'
        )
    if presence_penalty < -2 or presence_penalty > 2:
        await set_presence_penalty.finish(
            reply +
            '====Chat.Set_Presence_Penalty====\n> 存在惩罚设置错误，请输入-2~2之间的浮点数或百分比'
        )


    chat_core = ChatCore(stranger_info.name_space.namespace)
    if RepeaterDebugMode:
        await set_presence_penalty.finish(reply + f'[Chat.Set_Presence_Penalty|{chat_core.name_space}|{stranger_info.nickname}]:{msg}')
    else:
        code, text = await chat_core.set_config('presence_penalty', presence_penalty)

        await set_presence_penalty.finish(reply + f'====Chat.Set_Presence_Penalty====\n> {chat_core.name_space}\nHTTP Code: {code}\n\nPresence_Penalty: {presence_penalty}')