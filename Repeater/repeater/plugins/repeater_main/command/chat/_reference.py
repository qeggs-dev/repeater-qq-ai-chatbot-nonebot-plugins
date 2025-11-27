from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .._clients import ChatCore, ChatSendMsg
from ...assist import StrangerInfo
from ...logger import logger

reference = on_command("Reference", aliases={"ref", "Reference"}, rule=to_me(), block=True)

@reference.handle()
async def handle_reference(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot, event, args)

    logger.info(
        "Received a message {message} from {namespace}",
        message = stranger_info.message_str,
        namespace = stranger_info.namespace_str,
        module = "Chat.Reference"
    )

    message = stranger_info.message

    chat_core = ChatCore(stranger_info)

    if not stranger_info.noself_at_list:
        await reference.finish("==== Reference ==== \n Please at a member to get reference.")
        
    response = await chat_core.send_message(
        message = message.extract_plain_text().strip(), reference_context_id=stranger_info.noself_at_list[0]
    )

    send_msg = ChatSendMsg(
        "Reference",
        stranger_info,
        reference,
        response
    )
    await send_msg.send()
