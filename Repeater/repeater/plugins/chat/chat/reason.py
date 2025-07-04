from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore, RepeaterDebugMode, MAX_LENGTH, MAX_SINGLE_LINE_LENGTH, MIN_RENDER_IMAGE_TEXT_LINE

reason = on_command("reason", aliases={"r", "Reason"}, rule=to_me(), block=True)

@reason.handle()
async def reason_handle(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    msg = args.extract_plain_text().strip()
    reply = MessageSegment.reply(event.message_id) # 获取回复消息头
    if not msg:
        await reason.finish(
            'AI推理的输入不能为空哦~ (´・ω・`)'
        )
    
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
        await reason.finish(reply + f'[Chat.Reason|{session_id}|{nickname}]：{msg}')
    else:
        response = await chat_core.send_message(message=msg, username=nickname)
        if response['status_code'] == 200:
            render_response = await chat_core.content_render(response['content'], response['reasoning'])
            message = MessageSegment.image(render_response['image_url'])
            await reason.finish(reply + message)
        else:
            await reason.finish(reply + f"====Chat.Reason====\n> {session_id}\n{response}\nHTTP Code: {response['status_code']}")
