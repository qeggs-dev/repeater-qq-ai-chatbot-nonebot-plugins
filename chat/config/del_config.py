from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore, RepeaterDebugMode

del_config = on_command('delConfig', aliases={'dcfg', 'delete_config', 'Delete_Config', 'DeleteConfig'}, rule=to_me(), block=True)

@del_config.handle()
async def handle_del_config(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
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
        await del_config.finish(reply + f'[Chat.Delete_Config|{session_id}|{nickname}]:{msg}')
    else:
        code, text = await chat_core.delete_config()

        await del_config.finish(reply + f'====Chat.Delete_Config====\n> {session_id}\n{text}\nHTTP Code: {code}\n')

delsubconfig = on_command('delSubConfig', aliases={'dsc', 'delete_sub_config', 'Delete_Sub_Config', 'DeleteSubConfig'}, rule=to_me(), block=True)

@delsubconfig.handle()
async def handle_delete_sub_config(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
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
        await delsubconfig.finish(reply + f'[Chat.Delete_Config|{session_id}|{nickname}]')
    else:
        code, text = await chat_core.delete_subconfig()

        await delsubconfig.finish(reply + f'====Chat.Delete_Config====\n> {session_id}\n{text}\nHTTP Code: {code}')
