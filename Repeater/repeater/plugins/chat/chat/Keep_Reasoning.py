from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore
from ._get_stranger_info import StrangerInfo
from ._send_msg import send_msg 

keepReasoning = on_command("keepReasoning", aliases={"kr", "keep_reasoning", "Keep_Reasoning", "KeepReasoning"}, rule=to_me(), block=True)

@keepReasoning.handle()
async def handle_keep_reasoning(bot: Bot, event: MessageEvent):
    stranger_info = StrangerInfo()
    await stranger_info.get_stranger_info(bot, event)

    chat_core = ChatCore(stranger_info.name_space)
    response = await chat_core.send_message(username=stranger_info.nickname, model_type="reasoning")
    await send_msg(
        "Keep_Reasoning",
        stranger_info,
        keepReasoning,
        response
    )
