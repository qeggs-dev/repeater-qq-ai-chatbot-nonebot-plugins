from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from .._clients import ContextCore
from ...assist import PersonaInfo, SendMsg

delete_public_space_context = on_command('deletePublicSpaceContext', aliases={'dpsc', 'delete_public_space_context', 'Delete_Public_Space_Context', 'DeletePublicSpaceContext'}, rule=to_me(), block=True)

@delete_public_space_context.handle()
async def handle_delete_public_space_context(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    sendmsg = SendMsg("Context.Delete_Public_Space_Context", delete_public_space_context, persona_info)

    context_core = ContextCore(persona_info)
    if sendmsg.is_debug_mode:
        await sendmsg.send_debug_mode()
    else:
        response = await context_core.delete_context()
        await sendmsg.send_response(response, f"Delete Public Space Context from {persona_info.namespace_str}")