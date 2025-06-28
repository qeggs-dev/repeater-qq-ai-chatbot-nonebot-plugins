from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore, RepeaterDebugMode

inject_context = on_command('injectContext', aliases={'ic', 'inject_context', 'Inject_Context', 'InjectContext'}, rule=to_me(), block=True)


@inject_context.handle()
async def handle_inject_context(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    msg = args.extract_plain_text().strip()
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
    if ':' in msg:
        role = msg.split(':', 1)[0]
    elif '：' in msg:
        role = msg.split('：', 1)[0]
    else:
        role = 'user'
        
    if role not in {'user', 'assistant', 'system'}:
        role = 'invalid'
    
    if ':' in msg:
        text = msg.split(':', 1)[1]
    elif '：' in msg:
        text = msg.split('：', 1)[1]
    else:
        text = msg

    if RepeaterDebugMode:
        await inject_context.finish(reply + f'[Chat.Inject_Context|{session_id}|{nickname}]')
    else:
        response_code, response_text = await chat_core.inject_context(text=text, role=role)

        await inject_context.finish(reply + f'====Chat.Inject_Context====\n> {session_id}\nROLE: {role} (user/assistant/system)\n{response_text}\nHTTP Code: {response_code}')
