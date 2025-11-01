from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .._clients import UserFileCore
from ...assist import StrangerInfo, FileSender, SendMsg

send_user_data_file = on_command('sendUserDataFile', aliases={'sudf', 'send_user_data_file', 'Send_User_Data_File', 'SendUserDataFile'}, rule=to_me(), block=True)

@send_user_data_file.handle()
async def handle_send_user_data_file(bot: Bot, event: MessageEvent):
    stranger_info = StrangerInfo(bot=bot, event=event)
    sendmsg = SendMsg("UserFile.Send_User_Data_File", send_user_data_file, stranger_info)

    user_file_core = UserFileCore(stranger_info)
    sfurl = await user_file_core.get_user_data_file_url()
    if sendmsg.is_debug_mode:
        await sendmsg.send_debug_mode()
    else:
        file_sender = FileSender(stranger_info)

        await file_sender.send_file(sfurl, f"{stranger_info.namespace_str}_UserDataFile.zip")
