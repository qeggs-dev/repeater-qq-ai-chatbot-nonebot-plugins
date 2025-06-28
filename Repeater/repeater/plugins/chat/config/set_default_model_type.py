from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore, RepeaterDebugMode

set_default_model_type = on_command('setDefaultModel', aliases={'sdm', 'set_default_model', 'Set_Default_Model', 'SetDefaultModel'}, rule=to_me(), block=True)

@set_default_model_type.handle()
async def handle_set_default_model_type(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    msg =  args.extract_plain_text().strip()
    try:
        whatever, group_id, user_id = event.get_session_id().split('_')  # 获取当前群聊id，发起人id，返回的格式为group_groupid_userid
        session_id = f"Group:{group_id}:{user_id}"
    except:  # 如果上面报错了，意味着发起的是私聊，返回格式为userid
        group_id = None
        user_id = event.get_session_id()
        session_id = f"Private:{user_id}"
    result = await bot.get_stranger_info(user_id=user_id)
    nickname = result['nickname']

    style = {"chat", "reasoner", "prover"}
    if msg.lower() not in style:
        await set_default_model_type.finish(
            f'====Chat.Set_Default_Model====\n> 请输入正确的模型名称\n> 可选模型：{style}'
        )
    else:
        msg = msg.lower()


    reply = MessageSegment.reply(event.message_id)
    chat_core = ChatCore(session_id)
    if RepeaterDebugMode:
        await set_default_model_type.finish(reply + f'[Chat.Set_Default_Model|{session_id}|{nickname}]:{msg}')
    else:
        code, text = await chat_core.set_default_model_type(model_type=msg)

        await set_default_model_type.finish(reply + f'====Chat.Set_Default_Model====\n> {session_id}\n{text}\nHTTP Code: {code}\n\nDefault_Model: {msg}')