from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .._clients import PromptCore
from ...assist import StrangerInfo, SendMsg

setprompt = on_command('setPrompt', aliases={'sp', 'set_prompt', 'Set_Prompt', 'SetPrompt'}, rule=to_me(), block=True)


@setprompt.handle()
async def handle_setprompt(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot=bot, event=event, args=args)
    sendmsg = SendMsg("Prompt.Set_Prompt", setprompt, stranger_info)

    msg = stranger_info.message_str.strip()
    
    chat_core = PromptCore(stranger_info)
    if sendmsg.is_debug_mode:
        await sendmsg.send_debug_mode()
    else:
        response = await chat_core.set_prompt(msg)
        await sendmsg.send_response(response, f"Set Prompt{'successfully' if response.code == 200 else 'failed'}")
