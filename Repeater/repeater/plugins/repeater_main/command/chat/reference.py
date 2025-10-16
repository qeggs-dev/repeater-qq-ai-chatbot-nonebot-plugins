from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore
from ...assist import StrangerInfo
from .core import Send_msg

reference = on_command("Reference", aliases={"ref", "Reference"}, rule=to_me(), block=True)

@reference.handle()
async def handle_reference(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot, event, args)

    # message = await stranger_info.image_to_text(format="==== OCR Vision Begin ====\n{text}\n===== OCR Vision end =====", excluded_tags={"[动画表情]"})
    message = stranger_info.message

    chat_core = ChatCore(stranger_info)

    if not stranger_info.noself_at_list:
        await reference.finish("==== Reference ==== \n Please at a member to get reference.")
        
    response = await chat_core.send_message(
        message = message.extract_plain_text().strip(), reference_context_id=stranger_info.noself_at_list[0]
    )

    send_msg = Send_msg(
        "Reference",
        stranger_info,
        reference,
        response
    )
    await send_msg.send()
