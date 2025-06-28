from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore, RepeaterDebugMode

set_frequency_penalty = on_command('setFrequencyPenalty', aliases={'sfp', 'set_frequency_penalty', 'Set_Frequency_Penalty', 'SetFrequencyPenalty'}, rule=to_me(), block=True)

@set_frequency_penalty.handle()
async def handle_set_frequency_penalty(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
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
        if msg.endswith("%"):
            msg = msg[:-1]
            frequency_penalty = float(msg) / 100
        else:
            frequency_penalty = float(msg)
    except ValueError:
        await set_frequency_penalty.finish(
            '====Chat.Set_Frequency_Penalty====\n> 频率惩罚设置错误，请输入-2~2之间的浮点数'
        )
    if frequency_penalty < -2 or frequency_penalty > 2:
        await set_frequency_penalty.finish(
            '====Chat.Set_Frequency_Penalty====\n> 频率惩罚设置错误，请输入-2~2之间的浮点数'
        )


    reply = MessageSegment.reply(event.message_id)
    chat_core = ChatCore(session_id)
    if RepeaterDebugMode:
        await set_frequency_penalty.finish(reply + f'[Chat.Set_Frequency_Penalty|{session_id}|{nickname}]:{msg}')
    else:
        code, text = await chat_core.set_frequency_penalty(frequency_penalty=frequency_penalty)

        await set_frequency_penalty.finish(reply + f'====Chat.Set_Frequency_Penalty====\n> {session_id}\n{text}\nHTTP Code: {code}\n\nFrequency_Penalty: {frequency_penalty}')