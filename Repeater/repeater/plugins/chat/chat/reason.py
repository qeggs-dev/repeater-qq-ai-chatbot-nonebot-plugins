from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore, RepeaterDebugMode
from ..assist_func import StrangerInfo
from .core._send_msg import send_msg

reason = on_command("reason", aliases={"r", "Reason"}, rule=to_me(), block=True)

@reason.handle()
async def reason_handle(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot, event, args)

    chat_core = ChatCore(stranger_info.name_space)
    response = await chat_core.send_message(message=stranger_info.message_str, username=stranger_info.nickname, model_type="reasoner")
    await send_msg(
        "Reason",
        stranger_info,
        reason,
        response
    )