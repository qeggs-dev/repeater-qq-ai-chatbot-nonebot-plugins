from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot
from typing import Literal
from ..assist_func import image_to_text

class StrangerInfo:
    def __init__(self):
        self.group_id: str = ""
        self.user_id: str = ""
        self.nickname: str = ""
        self.mode: Literal["group", "private"] = "group"
        self.message: Message = Message()
        self.reply: MessageSegment = MessageSegment(type="reply")

    async def get_stranger_info(self, bot: Bot, event: MessageEvent, args: Message | None = None) -> dict:
        try:
            whatever, self.group_id, self.user_id = event.get_session_id().split('_')  # 获取当前群聊id，发起人id，返回的格式为group_groupid_userid
            self.mode = "group"
            result = await bot.get_group_member_info(group_id = self.group_id, user_id = self.user_id, no_cache = False)
            self.nickname = result['card']
            if not self.nickname:
                self.nickname = result['nickname']
        except:  # 如果上面报错了，意味着发起的是私聊，返回格式为userid
            self.group_id = None
            self.user_id = event.get_session_id()
            self.mode = "private"
            result = await bot.get_stranger_info(user_id=self.user_id)
            self.nickname = result['remark']
            if not self.nickname:
                self.nickname = result['nickname']
        
        if args is not None:
            tmsg:Message = await image_to_text(bot, args, "\n==== OCR Image Begin ====\n{text}\n===== OCR Image End =====\n")
        else:
            tmsg:Message = await image_to_text(bot, event.message, "\n==== OCR Image Begin ====\n{text}\n===== OCR Image End =====\n")
        
        self.message:str = tmsg.extract_plain_text().strip()
        self.reply = MessageSegment.reply(event.message_id)
    
    @property
    def name_space(self):
        if self.mode == "group":
            return f"Group:{self.group_id}:{self.name_space}"
        else:
            return f"Private:{self.name_space}"
    
    @property
    def public_space_id(self):
        if self.mode == "group":
            return f"Group:{self.group_id}_Public_Space"
        else:
            return f"Private:{self.name_space}_Public_Space"