from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore, RepeaterDebugMode

delprompt = on_command('deletePrompt', aliases={'dp', 'delete_prompt', 'Delete_Prompt', 'DeletePrompt'}, rule=to_me(), block=True)

@delprompt.handle()
async def handle_delete_prompt(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
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
        await delprompt.finish(reply + f'[Chat.Delete_Prompt|{session_id}|{nickname}]')
    else:
        code, text = await chat_core.delete_prompt()

        await delprompt.finish(reply + f'====Chat.Delete_Prompt====\n> {session_id}\n{text}\nHTTP Code: {code}')

delsubprompt = on_command('delSubPrompt', aliases={'dsp', 'delete_sub_prompt', 'Delete_Sub_Prompt', 'DeleteSubPrompt'}, rule=to_me(), block=True)

@delsubprompt.handle()
async def handle_delete_sub_prompt(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
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
        await delsubprompt.finish(reply + f'[Chat.Delete_Prompt|{session_id}|{nickname}]')
    else:
        code, text = await chat_core.delete_subprompt()

        await delsubprompt.finish(reply + f'====Chat.Delete_Prompt====\n> {session_id}\n{text}\nHTTP Code: {code}')
