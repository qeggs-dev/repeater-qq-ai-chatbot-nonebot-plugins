from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore, RepeaterDebugMode

set_top_p = on_command('setTopP', aliases={'stp', 'set_top_p', 'Set_Top_P', 'SetTopP'}, rule=to_me(), block=True)

@set_top_p.handle()
async def handle_set_top_p(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
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

    try:
        if msg.endswith("%"):
            msg = msg[:-1]
            top_p = float(msg) / 100
        else:
            top_p = float(msg)
    except ValueError:
        await set_top_p.finish(
            '====Chat.Set_Top_P====\n> Top_P设置错误，请输入0~1之间的浮点数'
        )
    if top_p < -2 or top_p > 2:
        await set_top_p.finish(
            '====Chat.Set_Top_P====\n> Top_P设置错误，请输入0~1之间的浮点数'
        )


    reply = MessageSegment.reply(event.message_id)
    chat_core = ChatCore(session_id)
    if RepeaterDebugMode:
        await set_top_p.finish(reply + f'[Chat.Set_Top_P|{session_id}|{nickname}]:{msg}')
    else:
        code, text = await chat_core.set_top_p(top_p=top_p)

        await set_top_p.finish(reply + f'====Chat.Set_Top_P====\n> {session_id}\n{text}\nHTTP Code: {code}\n\nTop_P: {top_p}')