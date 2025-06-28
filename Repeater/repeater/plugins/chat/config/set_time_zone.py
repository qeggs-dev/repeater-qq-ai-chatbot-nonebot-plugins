from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore, RepeaterDebugMode

set_time_zone = on_command('setTimeZone', aliases={'stz', 'set_time_zone', 'Set_Time_Zone', 'SetTimeZone'}, rule=to_me(), block=True)

@set_time_zone.handle()
async def handle_set_time_zone(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
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

    try:
        time_zone = float(msg)
    except ValueError:
        if time_zone < -12 or time_zone > 12:
            await set_time_zone.finish(
                '====Chat.Set_Time_Zone====\n> 时区设置错误，请输入-12~12之间的浮点数'
            )
        time_zone = 0


    reply = MessageSegment.reply(event.message_id)
    chat_core = ChatCore(session_id)
    if RepeaterDebugMode:
        await set_time_zone.finish(reply + f'[Chat.Set_Time_Zone|{session_id}|{nickname}]:{msg}')
    else:
        code, text = await chat_core.set_time_zone(timezone=time_zone)

        await set_time_zone.finish(reply + f'====Chat.Set_Time_Zone====\n> {session_id}\n{text}\nHTTP Code: {code}\n\nTime_Zone: UTC{"" if time_zone < 0 else "+"}{time_zone}')