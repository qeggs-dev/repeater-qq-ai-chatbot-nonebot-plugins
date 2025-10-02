from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore, RepeaterDebugMode
from ...assist import StrangerInfo
from .core._send_msg import send_msg

reason = on_command("reason", aliases={"r", "Reason"}, rule=to_me(), block=True)

@reason.handle()
async def reason_handle(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot, event, args)

    # message = await stranger_info.image_to_text(format="==== OCR Vision Begin ====\n{text}\n===== OCR Vision end =====", excluded_tags={"[动画表情]"})
    message = stranger_info.message

    chat_core = ChatCore(stranger_info.name_space.namespace)
    response = await chat_core.send_message(message=message.extract_plain_text().strip(), user_info = stranger_info, model_uid="deepseek-reasoner")
    await send_msg(
        "Reason",
        stranger_info,
        reason,
        response
    )