from ...assist import StrangerInfo
from ...chattts import ChatTTSAPI
from .core import ChatCore, Send_msg
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message
from nonebot.params import CommandArg

api = ChatTTSAPI()

tts_chat = on_command('tts_chat', aliases={'ttsc', 'tts_Chat', 'TTS_Chat'}, rule=to_me(), block=True)

@tts_chat.handle()
async def handle_tts_chat(bot: Bot, event: MessageEvent, args: Message = CommandArg()) -> None:
    stranger_info = StrangerInfo(bot, event, args)

    core = ChatCore(stranger_info)

    response = await core.send_message(
        message = stranger_info.message_str
    )

    send_msg = Send_msg(
        "TTS_Chat",
        stranger_info = stranger_info,
        matcher = tts_chat,
        response = response
    )
    await send_msg.send_tts(send_picture_first=True)