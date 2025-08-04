from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore, RepeaterDebugMode
from ..assist_func import image_to_text

renderChat = on_command('renderChat', aliases={'rc', 'render_chat', 'Render_Chat', 'RenderChat'}, rule=to_me(), block=True)

@renderChat.handle()
async def handle_render_Chat(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    tmsg:Message = await image_to_text(bot, event.message, "\n==== OCR Image Begin ====\n{text}\n===== OCR Image End =====\n")
    msg:str = tmsg.extract_plain_text().strip()
    reply = MessageSegment.reply(event.message_id) # 获取回复消息头
    if msg:
        try:
            whatever, group_id, user_id = event.get_session_id().split('_')  # 获取当前群聊id，发起人id，返回的格式为group_groupid_userid
            session_id = f"Group:{group_id}:{user_id}"
            mode = "group"
            result = await bot.get_group_member_info(group_id = group_id, user_id = user_id, no_cache = False)
            nickname = result['card']
            if not nickname:
                nickname = result['nickname']
        except:  # 如果上面报错了，意味着发起的是私聊，返回格式为userid
            group_id = None
            user_id = event.get_session_id()
            session_id = f"Private:{user_id}"
            mode = "private"
            result = await bot.get_stranger_info(user_id=user_id)
            nickname = result['nickname']
    
    chat_core = ChatCore(session_id)
    if RepeaterDebugMode:
        await renderChat.finish(reply + f'[Chat.Render_Chat|{session_id}|{nickname}]：{msg}')
    else:
        response = await chat_core.send_message(message=msg, username=nickname)
        if response['status_code'] == 200:
            render_response = await chat_core.content_render(response['content'], response['reasoning'])
            message = MessageSegment.image(render_response['image_url'])
            await renderChat.finish(reply + message)
        else:
            await renderChat.finish(reply + f"====Chat.Render_Chat====\n> {session_id}\n{response}\nHTTP Code: {response['status_code']}")
