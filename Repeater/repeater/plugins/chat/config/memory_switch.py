from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore, RepeaterDebugMode

enable_memory = on_command('enableMemory', aliases={'enm', 'enable_memory', 'Enable_Memory', 'EnableMemory'}, rule=to_me(), block=True)

@enable_memory.handle()
async def handle_enable_memory(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
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
        await enable_memory.finish(reply + f'[Chat.Enable_Memory|{session_id}|{nickname}]:{msg}')
    else:
        code, text = await chat_core.enable_memory()

        await enable_memory.finish(reply + f'====Chat.Enable_Memory====\n> {session_id}\n{text}\nHTTP Code: {code}')

disable_memory = on_command('disableMemory', aliases={'dim', 'disable_memory', 'Disable_Memory', 'DisableMemory'}, rule=to_me(), block=True)

@disable_memory.handle()
async def handle_disable_memory(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
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
        await disable_memory.finish(reply + f'[Chat.Disable_Memory|{session_id}|{nickname}]:{msg}')
    else:
        code, text = await chat_core.disable_memory()

        await disable_memory.finish(reply + f'====Chat.Disable_Memory====\n> {session_id}\n{text}\nHTTP Code: {code}')