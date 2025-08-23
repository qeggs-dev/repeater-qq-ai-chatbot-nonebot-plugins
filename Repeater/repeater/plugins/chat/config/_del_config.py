from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from ._core import ChatCore, RepeaterDebugMode
from ..assist import StrangerInfo

del_config = on_command('delConfig', aliases={'dcfg', 'delete_config', 'Delete_Config', 'DeleteConfig'}, rule=to_me(), block=True)

@del_config.handle()
async def handle_del_config(bot: Bot, event: MessageEvent):
    stranger_info = StrangerInfo(bot, event)

    reply = MessageSegment.reply(event.message_id)
    chat_core = ChatCore(stranger_info.name_space.namespace)
    if RepeaterDebugMode:
        await del_config.finish(reply + f'[Chat.Delete_Config|{chat_core.name_space}|{stranger_info.nickname}]')
    else:
        code, text = await chat_core.delete_config()

        await del_config.finish(reply + f'====Chat.Delete_Config====\n> {chat_core.name_space}\n{text}\nHTTP Code: {code}\n')
