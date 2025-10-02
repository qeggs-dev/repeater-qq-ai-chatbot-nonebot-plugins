from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from ._core import ChatCore, RepeaterDebugMode
from ...assist import StrangerInfo

change_context_branch = on_command('changeContextBranch', aliases={'ccb', 'change_context_branch', 'Change_Context_Branch', 'ChangeContextBranch'}, rule=to_me(), block=True)

@change_context_branch.handle()
async def handle_change_context_branch(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot=bot, event=event, args=args)
    
    msg = stranger_info.message_str.strip()
    
    reply = MessageSegment.reply(event.message_id)
    chat_core = ChatCore(stranger_info.name_space.namespace)
    if RepeaterDebugMode:
        await change_context_branch.finish(reply + f'[Context.Change_Context_Branch|{chat_core.name_space}|{stranger_info.nickname}]:{msg}')
    else:
        code, text = await chat_core.change_context_branch(msg)

        await change_context_branch.finish(reply + f'====Context.Change_Context_Branch====\n> {chat_core.name_space}\n{text}\nHTTP Code: {code}')