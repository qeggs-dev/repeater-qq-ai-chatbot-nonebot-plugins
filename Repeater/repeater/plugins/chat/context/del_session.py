from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from ._core import ChatCore, RepeaterDebugMode

delsession = on_command('delSession', aliases={'ds', 'delete_session', 'Delete_Session', 'DeleteSession'}, rule=to_me(), block=True)

@delsession.handle()
async def handle_delete_session(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
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
        await delsession.finish(reply + f'[Chat.Delete_Session|{session_id}|{nickname}]')
    else:
        code, text = await chat_core.delete_session()

        await delsession.finish(reply + f'====Chat.Delete_Session====\n> {session_id}\n{text}\nHTTP Code: {code}')