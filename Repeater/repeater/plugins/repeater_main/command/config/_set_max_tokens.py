from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from ._core import ChatCore, RepeaterDebugMode
from ...assist import StrangerInfo

set_max_tokens = on_command('setMaxTokens', aliases={'smt', 'set_max_tokens', 'Set_Max_Tokens', 'SetMaxTokens'}, rule=to_me(), block=True)

@set_max_tokens.handle()
async def handle_set_max_tokens(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot=bot, event=event, args=args)

    msg = stranger_info.message_str.strip()
    reply = MessageSegment.reply(event.message_id)

    try:
        max_tokens = int(msg)
    except ValueError:
        await set_max_tokens.finish(
            reply +
            '====Chat.Set_Max_Tokens====\n> Max_Tokens设置错误，请输入整数'
        )
        
    if max_tokens < 1 or max_tokens > 8192:
        await max_tokens.finish(
            reply +
            '====Chat.Set_Max_Tokens====\n> Max_Tokens设置错误，请输入整数'
        )


    chat_core = ChatCore(stranger_info.namespace_str)
    if RepeaterDebugMode:
        await set_max_tokens.finish(reply + f'[Chat.Set_Max_Tokens|{chat_core.name_space}|{stranger_info.nickname}]:{msg}')
    else:
        code, text = await chat_core.set_config("max_tokens", max_tokens)

        await set_max_tokens.finish(reply + f'====Chat.Set_Max_Tokens====\n> {chat_core.name_space}\nHTTP Code: {code}\n\nMax_Tokens: {max_tokens}')