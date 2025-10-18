from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .._clients import ChatCore, ChatSendMsg
from ...assist import StrangerInfo

keepAnswering = on_command("keepAnswering", aliases={"ka", "keep_answering", "Keep_Answering", "KeepAnswering"}, rule=to_me(), block=True)

@keepAnswering.handle()
async def handle_keep_answering(bot: Bot, event: MessageEvent):
    stranger_info = StrangerInfo(bot, event)

    chat_core = ChatCore(stranger_info.namespace_str)

    response = await chat_core.send_message()
    
    send_msg = ChatSendMsg(
        "Keep_Answering",
        stranger_info,
        keepAnswering,
        response
    )
    await send_msg.send()