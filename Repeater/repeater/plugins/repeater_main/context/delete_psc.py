from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from ._core import ChatCore, RepeaterDebugMode
from ..assist import StrangerInfo

delete_public_space_context = on_command('deletePublicSpaceContext', aliases={'dpsc', 'delete_public_space_context', 'Delete_Public_Space_Context', 'DeletePublicSpaceContext'}, rule=to_me(), block=True)

@delete_public_space_context.handle()
async def handle_delete_public_space_context(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot=bot, event=event, args=args)

    reply = MessageSegment.reply(event.message_id)
    chat_core = ChatCore(stranger_info.name_space.namespace)
    if RepeaterDebugMode:
        await delete_public_space_context.finish(reply + f'[Context.Delete_Public_Space_Context|{chat_core.name_space}|{stranger_info.nickname}]')
    else:
        code, text = await chat_core.delete_context()

        await delete_public_space_context.finish(reply + f'====Context.Delete_Public_Space_Context====\n> {chat_core.name_space}\n{text}\nHTTP Code: {code}')