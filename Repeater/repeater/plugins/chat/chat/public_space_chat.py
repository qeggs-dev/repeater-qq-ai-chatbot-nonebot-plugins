from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot
from nonebot import logger

from .core import ChatCore, RepeaterDebugMode
from ..assist import StrangerInfo
from .core._send_msg import send_msg

public_space_chat = on_command('publicSpaceChat', aliases={'psc', 'public_space_chat', 'Public_Space_Chat', 'PublicSpaceChat'}, rule=to_me(), block=True)

@public_space_chat.handle()
async def handle_public_space_chat(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
        stranger_info = StrangerInfo(bot, event, args)

        chat_core = ChatCore(stranger_info.name_space.public_space_id)
        response = await chat_core.send_message(message=stranger_info.message_str.strip(), username=stranger_info.nickname)
        await send_msg(
            "Public_Space_Chat",
            stranger_info,
            public_space_chat,
            response
        )