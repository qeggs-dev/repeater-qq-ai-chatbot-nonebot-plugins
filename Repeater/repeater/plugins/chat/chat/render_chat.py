from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore, RepeaterDebugMode, send_msg
from ..assist import image_to_text, StrangerInfo

renderChat = on_command('renderChat', aliases={'rc', 'render_chat', 'Render_Chat', 'RenderChat'}, rule=to_me(), block=True)

@renderChat.handle()
async def handle_render_Chat(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot, event)
    
    core = ChatCore(stranger_info.name_space.namespace)

    response = await core.send_message(stranger_info.message_str.strip(), stranger_info.nickname)

    await send_msg(
        "Chat",
        stranger_info,
        renderChat,
        response,
        must_image=True
    )