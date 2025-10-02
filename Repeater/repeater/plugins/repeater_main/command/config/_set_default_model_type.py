from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from ._core import ChatCore, RepeaterDebugMode
from ...assist import StrangerInfo

set_default_model_type = on_command('setDefaultModel', aliases={'sdm', 'set_default_model', 'Set_Default_Model', 'SetDefaultModel'}, rule=to_me(), block=True)

@set_default_model_type.handle()
async def handle_set_default_model_type(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot=bot, event=event, args=args)

    msg: str = stranger_info.message_str.strip()

    chat_core = ChatCore(stranger_info.name_space.namespace)
    if RepeaterDebugMode:
        await set_default_model_type.finish(stranger_info.reply + f'[Chat.Set_Default_Model|{chat_core.name_space}|{stranger_info.nickname}]:{msg}')
    else:
        code, text = await chat_core.set_config("model_uid", msg)

        await set_default_model_type.finish(stranger_info.reply + f'====Chat.Set_Default_Model====\n> {chat_core.name_space}\nHTTP Code: {code}\n\nDefault_Model: {text}')