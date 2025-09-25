from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from ._core import ChatCore, RepeaterDebugMode
from ..assist import StrangerInfo

setprompt = on_command('setPrompt', aliases={'sp', 'set_prompt', 'Set_Prompt', 'SetPrompt'}, rule=to_me(), block=True)


@setprompt.handle()
async def handle_setprompt(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot=bot, event=event, args=args)

    msg = stranger_info.message_str.strip()
    
    reply = MessageSegment.reply(event.message_id)
    chat_core = ChatCore(stranger_info.name_space.namespace)
    if RepeaterDebugMode:
        await setprompt.finish(reply + f'[Prompt.Set_Prompt|{chat_core.name_space}]')
    else:
        code, text = await chat_core.set_prompt(msg)

        await setprompt.finish(reply + f'====Prompt.Set_Prompt====\n> {chat_core.name_space}\n{text}\nHTTP Code: {code}')
