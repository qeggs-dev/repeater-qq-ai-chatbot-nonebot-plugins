from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from ._core import ChatCore, RepeaterDebugMode
from ..assist import StrangerInfo

set_temperature = on_command('setTemperature', aliases={'st', 'set_temperature', 'Set_Temperature', 'SetTemperature'}, rule=to_me(), block=True)

@set_temperature.handle()
async def handle_set_temperature(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot=bot, event=event, args=args)

    msg = stranger_info.message_str.strip()

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
    chat_core = ChatCore(stranger_info.name_space.namespace)
    if RepeaterDebugMode:
        await set_temperature.finish(reply + f'[Chat.Set_Temperature|{chat_core.name_space}|{set_temperature.nickname}]:{msg}')
    else:
        code, text = await chat_core.set_config("temperature", temperature)

        await set_temperature.finish(reply + f'====Chat.Set_Temperature====\n> {chat_core.name_space}\nHTTP Code: {code}\n\nTemperature: {temperature}')