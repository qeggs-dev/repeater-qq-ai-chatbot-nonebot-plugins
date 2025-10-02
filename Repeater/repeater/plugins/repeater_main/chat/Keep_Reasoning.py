from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore
from ..assist import StrangerInfo
from .core._send_msg import send_msg 

keepReasoning = on_command("keepReasoning", aliases={"kr", "keep_reasoning", "Keep_Reasoning", "KeepReasoning"}, rule=to_me(), block=True)

@keepReasoning.handle()
async def handle_keep_reasoning(bot: Bot, event: MessageEvent):
    stranger_info = StrangerInfo(bot, event)

    chat_core = ChatCore(stranger_info.name_space.namespace)

    response = await chat_core.send_message(user_info = stranger_info, model_uid="reasoning")
    
    await send_msg(
        "Keep_Reasoning",
        stranger_info,
        keepReasoning,
        response
    )
