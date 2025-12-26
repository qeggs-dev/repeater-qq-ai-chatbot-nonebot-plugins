from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from .._clients import ConfigCore
from ...assist import PersonaInfo, SendMsg, str_to_bool

set_auto_save_context = on_command("setAutoSaveContext", aliases={"sasc", "set_auto_save_context", "Set_Auto_Save_Context", "SetAutoSaveContext"}, rule=to_me(), block=True)

@set_auto_save_context.handle()
async def handle_set_auto_save_context(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    sendmsg = SendMsg("Config.Set_Auto_Save_Context", set_auto_save_context, persona_info)

    try:
        auto_save_context = str_to_bool(persona_info.message_str)
    except ValueError:
        await sendmsg.send_error("Not a valid boolean value")

    if sendmsg.is_debug_mode:
        await sendmsg.send_debug_mode()
    else:
        config_core = ConfigCore(persona_info)
        response = await config_core.set_config("save_context", auto_save_context)
        await sendmsg.send_response(response, f"Auto Save Context set to {auto_save_context}")