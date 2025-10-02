from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot
from nonebot import logger

from .core import ChatCore, RepeaterDebugMode
from ...assist import StrangerInfo
from .core._send_msg import send_msg

public_space_chat = on_command('publicSpaceChat', aliases={'psc', 'public_space_chat', 'Public_Space_Chat', 'PublicSpaceChat'}, rule=to_me(), block=True)

@public_space_chat.handle()
async def handle_public_space_chat(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot, event, args)

    # message = await stranger_info.image_to_text(format="==== OCR Vision Begin ====\n{text}\n===== OCR Vision end =====", excluded_tags={"[动画表情]"})
    message = stranger_info.message

    chat_core = ChatCore(stranger_info.public_namespace_str)
    response = await chat_core.send_message(message=message.extract_plain_text().strip(), user_info = stranger_info)
    await send_msg(
        "Public_Space_Chat",
        stranger_info,
        public_space_chat,
        response
    )