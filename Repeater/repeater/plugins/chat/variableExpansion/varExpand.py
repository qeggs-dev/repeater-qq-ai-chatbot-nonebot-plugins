from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore, RepeaterDebugMode
from ..assist import StrangerInfo

var_Expand = on_command("varExpand", aliases={"ve", "var_expand", "Var_Expand", "VarExpand"}, rule=to_me(), block=True)

@var_Expand.handle()
async def handle_var_expand(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot=bot, event=event, args=args)

    msg = args.extract_plain_text().strip()

    chat_core = ChatCore(stranger_info.name_space.namespace)
    if RepeaterDebugMode:
        await var_Expand.finish(stranger_info.reply + f'[Chat.Var_Expand|{chat_core.name_space}|{stranger_info.nickname}]：{msg}')
    else:
        code, text = await chat_core.expand_variable(username=stranger_info.nickname, text=msg)
        if code == 200:
            await var_Expand.finish(stranger_info.reply + text)
        else:
            await var_Expand.finish(stranger_info.reply + f'====Chat.Var_Expand====\n> {chat_core.name_space}\n{text}\nHTTP Code: {code}')
