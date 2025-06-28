from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore, RepeaterDebugMode

prover = on_command("prover", aliases={"p", "Prover"}, rule=to_me(), block=True)

@prover.handle()
async def prover_handle(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    msg = args.extract_plain_text().strip()
    if not msg:
        await prover.finish(
            'AI推理的输入不能为空哦~ (´・ω・`)'
        )
    
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
    reply = MessageSegment.reply(event.message_id)
    if RepeaterDebugMode:
        await prover.finish(reply + f'[Chat.Prover|{session_id}|{nickname}]：{msg}')
    else:
        filename, code, text, reasoing, content = await chat_core.send_message_and_get_image(msg, nickname, load_prompt=False, model_type='prover')
        if code == 200:
            response = MessageSegment.image(filename)
        else:
            await prover.finish(reply + f'====Chat.Prover====\n> {session_id}\n{text}\nHTTP Code: {code}')
        await prover.finish(reply + response)
