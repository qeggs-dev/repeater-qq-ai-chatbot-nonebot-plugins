from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore, RepeaterDebugMode

get_context_total_length = on_command('getContextTotalLength', aliases={'gctl', 'get_context_total_length', 'Get_Context_Total_Length', 'GetContextTotalLength'}, rule=to_me(), block=True)

@get_context_total_length.handle()
async def handle_total_context_length(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
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
        await get_context_total_length.finish(reply + f'[Chat.Get_Context_Total_Length|{session_id}|{nickname}]')
    else:
        code, body = await chat_core.get_context_total_length()

        await get_context_total_length.finish(reply + f'====Chat.Get_Context_Total_Length====\n> {session_id}\nlength:{body.get("context_length", "0")}\ntotal_text_length:{body.get("total_context_length", "0")}\nHTTP Code: {code}')