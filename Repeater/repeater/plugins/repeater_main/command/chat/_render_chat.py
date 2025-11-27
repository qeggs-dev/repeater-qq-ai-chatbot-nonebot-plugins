from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .._clients import ChatCore, ChatSendMsg
from ...assist import PersonaInfo
from ...logger import logger

renderChat = on_command("renderChat", aliases={"rc", "render_chat", "Render_Chat", "RenderChat"}, rule=to_me(), block=True)

@renderChat.handle()
async def handle_render_Chat(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot, event, args)

    logger.info(
        "Received a message {message} from {namespace}",
        message = persona_info.message_str,
        namespace = persona_info.namespace_str,
        module = "Chat.Render_Chat"
    )
    
    message = persona_info.message
    
    core = ChatCore(persona_info)

    response = await core.send_message(
        message = message.extract_plain_text().strip()
    )

    send_msg = ChatSendMsg(
        "Render_Chat",
        persona_info,
        renderChat,
        response
    )
    await send_msg.send_image()