from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from .._clients import ContextCore
from ...assist import StrangerInfo, SendMsg

delsession = on_command('delSession', aliases={'ds', 'delete_session', 'Delete_Session', 'DeleteSession'}, rule=to_me(), block=True)

@delsession.handle()
async def handle_delete_session(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot=bot, event=event, args=args)
    sendmsg = SendMsg("Chat.Delete_Session", delsession, stranger_info)

    chat_core = ContextCore(stranger_info)
    if sendmsg.is_debug_mode:
        await sendmsg.send_debug_mode()
    else:
        response = await chat_core.delete_session()
        await sendmsg.send_response(response, f"Delete Session from {stranger_info.namespace_str}")