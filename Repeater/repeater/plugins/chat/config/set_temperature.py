from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore, RepeaterDebugMode

set_temperature = on_command('setTemperature', aliases={'st', 'set_temperature', 'Set_Temperature', 'SetTemperature'}, rule=to_me(), block=True)

@set_temperature.handle()
async def handle_set_temperature(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
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
            temperature = (float(msg) / 100) + 1
        else:
            temperature = float(msg)
    except ValueError:
        await set_temperature.finish(
            '====Chat.Set_Temperature====\n> 温度设置错误，请输入0~2之间的浮点数'
        )
    if temperature < 0 or temperature > 2:
        await set_temperature.finish(
            '====Chat.Set_Temperature====\n> 温度设置错误，请输入0~2之间的浮点数'
        )


    reply = MessageSegment.reply(event.message_id)
    chat_core = ChatCore(session_id)
    if RepeaterDebugMode:
        await set_temperature.finish(reply + f'[Chat.Set_Temperature|{session_id}|{nickname}]:{msg}')
    else:
        code, text = await chat_core.set_temperature(temperature=temperature)

        await set_temperature.finish(reply + f'====Chat.Set_Temperature====\n> {session_id}\n{text}\nHTTP Code: {code}\n\nTemperature: {temperature}')