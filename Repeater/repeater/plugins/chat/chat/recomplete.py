from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore, RepeaterDebugMode, MAX_LENGTH, MAX_SINGLE_LINE_LENGTH, MIN_RENDER_IMAGE_TEXT_LINE

recomplete = on_command("recomplete", aliases={"rec", "Recomplete"}, rule=to_me(), block=True)

@recomplete.handle()
async def handle_recomplete(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
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
    
    if not msg:
        msg = ''

    chat_core = ChatCore(session_id)
    if RepeaterDebugMode:
        await recomplete.finish(reply + f'[Chat.Recomplete|{session_id}|{nickname}]：{msg}')
    else:
        response = await chat_core.send_message(message=msg, username=nickname)
        lines = response['content'].split('\n')
        max_line_length = max(len(line) for line in lines) if lines else 0
        if response['status_code'] == 200:
            if mode == "group" and (max_line_length < MAX_SINGLE_LINE_LENGTH or len(response['content'].split('\n')) > MIN_RENDER_IMAGE_TEXT_LINE):
                render_response = await chat_core.content_render(response['content'], response['reasoning'])
                message = MessageSegment.image(render_response['image_url'])
            elif len(response['response_text']) > MAX_LENGTH:
                render_response = await chat_core.content_render(response['content'], response['reasoning'])
                message = MessageSegment.image(render_response['image_url'])
            else:
                message = response['content']
            await recomplete.finish(reply + message)
        else:
            await recomplete.finish(reply + f"====Chat.Recomplete====\n> {session_id}\n{response}\nHTTP Code: {response['status_code']}")
