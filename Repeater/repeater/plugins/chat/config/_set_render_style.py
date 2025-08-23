from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from ._core import ChatCore, RepeaterDebugMode
from ..assist import StrangerInfo

set_render_style = on_command('setRenderStyle', aliases={'srs', 'set_render_style', 'Set_Render_Style', 'SetRenderStyle'}, rule=to_me(), block=True)

@set_render_style.handle()
async def handle_set_render_style(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot=bot, event=event, args=args)

    msg = stranger_info.message_str.strip()

    reply = MessageSegment.reply(event.message_id)
    chat_core = ChatCore(stranger_info.name_space.namespace)
    if RepeaterDebugMode:
        await set_render_style.finish(reply + f'[Chat.Set_Render_Style|{chat_core.name_space}|{stranger_info.nickname}]:{msg}')
    else:
        code, text = await chat_core.set_config("render_style", msg)

        await set_render_style.finish(reply + f'====Chat.Set_Render_Style====\n> {chat_core.name_space}\n{text}\nHTTP Code: {code}\n\nRender_Style: {msg}')