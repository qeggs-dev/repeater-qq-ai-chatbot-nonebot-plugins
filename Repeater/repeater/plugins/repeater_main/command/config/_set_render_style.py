from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from .._clients import ConfigCore
from ...assist import StrangerInfo, SendMsg

set_render_style = on_command('setRenderStyle', aliases={'srs', 'set_render_style', 'Set_Render_Style', 'SetRenderStyle'}, rule=to_me(), block=True)

@set_render_style.handle()
async def handle_set_render_style(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot=bot, event=event, args=args)
    sendmsg = SendMsg("Config.Set_Render_Style", set_render_style, stranger_info)

    msg = stranger_info.message_str.strip()

    config_core = ConfigCore(stranger_info.namespace_str)
    if sendmsg.is_debug_mode:
        await sendmsg.send_debug_mode()
    else:
        response = await config_core.set_config("render_style", msg)
        await sendmsg.send_response(response, f"Set Render_Style to {msg}")