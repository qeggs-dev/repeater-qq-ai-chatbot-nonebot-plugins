from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore, RepeaterDebugMode

reason = on_command("reason", aliases={"r", "Reason"}, rule=to_me(), block=True)

@reason.handle()
async def reason_handle(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    msg = args.extract_plain_text().strip()
    if not msg:
        await reason.finish(
            'AI推理的输入不能为空哦~ (´・ω・`)'
        )
    
    try:
        whatever, group_id, user_id = event.get_session_id().split('_')  # 获取当前群聊id，发起人id，返回的格式为group_groupid_userid
        session_id = f"Group:{group_id}:{user_id}"
    except:  # 如果上面报错了，意味着发起的是私聊，返回格式为userid
        group_id = None
        user_id = event.get_session_id()
        session_id = f"Private:{user_id}"
    result = await bot.get_stranger_info(user_id=user_id)
    nickname = result['nickname']

    chat_core = ChatCore(session_id)
    reply = MessageSegment.reply(event.message_id)
    if RepeaterDebugMode:
        await reason.finish(reply + f'[Chat.Reason|{session_id}|{nickname}]：{msg}')
    else:
        filename, code, text, reasoning, content = await chat_core.send_message_and_get_image(msg, nickname, model_type='reasoner')
        if code == 200:
            response = MessageSegment.image(filename)
            await reason.finish(reply + response)
        else:
            await reason.finish(reply + f'====Chat.Reason====\n> {session_id}\n{response}\nHTTP Code: {code}')
