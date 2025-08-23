from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from ._core import ChatCore, RepeaterDebugMode
from ..assist import StrangerInfo

change_default_personality = on_command('changeDefaultPersonality', aliases={'cdp', 'change_default_personality', 'Change_Default_Personality', 'ChangeDefaultPersonality'}, rule=to_me(), block=True)

@change_default_personality.handle()
async def handle_change_default_personality(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot=bot, event=event, args=args)
    
    msg = stranger_info.message_str.strip()
    
    chat_core = ChatCore(stranger_info.name_space.namespace)
    if RepeaterDebugMode:
        await change_default_personality.finish(stranger_info.reply + f'[Chat.Set_Default_Personality|{stranger_info.name_space}]: {msg}')
    else:
        code, text = await chat_core.set_config("parset_prompt_name", msg)

        await change_default_personality.finish(stranger_info.reply + f'====Chat.Set_Default_Personality====\n> {stranger_info.name_space}\n{text}\nHTTP Code: {code}')
