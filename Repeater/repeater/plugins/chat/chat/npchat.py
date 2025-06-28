from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore, RepeaterDebugMode

npchat = on_command('npChat', aliases={'np', 'no_prompt_chat', 'No_Prompt_Chat', 'NoPromptChat'}, rule=to_me(), block=True)


@npchat.handle()
async def handle_npchat(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    msg = args.extract_plain_text().strip()
    reply = MessageSegment.reply(event.message_id) # 获取回复消息头
    if msg:
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
        if RepeaterDebugMode:
            await npchat.finish(reply + f'[Chat.NoPrompt|{session_id}|{nickname}]：{msg}')
        else:
            filename, code, text, reasoning, content = await chat_core.send_message_and_get_image(message=msg, username=nickname, load_prompt=False)
            if code == 200:
                response = MessageSegment.image(filename)
            else:
                response = MessageSegment.text(text)
            await npchat.finish(reply + response)
