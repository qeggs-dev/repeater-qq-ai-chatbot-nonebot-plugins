from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .._core import ConfigCore
from ...assist import StrangerInfo, SendMsg

set_temperature = on_command('setTemperature', aliases={'st', 'set_temperature', 'Set_Temperature', 'SetTemperature'}, rule=to_me(), block=True)

@set_temperature.handle()
async def handle_set_temperature(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot=bot, event=event, args=args)
    sendmsg = SendMsg("Chat.Set_Temperature", set_temperature, stranger_info)

    msg = stranger_info.message_str.strip()

    try:
        if msg.endswith("%"):
            msg = msg[:-1]
            temperature = (float(msg) / 100) + 1
        else:
            temperature = float(msg)
    except ValueError:
        await sendmsg.send_error("Temperature is set incorrectly. Please enter a floating-point number or percentage between 0 and 2!")
    if temperature < 0 or temperature > 2:
        await sendmsg.send_error("Temperature is set incorrectly. Please enter a floating-point number or percentage between 0 and 2!")

    chat_core = ConfigCore(stranger_info)
    if sendmsg.is_debug_mode:
        await sendmsg.send_debug_mode()
    else:
        response = await chat_core.set_config("temperature", temperature)
        await sendmsg.send_response(response, f"Set Temperature to {temperature}")