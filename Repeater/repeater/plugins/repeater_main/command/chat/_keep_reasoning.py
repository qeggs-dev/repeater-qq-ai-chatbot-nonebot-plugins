from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .._clients import ChatCore, ChatSendMsg
from ...assist import PersonaInfo, ImageDownloader
from ...logger import logger

keepReasoning = on_command("keepReasoning", aliases={"kr", "keep_reasoning", "Keep_Reasoning", "KeepReasoning"}, rule=to_me(), block=True)

@keepReasoning.handle()
async def handle_keep_reasoning(bot: Bot, event: MessageEvent):
    persona_info = PersonaInfo(bot, event)

    logger.info(
        "Received a message from {namespace}",
        namespace = persona_info.namespace_str,
        module = "Chat.Keep_Reasoning"
    )

    message = persona_info.message

    chat_core = ChatCore(persona_info)

    images: list[str] = []
    if "image" in message:
        async with ImageDownloader(persona_info) as downloader:
            get_image_url = downloader.download_image_to_base64()
            async for image_url in get_image_url:
                if image_url.data is not None:
                    images.append(
                        image_url.data
                    )

    response = await chat_core.send_message(model_uid="deepseek-reasoner")
    
    send_msg = ChatSendMsg(
        "Keep_Reasoning",
        persona_info,
        keepReasoning,
        response
    )
    await send_msg.send()
