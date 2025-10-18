from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from .._clients import ContextCore
from ...assist import StrangerInfo, SendMsg

change_context_branch = on_command('changeContextBranch', aliases={'ccb', 'change_context_branch', 'Change_Context_Branch', 'ChangeContextBranch'}, rule=to_me(), block=True)

@change_context_branch.handle()
async def handle_change_context_branch(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot=bot, event=event, args=args)
    sendmsg = SendMsg("Chat.Change_Context_Branch", change_context_branch, stranger_info)
    
    msg = stranger_info.message_str.strip()
    
    chat_core = ContextCore(stranger_info)
    if sendmsg.is_debug_mode:
        await sendmsg.send_debug_mode()
    else:
        response = await chat_core.change_context_branch(msg)
        await sendmsg.send_response(response, f"Change Context Branch to {msg}")