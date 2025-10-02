from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from ._core import ChatCore, RepeaterDebugMode
from ...assist import StrangerInfo

change_config_branch = on_command('changeConfigBranch', aliases={'ccfgb', 'change_config_branch', 'Change_Config_Branch', 'ChangeConfigBranch'}, rule=to_me(), block=True)

@change_config_branch.handle()
async def handle_change_config_branch(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot=bot, event=event, args=args)
    
    msg = stranger_info.message_str.strip()
    
    reply = MessageSegment.reply(event.message_id)
    chat_core = ChatCore(stranger_info.namespace_str)
    if RepeaterDebugMode:
        await change_config_branch.finish(reply + f'[Chat.Change_Config_Branch|{chat_core.name_space}|{stranger_info.nickname}]:{msg}')
    else:
        code, text = await chat_core.set_config("new_branch_id", msg)

        await change_config_branch.finish(reply + f'====Chat.Change_Config_Branch====\n> {chat_core.name_space}\nHTTP Code: {code}')