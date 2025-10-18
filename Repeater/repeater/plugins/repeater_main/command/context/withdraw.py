from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .._clients import ContextCore
from ...assist import StrangerInfo, SendMsg

withdraw = on_command('withdraw', aliases={'w', 'Withdraw'}, rule=to_me(), block=True)

@withdraw.handle()
async def handle_withdraw(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot=bot, event=event, args=args)
    sendmsg = SendMsg("Chat.Withdraw", withdraw, stranger_info)

    chat_core = ContextCore(stranger_info.namespace_str)
    if sendmsg.is_debug_mode:
        await sendmsg.send_debug_mode()
    else:
        response = await chat_core.withdraw()

        if response.code == 200:
            await sendmsg.send_prompt(
                f"Deleted: {response.data.deleted}\n"
                f"Remaining: {len(response.data.context)}\n"
            )
            
        else:
            await sendmsg.send_response(response, "Withdraw Failed")
