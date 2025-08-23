from nonebot import on_message, on_command
from nonebot.internal.matcher.matcher import Matcher
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot
from nonebot import logger

from .core import ChatCore, RepeaterDebugMode, MAX_LENGTH, MAX_SINGLE_LINE_LENGTH, MIN_RENDER_IMAGE_TEXT_LINE
from ..assist import StrangerInfo
from .core._send_msg import send_msg

smart_at: type[Matcher] = on_message(rule=to_me(), priority=100, block=True)

@smart_at.handle()
async def handle_smart_at(bot: Bot, event: MessageEvent):
    
    stranger_info = StrangerInfo(bot, event)
    
    if not stranger_info.message_str.strip():
        if stranger_info._mode == "group":
            await smart_at.finish(
                stranger_info._reply + '复读机在线哦~ ο(=•ω＜=)ρ⌒☆'
            )
        else:
            return
    
    core = ChatCore(stranger_info.name_space.namespace)

    response = await core.send_message(stranger_info.message_str.strip(), stranger_info.nickname)

    await send_msg(
        "Chat",
        stranger_info,
        smart_at,
        response
    )

chat: Matcher = on_command('chat', aliases={'c', 'Chat'}, rule=to_me(), block=True)

async def handle_chat(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot, event)

    core = ChatCore(stranger_info.name_space.namespace)

    response = await core.send_message(stranger_info.message_str.strip(), stranger_info.nickname)

    await send_msg(
        "Chat",
        stranger_info,
        chat,
        response,
    )