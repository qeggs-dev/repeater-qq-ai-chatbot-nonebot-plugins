from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .._clients import ChatCore, ChatSendMsg
from ...assist import StrangerInfo
from ...logger import logger

npchat = on_command('npChat', aliases={'np', 'no_prompt_chat', 'No_Prompt_Chat', 'NoPromptChat'}, rule=to_me(), block=True)

@npchat.handle()
async def handle_npchat(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot, event, args)

    logger.info("Received a message {message} from {namespace}", message=stranger_info.message_str, namespace=stranger_info.namespace_str, module="Chat.NPChat")

    # message = await stranger_info.image_to_text(format="==== OCR Vision Begin ====\n{text}\n===== OCR Vision end =====", excluded_tags={"[动画表情]"})
    message = stranger_info.message

    chat_core = ChatCore(stranger_info.namespace_str)

    response = await chat_core.send_message(message.extract_plain_text().strip())

    send_msg = ChatSendMsg(
        "No_Prompt_Chat",
        stranger_info,
        npchat,
        response
    )
    await send_msg.send()