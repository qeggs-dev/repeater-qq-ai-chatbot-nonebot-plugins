from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore, RepeaterDebugMode

from ..assist_func import get_first_mentioned_user

clone_prompt = on_command('clonePrompt', aliases={'cp', 'clone_prompt', 'Clone_Prompt', 'ClonePrompt'}, rule=to_me(), block=True)

@clone_prompt.handle()
async def handle_clone_prompt(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    msg =  args.extract_plain_text().strip()
    try:
        whatever, group_id, user_id = event.get_prompt_id().split('_')  # 获取当前群聊id，发起人id，返回的格式为group_groupid_userid
        prompt_id = f"Group:{group_id}:{user_id}"
        mode = 'group'
    except:  # 如果上面报错了，意味着发起的是私聊，返回格式为userid
        group_id = None
        user_id = event.get_prompt_id()
        prompt_id = f"Private:{user_id}"
        mode = 'private'
    result = await bot.get_stranger_info(user_id=user_id)
    nickname = result['nickname']
    
    reply = MessageSegment.reply(event.message_id)
    chat_core = ChatCore(prompt_id)
    if RepeaterDebugMode:
        await clone_prompt.finish(reply + f'[Chat.Clone_prompt|{prompt_id}|{nickname}]:{msg}')
    else:
        mentioned_id = get_first_mentioned_user(event)
        if mentioned_id:
            if mode == 'group':
                from_prompt_id = f"Group:{group_id}:{mentioned_id}"
            else:
                from_prompt_id = f"Private:{mentioned_id}"

            code, text = await chat_core.clone_prompt(
                from_prompt_id = from_prompt_id,
            )

            await clone_prompt.finish(reply + f'====Chat.Clone_Prompt====\n> {from_prompt_id} -> {prompt_id}\n{text}\nHTTP Code: {code}')
        else:
            await clone_prompt.finish(reply + f'====Chat.Clone_Prompt====\n> {prompt_id}\nNeed A Mentioned User')