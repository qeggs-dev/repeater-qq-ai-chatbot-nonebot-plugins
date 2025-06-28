from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore, RepeaterDebugMode

seed_session_file = on_command('sendSeessionFile', aliases={'ssf', 'send_session_file', 'Send_Session_File', 'SendSessionFile'}, rule=to_me(), block=True)

@seed_session_file.handle()
async def handle_send_session_file(bot: Bot, event: MessageEvent):
    msg = event.get_plaintext().strip()
    reply = MessageSegment.reply(event.message_id) # 获取回复消息头
    if msg:
        try:
            whatever, group_id, user_id = event.get_session_id().split('_')  # 获取当前群聊id，发起人id，返回的格式为group_groupid_userid
            session_id = f"Group:{group_id}:{user_id}"
            mode = "group"
        except:  # 如果上面报错了，意味着发起的是私聊，返回格式为userid
            group_id = None
            user_id = event.get_session_id()
            session_id = f"Private:{user_id}"
            mode = "private"
        result = await bot.get_stranger_info(user_id=user_id)
        nickname = result['nickname']

        chat_core = ChatCore(session_id)
        sfurl = await chat_core.get_session_file_url()
        if RepeaterDebugMode:
            await seed_session_file.finish(reply + f'[Chat.Download_Session|{session_id}:{sfurl}]')
        else:
            if mode == "group":
                data = {
                  "group_id": group_id,
                  "file": sfurl,
                  "name": f"Group_{group_id}_{user_id}.zip",
                  "folder_id": None
                }
                await bot.upload_group_file(**data)
            elif mode == "private":
                data = {
                    "user_id": user_id,
                    "file": sfurl,
                    "name": f"Private_{user_id}.zip"
                }
                await bot.upload_private_file(**data)
