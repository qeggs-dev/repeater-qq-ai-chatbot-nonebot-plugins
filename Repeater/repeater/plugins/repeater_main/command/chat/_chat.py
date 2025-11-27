from nonebot import on_command
from nonebot.internal.matcher.matcher import Matcher
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot
from ...logger import logger

from .._clients import ChatCore, ChatSendMsg
from ...assist import StrangerInfo

chat: type[Matcher] = on_command("chat", aliases={"c", "Chat"}, rule=to_me(), block=True)

@chat.handle()
async def handle_chat(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot, event, args)

    logger.info(
        "Received a message {message} from {namespace}",
        message = stranger_info.message_str,
        namespace = stranger_info.namespace_str,
        module = "Chat.Chat"
    )

    message = stranger_info.message

    core = ChatCore(stranger_info.namespace_str)

    response = await core.send_message(
        message = message.extract_plain_text().strip()
    )

    send_msg = ChatSendMsg(
        "Chat.Chat",
        stranger_info,
        chat,
        response
    )
    await send_msg.send_text()