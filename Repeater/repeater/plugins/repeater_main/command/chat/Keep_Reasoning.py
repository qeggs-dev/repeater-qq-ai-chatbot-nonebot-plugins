from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .._clients import ChatCore, ChatSendMsg
from ...assist import StrangerInfo

keepReasoning = on_command("keepReasoning", aliases={"kr", "keep_reasoning", "Keep_Reasoning", "KeepReasoning"}, rule=to_me(), block=True)

@keepReasoning.handle()
async def handle_keep_reasoning(bot: Bot, event: MessageEvent):
    stranger_info = StrangerInfo(bot, event)

    chat_core = ChatCore(stranger_info.namespace_str)

    response = await chat_core.send_message(model_uid="deepseek-reasoner")
    
    send_msg = ChatSendMsg(
        "Keep_Reasoning",
        stranger_info,
        keepReasoning,
        response
    )
    await send_msg.send()
