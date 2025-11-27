from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from .._clients import ContextCore, PromptCore, ConfigCore
from ...assist import StrangerInfo, SendMsg

delsession = on_command('delSession', aliases={'ds', 'delete_session', 'Delete_Session', 'DeleteSession'}, rule=to_me(), block=True)

@delsession.handle()
async def handle_delete_session(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot=bot, event=event, args=args)
    sendmsg = SendMsg("Mixed.Delete_Session", delsession, stranger_info)

    context_core = ContextCore(stranger_info)
    prompt_core = PromptCore(stranger_info)
    config_core = ConfigCore(stranger_info)
    if sendmsg.is_debug_mode:
        await sendmsg.send_debug_mode()
    else:
        response_context = await context_core.delete_context()
        response_prompt = await prompt_core.delete_prompt()
        response_config = await config_core.delete_config()
        await sendmsg.send_multiple_responses(
            (response_context, "Context"),
            (response_prompt, "Prompt"),
            (response_config, "Config")
        )