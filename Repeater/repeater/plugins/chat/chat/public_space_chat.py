from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot
from nonebot import logger

from .core import ChatCore, RepeaterDebugMode, MAX_LENGTH, MAX_SINGLE_LINE_LENGTH, MIN_RENDER_IMAGE_TEXT_LINE
from ..assist_func import image_to_text

public_space_chat = on_command('publicSpaceChat', aliases={'psc', 'public_space_chat', 'Public_Space_Chat', 'PublicSpaceChat'}, rule=to_me(), block=True)

@public_space_chat.handle()
async def handle_public_space_chat(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
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
        chat_core = ChatCore(session_id)
        if RepeaterDebugMode:
            await public_space_chat.finish(reply + f'[Chat.Public_Space_Chat|{session_id}|{nickname}]：{msg}')
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
                await public_space_chat.finish(reply + message)
            else:
                await public_space_chat.finish(reply + f"====Chat.Public_Space_Chat====\n> {session_id}\n{response}\nHTTP Code: {response['status_code']}")