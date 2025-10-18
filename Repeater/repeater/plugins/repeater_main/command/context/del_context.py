from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from .._clients import ContextCore
from ...assist import StrangerInfo, SendMsg

delcontext = on_command('deleteContext', aliases={'dc', 'delete_context', 'Delete_Context', 'DeleteContext'}, rule=to_me(), block=True)

@delcontext.handle()
async def handle_delete_context(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot=bot, event=event, args=args)
    sendmsg = SendMsg("Chat.Delete_Context", delcontext, stranger_info)
    
    chat_core = ContextCore(stranger_info.namespace_str)
    if sendmsg.is_debug_mode:
        await sendmsg.send_debug_mode()
    else:
        response = await chat_core.delete_context()
        await sendmsg.send_response(response, f"Delete Context from {stranger_info.namespace_str}")