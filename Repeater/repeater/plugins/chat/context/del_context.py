from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore, RepeaterDebugMode
from ..assist import StrangerInfo

delcontext = on_command('deleteContext', aliases={'dc', 'delete_context', 'Delete_Context', 'DeleteContext'}, rule=to_me(), block=True)

@delcontext.handle()
async def handle_delete_context(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot=bot, event=event, args=args)
    
    reply = MessageSegment.reply(event.message_id)
    chat_core = ChatCore(stranger_info.name_space.namespace)
    if RepeaterDebugMode:
        await delcontext.finish(reply + f'[Chat.Delete_Context|{chat_core.name_space}|{stranger_info.nickname}]')
    else:
        code, text = await chat_core.delete_context()

        await delcontext.finish(reply + f'====Chat.Delete_Context====\n> {chat_core.name_space}\n{text}\nHTTP Code: {code}')