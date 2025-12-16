from nonebot import on_command
from nonebot.internal.matcher.matcher import Matcher
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot
from ...logger import logger

from .._clients import ChatCore, ChatSendMsg
from ...assist import PersonaInfo, ImageDownloader

nosave_chat: type[Matcher] = on_command("noSaveChat", aliases={"nsc", "no_save_chat", "NoSaveChat", "No_Save_Chat"}, rule=to_me(), block=True)

@nosave_chat.handle()
async def handle_nosave_chat(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot, event, args)

    logger.info(
        "Received a message {message} from {namespace}",
        message = persona_info.message_str,
        namespace = persona_info.namespace_str,
        module = "Chat.No_Save_Chat"
    )

    message = persona_info.message

    core = ChatCore(persona_info)

    images: list[str] = []
    if "image" in message:
        async with ImageDownloader(persona_info) as downloader:
            get_image_url = downloader.download_image_to_base64()
            async for image_url in get_image_url:
                if image_url.data is not None:
                    images.append(
                        image_url.data
                    )

    response = await core.send_message(
        message = message.extract_plain_text().strip(),
        save_context = False
    )

    send_msg = ChatSendMsg(
        "Chat.No_Save_Chat",
        persona_info,
        nosave_chat,
        response
    )
    await send_msg.send()