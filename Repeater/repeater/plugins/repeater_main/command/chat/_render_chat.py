from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .._clients import ChatCore, ChatSendMsg
from ...assist import StrangerInfo
from ...logger import logger

renderChat = on_command("renderChat", aliases={"rc", "render_chat", "Render_Chat", "RenderChat"}, rule=to_me(), block=True)

@renderChat.handle()
async def handle_render_Chat(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot, event, args)

    logger.info(
        "Received a message {message} from {namespace}",
        message = stranger_info.message_str,
        namespace = stranger_info.namespace_str,
        module = "Chat.Render_Chat"
    )
    
    message = stranger_info.message
    
    core = ChatCore(stranger_info)

    response = await core.send_message(
        message = message.extract_plain_text().strip()
    )

    send_msg = ChatSendMsg(
        "Render_Chat",
        stranger_info,
        renderChat,
        response
    )
    await send_msg.send_image()