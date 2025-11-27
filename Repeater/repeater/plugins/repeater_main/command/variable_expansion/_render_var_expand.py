from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .._clients import VariableExpansionCore
from ...assist import PersonaInfo, SendMsg

render_var_expand = on_command("varExpandRender", aliases={"ver", "var_expand_render", "Var_Expand_Render", "VarExpandRender"}, rule=to_me(), block=True)

@render_var_expand.handle()
async def handle_render_var_expand(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    sendmsg = SendMsg("VarExpandRender", render_var_expand, persona_info)

    msg = args.extract_plain_text().strip()

    variable_expansion_core = VariableExpansionCore(persona_info)
    if sendmsg.is_debug_mode:
        sendmsg.send_debug_mode()
    else:
        response = await variable_expansion_core.expand_variable(text=msg)
        if response.code == 200:
            await sendmsg.send_render(response.text)
        else:
            await sendmsg.send_response(response, "Error: VariableExpansion")
