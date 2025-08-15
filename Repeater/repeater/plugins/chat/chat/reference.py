from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore, RepeaterDebugMode
from ..assist_func import StrangerInfo
from .core._send_msg import send_msg

reference = on_command("Reference", aliases={"ref", "Reference"}, rule=to_me(), block=True)

@reference.handle()
async def handle_reference(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot, event, args)

    chat_core = ChatCore(stranger_info.name_space)

    if not stranger_info.noself_at_list:
        await reference.finish("==== Reference ==== \n Please at a member to get reference.")
        
    response = await chat_core.send_message(message=stranger_info.message, username=stranger_info.nickname, reference_context_id=stranger_info.noself_at_list[0])

    await send_msg(
        "Reference",
        stranger_info,
        reference,
        response
    )
