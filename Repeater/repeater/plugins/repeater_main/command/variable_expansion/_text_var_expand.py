from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .._clients import VariableExpansionCore
from ...assist import StrangerInfo, SendMsg

var_Expand = on_command("varExpandText", aliases={"vet", "var_expand_text", "Var_Expand_Text", "VarExpandText"}, rule=to_me(), block=True)

@var_Expand.handle()
async def handle_var_expand(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot=bot, event=event, args=args)
    sendmsg = SendMsg("VarExpandText", var_Expand, stranger_info)

    msg = args.extract_plain_text().strip()

    variable_expansion_core = VariableExpansionCore(stranger_info)
    if sendmsg.is_debug_mode:
        sendmsg.send_debug_mode()
    else:
        response = await variable_expansion_core.expand_variable(text=msg)
        if response.code == 200:
            await sendmsg.send_text(response.text)
        else:
            await sendmsg.send_response(response, "Error: VariableExpansion")
