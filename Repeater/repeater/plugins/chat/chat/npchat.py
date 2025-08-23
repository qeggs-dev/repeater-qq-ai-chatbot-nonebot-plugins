from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore
from ..assist import StrangerInfo
from .core._send_msg import send_msg

npchat = on_command('npChat', aliases={'np', 'no_prompt_chat', 'No_Prompt_Chat', 'NoPromptChat'}, rule=to_me(), block=True)

@npchat.handle()
async def handle_npchat(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot, event, args)

    chat_core = ChatCore(stranger_info.name_space.namespace)

    response = await chat_core.send_message(stranger_info.message_str.strip(), username=stranger_info.nickname)

    await send_msg(
        "NPChat",
        stranger_info,
        npchat,
        response
    )