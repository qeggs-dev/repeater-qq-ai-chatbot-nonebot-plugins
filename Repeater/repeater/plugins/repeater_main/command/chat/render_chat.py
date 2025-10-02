from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore, RepeaterDebugMode, send_msg
from ...assist import image_to_text, StrangerInfo

renderChat = on_command('renderChat', aliases={'rc', 'render_chat', 'Render_Chat', 'RenderChat'}, rule=to_me(), block=True)

@renderChat.handle()
async def handle_render_Chat(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot, event)

    # message = await stranger_info.image_to_text(format="==== OCR Vision Begin ====\n{text}\n===== OCR Vision end =====", excluded_tags={"[动画表情]"})
    message = stranger_info.message
    
    core = ChatCore(stranger_info.namespace_str)

    response = await core.send_message(message.extract_plain_text().strip(), user_info = stranger_info)

    await send_msg(
        "Chat",
        stranger_info,
        renderChat,
        response,
        must = "image"
    )