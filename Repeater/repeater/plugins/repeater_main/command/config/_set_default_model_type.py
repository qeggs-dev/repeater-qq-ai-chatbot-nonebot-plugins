from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters import Bot

from .._clients import ConfigCore
from ...assist import PersonaInfo, SendMsg

set_default_model_type = on_command('setDefaultModel', aliases={'sdm', 'set_default_model', 'Set_Default_Model', 'SetDefaultModel'}, rule=to_me(), block=True)

@set_default_model_type.handle()
async def handle_set_default_model_type(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot=bot, event=event, args=args)
    sendmsg = SendMsg("Config.Set_Default_Model", set_default_model_type, persona_info)

    config_core = ConfigCore(persona_info)
    if sendmsg.is_debug_mode:
        await sendmsg.send_debug_mode()
    else:
        response = await config_core.set_config("model_uid", persona_info.message_str)
        await sendmsg.send_response(response, f"Set Default Model to {persona_info.message_str}")