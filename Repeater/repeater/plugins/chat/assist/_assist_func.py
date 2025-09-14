from nonebot.adapters.onebot.v11 import Message, MessageEvent, MessageSegment
from nonebot import on_message
from nonebot.adapters import Bot
from typing import Optional

user_cache = {}  # 缓存用户昵称

async def handle_at_with_name(bot: Bot, event: MessageEvent) -> Message:
    """
    处理@消息，将@的QQ号替换为昵称

    :param bot: Bot对象
    :param event: MessageEvent对象
    """
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
    """
    获取消息中第一个@的QQ号

    :param event: 消息事件对象
    """
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

async def image_to_text(bot:Bot, message: Message, format: str = "{text}", cite: bool = True, ensure_empty_when_text_exists: bool = False) -> Message:
    """
    将图片转换为文字

    :param bot: 机器人实例
    :param message: 消息对象
    :param format: 转换后的格式，需要填写 {text} 占位符
    :param cite: 是否引用原始消息
    :param ensure_empty_when_text_exists: 如果没有识别出文字，且消息中有文本内容，是否返回以空识别结果输出
    """
    if "image" not in message:
        return message
    outmsg = Message()
    for segment in message:
        if segment.type == "image":
            ocrout = await bot.ocr_image(image = segment.data["url"])
            text = ""
            summary = segment.data.get("summary", "")
            for item in ocrout:
                text += item["text"] + "\n"
            if text.endswith("\n"):
                text = text[:-1]
            text = format.format(text = text)
            if (ensure_empty_when_text_exists and message.extract_plain_text().strip()) or text.strip():
                text = f"[Image tag:{summary}]\n{text}"
                if cite:
                    text = text.replace("\n", "\n> ")
                outmsg.append(MessageSegment(type = "text", data = {"text": text}))
            else:
                outmsg.append(segment)
        else:
            outmsg.append(segment)
    return outmsg