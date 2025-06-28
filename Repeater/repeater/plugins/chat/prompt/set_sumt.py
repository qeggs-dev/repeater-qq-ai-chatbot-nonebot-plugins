from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore, RepeaterDebugMode

set_sumt = on_command('setNicknameMappingFromUsername', aliases={'snmu', 'set_nickname_mapping_from_username', 'Set_Nickname_Mapping_From_Username', 'SetNicknameMappingFromUsername'}, rule=to_me(), block=True)

@set_sumt.handle()
async def handle_snmu(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    msg =  args.extract_plain_text().strip()
    try:
        whatever, group_id, user_id = event.get_session_id().split('_')  # 获取当前群聊id，发起人id，返回的格式为group_groupid_userid
        session_id = f"Group:{group_id}:{user_id}"
    except:  # 如果上面报错了，意味着发起的是私聊，返回格式为userid
        group_id = None
        user_id = event.get_session_id()
        session_id = f"Private:{user_id}"
    result = await bot.get_stranger_info(user_id=user_id)
    nickname = result['nickname']
    
    reply = MessageSegment.reply(event.message_id)
    chat_core = ChatCore(session_id)
    if RepeaterDebugMode:
        await set_sumt.finish(reply + f'[Chat.Set_SUMT_From_Username|{session_id}|{nickname}]:{msg}')
    else:
        code, text = await chat_core.set_usmt(nickname, msg)

        await set_sumt.finish(reply + f'====Chat.Set_SUMT_From_Username====\n> {session_id}\n{text}\nHTTP Code: {code}\n')
        
set_sumt = on_command('setNicknameMappingFromSessionID', aliases={'snms', 'set_nickname_mapping_from_session_id', 'Set_Nickname_Mapping_From_SessionID', 'SetNicknameMappingFromSessionID'}, rule=to_me(), block=True)

@set_sumt.handle()
async def handle_snms(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    msg =  args.extract_plain_text().strip()
    try:
        whatever, group_id, user_id = event.get_session_id().split('_')  # 获取当前群聊id，发起人id，返回的格式为group_groupid_userid
        session_id = f"Group:{group_id}:{user_id}"
    except:  # 如果上面报错了，意味着发起的是私聊，返回格式为userid
        group_id = None
        user_id = event.get_session_id()
        session_id = f"Private:{user_id}"
    result = await bot.get_stranger_info(user_id=user_id)
    nickname = result['nickname']
    
    reply = MessageSegment.reply(event.message_id)
    chat_core = ChatCore(session_id)
    if RepeaterDebugMode:
        await set_sumt.finish(reply + f'[Chat.Set_SUMT_From_Username|{session_id}|{nickname}]:{msg}')
    else:
        code, text = await chat_core.set_usmt(session_id, msg)

        await set_sumt.finish(reply + f'====Chat.Set_SUMT_From_Username====\n> {session_id}\n{text}\nHTTP Code: {code}\n')