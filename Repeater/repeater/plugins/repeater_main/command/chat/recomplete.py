from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore, RepeaterDebugMode
from ...assist import StrangerInfo
from .core._send_msg import send_msg

recomplete = on_command("recomplete", aliases={"rec", "Recomplete"}, rule=to_me(), block=True)

@recomplete.handle()
async def handle_recomplete(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot, event, args)

    # message = await stranger_info.image_to_text(format="==== OCR Vision Begin ====\n{text}\n===== OCR Vision end =====", excluded_tags={"[动画表情]"})
    message = stranger_info.message

    chat_core = ChatCore(stranger_info.name_space.namespace)

    response = await chat_core.send_message(message=message.extract_plain_text().strip(), user_info = stranger_info)

    await send_msg(
        "Recomplete",
        stranger_info,
        recomplete,
        response,
    )