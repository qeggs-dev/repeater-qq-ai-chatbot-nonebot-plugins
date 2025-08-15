from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore, RepeaterDebugMode
from ..assist_func import StrangerInfo
from .core._send_msg import send_msg

recomplete = on_command("recomplete", aliases={"rec", "Recomplete"}, rule=to_me(), block=True)

@recomplete.handle()
async def handle_recomplete(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot, event, args)

    chat_core = ChatCore(stranger_info.name_space)

    response = await chat_core.send_message(message=stranger_info.message_str, username=stranger_info.nickname)

    await send_msg(
        "Recomplete",
        stranger_info,
        recomplete,
        response,
    )