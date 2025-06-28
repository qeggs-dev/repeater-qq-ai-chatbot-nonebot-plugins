from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore, RepeaterDebugMode, MAX_LENGTH

var_Expand = on_command("varExpand", aliases={"ve", "var_expand", "Var_Expand", "VarExpand"}, rule=to_me(), block=True)

@var_Expand.handle()
async def handle_var_expand(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    msg = args.extract_plain_text().strip()
    reply = MessageSegment.reply(event.message_id) # 获取回复消息头
    
    try:
        whatever, group_id, user_id = event.get_session_id().split('_')  # 获取当前群聊id，发起人id，返回的格式为group_groupid_userid
        session_id = f"Group:{group_id}:{user_id}"
        mode = "group"
    except:  # 如果上面报错了，意味着发起的是私聊，返回格式为userid
        group_id = None
        user_id = event.get_session_id()
        session_id = f"Private:{user_id}"
        mode = "private"
    result = await bot.get_stranger_info(user_id=user_id)
    nickname = result['nickname']

    chat_core = ChatCore(session_id)
    if RepeaterDebugMode:
        await var_Expand.finish(reply + f'[Chat.Var_Expand|{session_id}|{nickname}]：{msg}')
    else:
        code, text = await chat_core.expand_variable(username=nickname, text=msg)
        if code == 200:
            await var_Expand.finish(reply + text)
        else:
            await var_Expand.finish(reply + f'====Chat.Var_Expand====\n> {session_id}\n{text}\nHTTP Code: {code}')
