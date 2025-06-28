from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore, RepeaterDebugMode

from ..assist_func import get_first_mentioned_user

clone_config = on_command('cloneconfig', aliases={'cs', 'clone_config', 'Clone_Config', 'CloneConfig'}, rule=to_me(), block=True)

@clone_config.handle()
async def handle_clone_config(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    msg =  args.extract_plain_text().strip()
    try:
        whatever, group_id, user_id = event.get_config_id().split('_')  # 获取当前群聊id，发起人id，返回的格式为group_groupid_userid
        config_id = f"Group:{group_id}:{user_id}"
        mode = 'group'
    except:  # 如果上面报错了，意味着发起的是私聊，返回格式为userid
        group_id = None
        user_id = event.get_config_id()
        config_id = f"Private:{user_id}"
        mode = 'private'
    result = await bot.get_stranger_info(user_id=user_id)
    nickname = result['nickname']

    reply = MessageSegment.reply(event.message_id)
    chat_core = ChatCore(config_id)
    if RepeaterDebugMode:
        await clone_config.finish(reply + f'[Chat.Clone_config|{config_id}|{nickname}]:{msg}')
    else:
        mentioned_id = get_first_mentioned_user(event)
        if mentioned_id:
            if mode == 'group':
                from_config_id = f"Group:{group_id}:{mentioned_id}"
            else:
                from_config_id = f"Private:{mentioned_id}"

            code, text = await chat_core.clone_config(
                from_config_id = from_config_id,
            )

            await clone_config.finish(reply + f'====Chat.Clone_Config====\n> {from_config_id} -> {config_id}\n{text}\nHTTP Code: {code}')
        else:
            await clone_config.finish(reply + f'====Chat.Clone_Config====\n> {config_id}\nNeed A Mentioned User')