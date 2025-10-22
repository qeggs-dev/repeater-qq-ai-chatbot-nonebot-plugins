from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .._clients import PromptCore
from ...assist import StrangerInfo, SendMsg

change_prompt_branch = on_command('changePromptBranch', aliases={'cpb', 'change_prompt_branch', 'Change_Prompt_Branch', 'ChangePromptBranch'}, rule=to_me(), block=True)

@change_prompt_branch.handle()
async def handle_change_prompt_branch(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot=bot, event=event, args=args)
    sendmsg = SendMsg("Prompt.Change_Prompt_Branch", change_prompt_branch, stranger_info)

    msg = args.extract_plain_text().strip()
    
    prompt_core = PromptCore(stranger_info.namespace_str)
    if sendmsg.is_debug_mode:
        await sendmsg.send_debug_mode()
    else:
        response = await prompt_core.change_prompt_branch(msg)
        sendmsg.send_response(response, f"Change Prompt Branch to {msg}")