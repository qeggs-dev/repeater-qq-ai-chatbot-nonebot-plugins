from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core_config import *

seed_readme_file = on_command('sendReadmeFile', aliases={'srf', 'send_readme_file', 'Send_Readme_File', 'SendReadmeFile'}, rule=to_me(), block=True)

@seed_readme_file.handle()
async def handle_send_readme_file(bot: Bot, event: MessageEvent):
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

        sfurl = f'{CHAT_API}:{CHAT_PORT}/{HTML_README_FILE_ROUTE}'
        if RepeaterDebugMode:
            await seed_readme_file.finish(reply + f'[Chat.Send_Readme_File|{session_id}:{sfurl}]')
        else:
            if mode == "group":
                data = {
                  "group_id": group_id,
                  "file": sfurl,
                  "name": f"Repeater_Readme.html",
                  "folder_id": None
                }
                await bot.upload_group_file(**data)
            elif mode == "private":
                data = {
                    "user_id": user_id,
                    "file": sfurl,
                    "name": f"Repeater_Readme.html"
                }
                await bot.upload_private_file(**data)