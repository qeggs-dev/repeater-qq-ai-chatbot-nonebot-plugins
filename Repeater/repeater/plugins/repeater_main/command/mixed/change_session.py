from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from .._clients import ContextCore, PromptCore, ConfigCore
from ...assist import StrangerInfo, SendMsg

change_session = on_command('changeSession', aliases={'cs', 'change_session', 'Change_Session', 'ChangeSession'}, rule=to_me(), block=True)

@change_session.handle()
async def handle_change_session(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot=bot, event=event, args=args)
    sendmsg = SendMsg("Mixed.Change_Session", change_session, stranger_info)

    context_core = ContextCore(stranger_info)
    prompt_core = PromptCore(stranger_info)
    config_core = ConfigCore(stranger_info)
    if sendmsg.is_debug_mode:
        await sendmsg.send_debug_mode()
    else:
        response_context = await context_core.change_context_branch(
            stranger_info.message_str
        )
        response_prompt = await prompt_core.change_prompt_branch(
            stranger_info.message_str
        )
        response_config = await config_core.change_config_branch(
            stranger_info.message_str
        )
        await sendmsg.send_multiple_responses(
            (response_context, "Context"),
            (response_prompt, "Prompt"),
            (response_config, "Config")
        )