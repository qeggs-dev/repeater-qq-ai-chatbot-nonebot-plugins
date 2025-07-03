from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot
from nonebot import logger

from .core import ChatCore, RepeaterDebugMode, MAX_LENGTH, MAX_SINGLE_LINE_LENGTH, MIN_RENDER_IMAGE_TEXT_LINE

public_space_chat = on_command('publicSpaceChat', aliases={'psc', 'public_space_chat', 'Public_Space_Chat', 'PublicSpaceChat'}, rule=to_me(), block=True)


@public_space_chat.handle()
async def handle_public_space_chat(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    msg = args.extract_plain_text()
    reply = MessageSegment.reply(event.message_id) # 获取回复消息头
    if msg:
        try:
            whatever, group_id, user_id = event.get_session_id().split('_')  # 获取当前群聊id，发起人id，返回的格式为group_groupid_userid
            session_id = f"Group_{group_id}_Public_Space"
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
            await public_space_chat.finish(reply + f'[Chat.Public_Space_Chat|{session_id}|{nickname}]：{msg}')
        else:
            fileurl, code, text, reasoning, content = await chat_core.send_message_and_get_image(message=msg, username=nickname, role_name=nickname)
            logger.info(f'fileurl: {fileurl}')
            lines = content.split('\n')
            max_line_length = max(len(line) for line in lines) if lines else 0
            if mode == "group" and (max_line_length < MAX_SINGLE_LINE_LENGTH or len(content.split('\n')) > MIN_RENDER_IMAGE_TEXT_LINE):
                if code == 200:
                    response = MessageSegment.image(fileurl)
                    await public_space_chat.finish(reply + response)
                else:
                    await public_space_chat.finish(reply + f'====Chat.Chat====\n> {session_id}\n{text}\nHTTP Code: {code}')
            else:
                if code == 200:
                    if len(text) > MAX_LENGTH:
                        response = MessageSegment.image(fileurl)
                    else:
                        response = text
                    await public_space_chat.finish(reply + content)
                else:
                    await public_space_chat.finish(reply + f'====Chat.Chat====\n> {session_id}\n{response}\nHTTP Code: {code}')