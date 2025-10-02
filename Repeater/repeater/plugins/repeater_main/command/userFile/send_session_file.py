from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore, RepeaterDebugMode
from ...assist import StrangerInfo, FileSender

seed_user_data_file = on_command('sendUserDataFile', aliases={'sudf', 'send_user_data_file', 'Send_User_Data_File', 'SendUserDataFile'}, rule=to_me(), block=True)

@seed_user_data_file.handle()
async def handle_send_user_data_file(bot: Bot, event: MessageEvent):
    stranger_info = StrangerInfo(bot=bot, event=event)

    msg = stranger_info.message_str.strip()

    chat_core = ChatCore(stranger_info.namespace_str)
    sfurl = await chat_core.get_user_data_file_url()
    if RepeaterDebugMode:
        await seed_user_data_file.finish(stranger_info.reply + f'[UserDataFile.Send_User_Data_File|{chat_core.name_space}:{sfurl}]')
    else:
        file_sender = FileSender(stranger_info)

        await file_sender.send_file(sfurl, "UserDataFile.zip")
