from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from .._clients import ConfigCore
from ...assist import StrangerInfo, SendMsg

change_config_branch = on_command('changeConfigBranch', aliases={'ccfgb', 'change_config_branch', 'Change_Config_Branch', 'ChangeConfigBranch'}, rule=to_me(), block=True)

@change_config_branch.handle()
async def handle_change_config_branch(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot=bot, event=event, args=args)
    send_msg = SendMsg("Config.Change_Config_Branch", change_config_branch, stranger_info)

    config_core = ConfigCore(stranger_info)
    if send_msg.is_debug_mode:
        await send_msg.send_debug_mode()
    else:
        response = await config_core.set_config("new_branch_id", stranger_info.message_str)
        await send_msg.send_response(response, f"Config branch changed to {stranger_info.message_str}")