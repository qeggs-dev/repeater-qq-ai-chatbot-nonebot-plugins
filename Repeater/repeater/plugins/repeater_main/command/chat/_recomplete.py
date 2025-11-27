from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .._clients import ChatCore, ChatSendMsg
from ...assist import PersonaInfo
from ...logger import logger

recomplete = on_command("recomplete", aliases={"rec", "Recomplete"}, rule=to_me(), block=True)

@recomplete.handle()
async def handle_recomplete(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot, event, args)

    logger.info(
        "Received a message {message} from {namespace}",
        message = persona_info.message_str,
        namespace = persona_info.namespace_str,
        module = "Chat.Recomplete"
    )

    message = persona_info.message

    chat_core = ChatCore(persona_info)

    response = await chat_core.send_message(
        message = message.extract_plain_text().strip()
    )

    send_msg = ChatSendMsg(
        "Recomplete",
        persona_info,
        recomplete,
        response,
    )
    await send_msg.send()