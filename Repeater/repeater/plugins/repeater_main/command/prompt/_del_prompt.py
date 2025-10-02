from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from ._core import ChatCore, RepeaterDebugMode
from ...assist import StrangerInfo

delprompt = on_command('deletePrompt', aliases={'dp', 'delete_prompt', 'Delete_Prompt', 'DeletePrompt'}, rule=to_me(), block=True)

@delprompt.handle()
async def handle_delete_prompt(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot, event, args)

    msg = stranger_info.message_str.strip()

    
    reply = MessageSegment.reply(event.message_id)
    chat_core = ChatCore(stranger_info.name_space.namespace)
    if RepeaterDebugMode:
        await delprompt.finish(reply + f'[Prompt.Delete_Prompt|{chat_core.name_space}|{stranger_info.nickname}]')
    else:
        code, text = await chat_core.delete_prompt()

        await delprompt.finish(reply + f'====Prompt.Delete_Prompt====\n> {chat_core.name_space}\n{text}\nHTTP Code: {code}')
