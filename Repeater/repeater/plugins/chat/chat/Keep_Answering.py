from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore, RepeaterDebugMode, MAX_LENGTH, MAX_SINGLE_LINE_LENGTH, MIN_RENDER_IMAGE_TEXT_LINE
from ..assist import StrangerInfo
from .core._send_msg import send_msg

keepAnswering = on_command("keepAnswering", aliases={"ka", "keep_answering", "Keep_Answering", "KeepAnswering"}, rule=to_me(), block=True)

@keepAnswering.handle()
async def handle_keep_answering(bot: Bot, event: MessageEvent):
    stranger_info = StrangerInfo(bot, event)

    chat_core = ChatCore(stranger_info.name_space.namespace)

    response = await chat_core.send_message(user_info = stranger_info)
    
    await send_msg(
        "Keep_Answering",
        stranger_info,
        keepAnswering,
        response
    )