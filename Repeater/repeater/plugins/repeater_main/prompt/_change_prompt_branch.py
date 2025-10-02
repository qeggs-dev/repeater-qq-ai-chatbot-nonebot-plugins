from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from ._core import ChatCore, RepeaterDebugMode
from ..assist import StrangerInfo

change_prompt_branch = on_command('changePromptBranch', aliases={'cpb', 'change_prompt_branch', 'Change_Prompt_Branch', 'ChangePromptBranch'}, rule=to_me(), block=True)

@change_prompt_branch.handle()
async def handle_change_prompt_branch(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot=bot, event=event, args=args)

    msg = args.extract_plain_text().strip()
    
    reply = MessageSegment.reply(event.message_id)
    chat_core = ChatCore(stranger_info.name_space.namespace)
    if RepeaterDebugMode:
        await change_prompt_branch.finish(reply + f'[Prompt.Change_Prompt_Branch|{chat_core.name_space}|{stranger_info.nickname}]: {msg}')
    else:
        code, text = await chat_core.change_prompt_branch(msg)

        await change_prompt_branch.finish(reply + f'====Prompt.Change_Prompt_Branch====\n> {chat_core.name_space}\n{text}\nHTTP Code: {code}')