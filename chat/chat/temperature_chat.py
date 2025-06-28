from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot

from .core import ChatCore, RepeaterDebugMode

temperature_chat = on_command("temperatureChat", aliases={"tc", "temperature_chat", "Temperature_Chat", "TemperatureChat"}, rule=to_me(), block=True)

@temperature_chat.handle()
async def handle_temperature_chat(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    msg = args.extract_plain_text().strip()
    if not msg:
        await temperature_chat.finish(
            '输入不能为空哦~'
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

    parts = msg.split(maxsplit=1)
    first_arg = parts[0]
    remaining_args = parts[1] if len(parts) > 1 else ""

    try:
        temperature = float(first_arg)
    except ValueError:
        temperature = 1.3

    if temperature < 0 or temperature > 2:
        await temperature_chat.finish(
            '====Chat.Temperature_Chat====\n> 温度设置错误，请输入0~2之间的浮点数'
        )

    chat_core = ChatCore(session_id)
    reply = MessageSegment.reply(event.message_id)
    if RepeaterDebugMode:
        await temperature_chat.finish(reply + f'[Chat.Temperature_Chat|{session_id}|{nickname}]：{remaining_args}')
    else:
        filename, code, text, reasoning, content = await chat_core.send_message_and_get_image(message=remaining_args, username=nickname, temperature=first_arg, model_type='chat')
        if code == 200:
            response = MessageSegment.image(filename)
            await temperature_chat.finish(reply + response)
        else:
            await temperature_chat.finish(reply + f'====Chat.Temperature_Chat====\n> {session_id}\n{remaining_args}\nHTTP Code: {code}\n')
