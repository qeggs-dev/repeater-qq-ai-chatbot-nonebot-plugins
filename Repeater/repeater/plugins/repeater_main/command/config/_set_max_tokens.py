from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from .._core import ConfigCore
from ...assist import StrangerInfo, SendMsg

set_max_tokens = on_command('setMaxTokens', aliases={'smt', 'set_max_tokens', 'Set_Max_Tokens', 'SetMaxTokens'}, rule=to_me(), block=True)

@set_max_tokens.handle()
async def handle_set_max_tokens(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot=bot, event=event, args=args)
    sendmsg = SendMsg("Chat.Set_Max_Tokens", stranger_info, set_max_tokens, None)

    msg = stranger_info.message_str.strip()

    try:
        max_tokens = int(msg)
    except ValueError:
        await sendmsg.send_error("Max_Tokens setting is incorrect, please enter an integer!")
        
    if max_tokens < 1 or max_tokens > 8192:
        await sendmsg.send_error("Max_Tokens setting is incorrect, please enter an integer between 1 and 8192!")


    chat_core = ConfigCore(stranger_info)
    if sendmsg.is_debug_mode:
        await sendmsg.send_debug_mode()
    else:
        response = await chat_core.set_config("max_tokens", max_tokens)
        await sendmsg.send_response(response, f"Set Max_Tokens to {max_tokens}")