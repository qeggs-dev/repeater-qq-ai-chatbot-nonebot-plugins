from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot
from typing import Optional
import asyncio

from ..core_net_configs import RepeaterDebugMode

get_namespace = on_command('getNamespace', aliases={'gs', 'get_namespace', 'Get_Namespace', 'GetNamespace'}, rule=to_me(), block=True)

from ..assist import get_first_mentioned_user, PersonaInfo, Namespace

@get_namespace.handle()
async def handle_get_namespace(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    persona_info = PersonaInfo(bot, event, args)
    
    reply = persona_info.reply

    if RepeaterDebugMode:
        await get_namespace.finish(reply + f'[Chat.Get_Namespace|{persona_info.namespace_str}]')
    else:
        mentioned_id = get_first_mentioned_user(event)
        if mentioned_id is None:
            await get_namespace.finish(reply + f'====Chat.Get_Namespace====\n> {persona_info.namespace_str}')
        else:
            await get_namespace.finish(reply + f'====Chat.Get_Namespace====\n> {Namespace(mentioned_id).namespace}')
