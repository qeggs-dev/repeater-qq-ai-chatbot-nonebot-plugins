from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore, RepeaterDebugMode
from ..assist import StrangerInfo

get_context_total_length = on_command('getContextTotalLength', aliases={'gctl', 'get_context_total_length', 'Get_Context_Total_Length', 'GetContextTotalLength'}, rule=to_me(), block=True)

@get_context_total_length.handle()
async def handle_total_context_length(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot=bot, event=event, args=args)
    
    reply = MessageSegment.reply(event.message_id)
    chat_core = ChatCore(stranger_info.name_space.namespace)
    if RepeaterDebugMode:
        await get_context_total_length.finish(reply + f'[Chat.Get_Context_Total_Length|{chat_core.name_space}|{stranger_info.nickname}]')
    else:
        code, body = await chat_core.get_context_total_length()

        await get_context_total_length.finish(reply + f'====Chat.Get_Context_Total_Length====\n> {chat_core.name_space}\nlength:{body.get("context_length", "0")}\ntotal_text_length:{body.get("total_context_length", "0")}\nHTTP Code: {code}')