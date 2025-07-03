from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore, RepeaterDebugMode

delete_public_space_context = on_command('deletePublicSpaceContext', aliases={'dpsc', 'delete_public_space_context', 'Delete_Public_Space_Context', 'DeletePublicSpaceContext'}, rule=to_me(), block=True)

@delete_public_space_context.handle()
async def handle_delete_public_space_context(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    try:
        whatever, group_id, user_id = event.get_session_id().split('_')  # 获取当前群聊id，发起人id，返回的格式为group_groupid_userid
        user_id = f"Group_{group_id}_Public_Space"
        mode = "group"
    except:  # 如果上面报错了，意味着发起的是私聊，返回格式为userid
        group_id = None
        user_id = event.get_session_id()
        user_id = f"Private:{user_id}"
        mode = "private"
    result = await bot.get_stranger_info(user_id=user_id)
    nickname = result['nickname']

    reply = MessageSegment.reply(event.message_id)
    chat_core = ChatCore(user_id)
    if RepeaterDebugMode:
        await delete_public_space_context.finish(reply + f'[Chat.Delete_Public_Space_Context|{user_id}|{nickname}]')
    else:
        code, text = await chat_core.delete_context()

        await delete_public_space_context.finish(reply + f'====Chat.Delete_Public_Space_Context====\n> {user_id}\n{text}\nHTTP Code: {code}')