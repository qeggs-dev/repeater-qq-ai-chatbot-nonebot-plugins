from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore, RepeaterDebugMode

delcontext = on_command('deleteContext', aliases={'dc', 'delete_context', 'Delete_Context', 'DeleteContext'}, rule=to_me(), block=True)

@delcontext.handle()
async def handle_delete_context(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    try:
        whatever, group_id, user_id = event.get_session_id().split('_')  # 获取当前群聊id，发起人id，返回的格式为group_groupid_userid
        context_id = f"Group:{group_id}:{user_id}"
    except:  # 如果上面报错了，意味着发起的是私聊，返回格式为userid
        group_id = None
        user_id = event.get_session_id()
        context_id = f"Private:{user_id}"
    result = await bot.get_stranger_info(user_id=user_id)
    nickname = result['nickname']

    
    reply = MessageSegment.reply(event.message_id)
    chat_core = ChatCore(context_id)
    if RepeaterDebugMode:
        await delcontext.finish(reply + f'[Chat.Delete_Context|{context_id}|{nickname}]')
    else:
        code, text = await chat_core.delete_context()

        await delcontext.finish(reply + f'====Chat.Delete_Context====\n> {context_id}\n{text}\nHTTP Code: {code}')


delcontext = on_command('delSubContext', aliases={'dsc', 'delete_sub_context', 'Delete_Sub_Context', 'DeleteSubContext'}, rule=to_me(), block=True)

@delcontext.handle()
async def handle_delete_sub_context(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    try:
        whatever, group_id, user_id = event.get_session_id().split('_')  # 获取当前群聊id，发起人id，返回的格式为group_groupid_userid
        context_id = f"Group:{group_id}:{user_id}"
    except:  # 如果上面报错了，意味着发起的是私聊，返回格式为userid
        group_id = None
        user_id = event.get_session_id()
        context_id = f"Private:{user_id}"
    result = await bot.get_stranger_info(user_id=user_id)
    nickname = result['nickname']

    
    reply = MessageSegment.reply(event.message_id)
    chat_core = ChatCore(context_id)
    if RepeaterDebugMode:
        await delcontext.finish(reply + f'[Chat.Delete_Context|{context_id}|{nickname}]')
    else:
        code, text = await chat_core.delete_subcontext()

        await delcontext.finish(reply + f'====Chat.Delete_Context====\n> {context_id}\n{text}\nHTTP Code: {code}')