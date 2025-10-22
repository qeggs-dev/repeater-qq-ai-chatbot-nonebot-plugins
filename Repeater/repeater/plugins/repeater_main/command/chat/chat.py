from nonebot import on_message, on_command
from nonebot.internal.matcher.matcher import Matcher
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot
from ...logger import logger

from .._clients import ChatCore, ChatSendMsg
from ...assist import StrangerInfo, MessageSource, SendMsg

smart_at: type[Matcher] = on_message(rule=to_me(), priority=100, block=True)

@smart_at.handle()
async def handle_smart_at(bot: Bot, event: MessageEvent):
    stranger_info = StrangerInfo(bot, event)
    sendmsg = SendMsg("Chat.Smart_at", smart_at, stranger_info)

    logger.info(
        "Received a message {message} from {namespace}",
        message = stranger_info.message_str,
        namespace = stranger_info.namespace_str,
        module = "Chat.Smart_at"
    )

    # message = await stranger_info.image_to_text(format="==== OCR Vision Begin ====\n{text}\n===== OCR Vision end =====", excluded_tags={"[动画表情]"})
    message = stranger_info.message
    
    if not stranger_info.message_str.strip():
        if stranger_info._mode == MessageSource.GROUP:
            await sendmsg.send_hello()
        else:
            return
    
    core = ChatCore(stranger_info)
    
    response = await core.send_message(
        message = message.extract_plain_text().strip()
    )
    
    chat_send_msg = ChatSendMsg(
        "Chat.Smart_at",
        stranger_info,
        smart_at,
        response
    )
    await chat_send_msg.send()

chat: type[Matcher] = on_command('chat', aliases={'c', 'Chat'}, rule=to_me(), block=True)

@chat.handle()
async def handle_chat(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot, event, args)

    logger.info(
        "Received a message {message} from {namespace}",
        message = stranger_info.message_str,
        namespace = stranger_info.namespace_str,
        module = "Chat.Chat"
    )

    # message = await stranger_info.image_to_text(format="==== OCR Vision Begin ====\n{text}\n===== OCR Vision end =====", excluded_tags={"[动画表情]"})
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