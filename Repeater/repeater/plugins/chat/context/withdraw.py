from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore, RepeaterDebugMode
from ..assist import StrangerInfo

withdraw = on_command('withdraw', aliases={'w', 'Withdraw'}, rule=to_me(), block=True)


@withdraw.handle()
async def handle_withdraw(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot=bot, event=event, args=args)

    msg = stranger_info.message_str.strip()

    chat_core = ChatCore(stranger_info.name_space.namespace)
    if RepeaterDebugMode:
        await withdraw.finish(stranger_info.reply + f'[Chat.Withdraw|{chat_core.name_space}|{stranger_info.nickname}]')
    else:
        response_code, response_text = await chat_core.withdraw()

        await withdraw.finish(stranger_info.reply + f'====Chat.Withdraw====\n> {chat_core.name_space}\n{response_text}\nHTTP Code: {response_code}')
