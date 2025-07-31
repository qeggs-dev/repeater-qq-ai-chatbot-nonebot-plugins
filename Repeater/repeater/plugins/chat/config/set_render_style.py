from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore, RepeaterDebugMode

set_render_style = on_command('setRenderStyle', aliases={'srs', 'set_render_style', 'Set_Render_Style', 'SetRenderStyle'}, rule=to_me(), block=True)

@set_render_style.handle()
async def handle_set_render_style(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    msg =  args.extract_plain_text().strip()
    try:
        whatever, group_id, user_id = event.get_session_id().split('_')  # 获取当前群聊id，发起人id，返回的格式为group_groupid_userid
        session_id = f"Group:{group_id}:{user_id}"
    except:  # 如果上面报错了，意味着发起的是私聊，返回格式为userid
        group_id = None
        user_id = event.get_session_id()
        session_id = f"Private:{user_id}"
    result = await bot.get_stranger_info(user_id=user_id)
    nickname = result['nickname']

    msg = msg.lower()

    reply = MessageSegment.reply(event.message_id)
    chat_core = ChatCore(session_id)
    if RepeaterDebugMode:
        await set_render_style.finish(reply + f'[Chat.Set_Render_Style|{session_id}|{nickname}]:{msg}')
    else:
        code, text = await chat_core.set_render_style(style=msg)

        await set_render_style.finish(reply + f'====Chat.Set_Render_Style====\n> {session_id}\n{text}\nHTTP Code: {code}\n\nRender_Style: {msg}')