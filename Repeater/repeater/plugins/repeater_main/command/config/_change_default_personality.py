from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from .._clients import ConfigCore
from ...assist import StrangerInfo, SendMsg

change_default_personality = on_command('changeDefaultPersonality', aliases={'cdp', 'change_default_personality', 'Change_Default_Personality', 'ChangeDefaultPersonality'}, rule=to_me(), block=True)

@change_default_personality.handle()
async def handle_change_default_personality(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot=bot, event=event, args=args)
    sendmsg = SendMsg("Chat.Change_Default_Personality", change_default_personality, stranger_info)
    
    chat_core = ConfigCore(stranger_info)
    if sendmsg.is_debug_mode:
        await sendmsg.send_debug_mode()
    else:
        response = await chat_core.set_config("parset_prompt_name", stranger_info.message_str)
        await sendmsg.send_response(response, f"Change Default Personality to {stranger_info.message_str}")
        
