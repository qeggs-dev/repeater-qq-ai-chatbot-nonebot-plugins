from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot
from typing import Optional
import asyncio

from .core_config import RepeaterDebugMode

get_session_id = on_command('getSessionId', aliases={'gs', 'get_session_id', 'Get_Session_Id', 'GetSessionId'}, rule=to_me(), block=True)

from .assist_func import get_first_mentioned_user

@get_session_id.handle()
async def handle_get_session_id(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    msg = args.extract_plain_text().strip()
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

    
    reply = MessageSegment.reply(event.message_id)

    if RepeaterDebugMode:
        await get_session_id.finish(reply + f'[Chat.Get_Session_Id|{session_id}|{nickname}]')
    else:
        mentioned_id = await asyncio.to_thread(get_first_mentioned_user, event)
        if mentioned_id is None:
            await get_session_id.finish(reply + f'====Chat.Get_Session_Id====\n> {session_id}')
        else:
            if mode == 'group':
                await get_session_id.finish(reply + f'====Chat.Get_Session_Id====\n> Group:{group_id}:{mentioned_id}')
            else:
                await get_session_id.finish(reply + f'====Chat.Get_Session_Id====\n> Private:{mentioned_id}')