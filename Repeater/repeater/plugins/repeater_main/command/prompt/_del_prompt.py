from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .._clients import PromptCore
from ...assist import StrangerInfo, SendMsg

delprompt = on_command('deletePrompt', aliases={'dp', 'delete_prompt', 'Delete_Prompt', 'DeletePrompt'}, rule=to_me(), block=True)

@delprompt.handle()
async def handle_delete_prompt(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot, event, args)
    sendmsg = SendMsg("Chat.Delete_Prompt", delprompt, stranger_info)
    
    chat_core = PromptCore(stranger_info.namespace_str)
    if sendmsg.is_debug_mode:
        await sendmsg.send_debug_mode()
    else:
        response = await chat_core.delete_prompt()
        await sendmsg.send_response(response, f"Delete Prompt from {stranger_info.namespace_str}")
