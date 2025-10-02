from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from ._core import ChatCore, RepeaterDebugMode
from ...assist import StrangerInfo

get_context_total_length = on_command('getContextTotalLength', aliases={'gctl', 'get_context_total_length', 'Get_Context_Total_Length', 'GetContextTotalLength'}, rule=to_me(), block=True)

@get_context_total_length.handle()
async def handle_total_context_length(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot=bot, event=event, args=args)
    
    reply = MessageSegment.reply(event.message_id)
    chat_core = ChatCore(stranger_info.namespace_str)
    if RepeaterDebugMode:
        await get_context_total_length.finish(reply + f'[Context.Get_Context_Total_Length|{chat_core.name_space}|{stranger_info.nickname}]')
    else:
        response = await chat_core.get_context_total_length()

        if response.status_code == 200:
            await get_context_total_length.finish(
                reply + f"====Context.Get_Context_Total_Length====\n"
                f"> {chat_core.name_space}\n"
                f"length: {response.response_body.context_length}\n"
                f"total_text_length: {response.response_body.total_context_length}\n"
                f"average_content_length: {response.response_body.average_content_length}\n"
                f"HTTP Code: {response.status_code}"
            )
        else:
            await get_context_total_length.finish(reply + f'====Context.Get_Context_Total_Length====\n> {chat_core.name_space}\nHTTP Code: {response.status_code}')