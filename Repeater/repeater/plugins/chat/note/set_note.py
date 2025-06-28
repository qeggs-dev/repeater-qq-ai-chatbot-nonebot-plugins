from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore, RepeaterDebugMode

setnote = on_command('setNote', aliases={'sn', 'set_note', 'Set_Note', 'SetNote'}, rule=to_me(), block=True)


@setnote.handle()
async def handle_set_note(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    msg = args.extract_plain_text()
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
        await setnote.finish(reply + f'[Chat.Set_Note|{session_id}]')
    else:
        code, text = await chat_core.set_note(msg)

        await setnote.finish(reply + f'====Chat.Set_Note====\n> {session_id}\n{text}\nHTTP Code: {code}')
