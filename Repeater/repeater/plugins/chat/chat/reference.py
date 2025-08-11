from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore, RepeaterDebugMode
from ._get_stranger_info import StrangerInfo
from ._send_msg import send_msg

reference = on_command("Reference", aliases={"ref", "Reference"}, rule=to_me(), block=True)

@reference.handle()
async def handle_reference(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo()
    await stranger_info.get_stranger_info(bot, event, args)

    chat_core = ChatCore(stranger_info.name_space)
    response = await chat_core.send_message(message=stranger_info.message, username=stranger_info.nickname, reference_context_id=stranger_info.from_session_id)
    await send_msg(
        "Reference",
        stranger_info,
        reference,
        response
    )
