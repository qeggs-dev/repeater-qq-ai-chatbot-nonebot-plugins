from nonebot.adapters.onebot.v11 import Message, MessageEvent
from nonebot import on_message
from nonebot.adapters import Bot
from typing import Optional

user_cache = {}  # 缓存用户昵称

async def handle_at_with_name(bot: Bot, event: MessageEvent) -> Message:
    new_msg = Message()
    
    for seg in event.message:
        if seg.type == "at":
            qq = seg.data.get("qq", "")
            if qq in user_cache:  # 优先读缓存
                name = user_cache[qq]
            else:
                try:
                    info = await bot.get_stranger_info(user_id=int(qq))
                    name = info["nickname"]
                    user_cache[qq] = name  # 存入缓存
                except:
                    name = qq  # 失败则用 QQ 号代替
            new_msg.append(f"@{name}")
        else:
            new_msg.append(seg)
    
    return new_msg

def get_first_mentioned_user(event: MessageEvent) -> Optional[str]:
    # 获取机器人自己的QQ号
    bot_id = str(event.self_id)
    
    # 遍历消息中的所有@消息段
    for segment in event.message:
        if segment.type == "at":
            mentioned_id = segment.data["qq"]
            # 检查是否@的是非机器人用户
            if mentioned_id != bot_id:
                return mentioned_id
    return None