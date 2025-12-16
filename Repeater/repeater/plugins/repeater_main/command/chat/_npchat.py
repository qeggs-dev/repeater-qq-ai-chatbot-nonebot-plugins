from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .._clients import ChatCore, ChatSendMsg
from ...assist import PersonaInfo, ImageDownloader
from ...logger import logger

npchat = on_command("npChat", aliases={"np", "no_prompt_chat", "No_Prompt_Chat", "NoPromptChat"}, rule=to_me(), block=True)

@npchat.handle()
async def handle_npchat(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot, event, args)

    logger.info(
        "Received a message {message} from {namespace}",
        message = persona_info.message_str,
        namespace = persona_info.namespace_str,
        module = "Chat.NPChat"
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

    response = await chat_core.send_message(message.extract_plain_text().strip())

    send_msg = ChatSendMsg(
        "No_Prompt_Chat",
        persona_info,
        npchat,
        response
    )
    await send_msg.send()