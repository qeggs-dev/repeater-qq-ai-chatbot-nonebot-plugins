from nonebot import on_message, on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore, RepeaterDebugMode, MAX_LENGTH

smart_at = on_message(rule=to_me(), priority=100, block=True)

@smart_at.handle()
async def handle_smart_at(bot: Bot, event: MessageEvent):
    msg = event.get_plaintext().strip()
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
        if mode == "group":
            await smart_at.finish(
                reply + '复读机在线哦~ ο(=•ω＜=)ρ⌒☆'
            )
        else:
            return

    chat_core = ChatCore(session_id)
    if RepeaterDebugMode:
        await smart_at.finish(reply + f'[Chat|{session_id}|{nickname}]：{msg}')
    else:
        filename, code, text, reasoning, content = await chat_core.send_message_and_get_image(message=msg, username=nickname, model_type='chat')
        if mode == "group":
            if code == 200:
                response = MessageSegment.image(filename)
                await smart_at.finish(reply + response)
            else:
                await smart_at.finish(reply + f'====Chat.Chat====\n> {session_id}\n{text}\nHTTP Code: {code}')
        else:
            if code == 200:
                if len(text) > MAX_LENGTH:
                    response = MessageSegment.image(filename)
                else:
                    response = text
                await smart_at.finish(reply + content)
            else:
                await smart_at.finish(reply + f'====Chat.Chat====\n> {session_id}\n{response}\nHTTP Code: {code}')

chat = on_command('chat', aliases={'c', 'Chat'}, rule=to_me(), block=True)

async def handle_chat(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
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
        await smart_at.finish(reply + f'[Chat|{session_id}|{nickname}]：{msg}')
    else:
        reasoning, response, text, code = await chat_core.send_message(message=msg, username=nickname, model_type='chat')
        if code == 200:
            if reasoning:
                content = ('> ' + reasoning.replace('\n', '\n> ') + '\n\n---\n\n' + response)
            else:
                content = response
            await smart_at.finish(reply + content)
        else:
            await smart_at.finish(reply + f'====Chat.Chat====\n> {session_id}\n{text}\nHTTP Code: {code}')