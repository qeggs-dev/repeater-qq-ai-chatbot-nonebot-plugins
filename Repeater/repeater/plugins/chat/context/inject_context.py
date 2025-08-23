from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore, RepeaterDebugMode
from ..assist import StrangerInfo

inject_context = on_command('injectContext', aliases={'ic', 'inject_context', 'Inject_Context', 'InjectContext'}, rule=to_me(), block=True)


@inject_context.handle()
async def handle_inject_context(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot=bot, event=event, args=args)

    msg = stranger_info.message_str.strip()

    
    reply = MessageSegment.reply(event.message_id)
    chat_core = ChatCore(stranger_info.name_space.namespace)
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
        await inject_context.finish(reply + f'[Chat.Inject_Context|{chat_core.name_space}|{stranger_info.nickname}]')
    else:
        response_code, response_text = await chat_core.inject_context(text=text, role=role)

        await inject_context.finish(reply + f'====Chat.Inject_Context====\n> {chat_core.name_space}\nROLE: {role} (user/assistant/system)\n{response_text}\nHTTP Code: {response_code}')
