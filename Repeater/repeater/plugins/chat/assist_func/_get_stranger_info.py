from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment, Message
from nonebot.adapters import Bot
from typing import Literal
from ._assist_func import (
    handle_at_with_name,
    image_to_text
)

class StrangerInfo:
    def __init__(self, bot: Bot, event: MessageEvent, args: Message | None = None):
        self.group_id: str | None = None
        self.user_id: str = event.user_id
        self.nickname: str = ""
        self._mode: Literal["group", "private"] = "group"
        self._args: Message = args
        self._reply = MessageSegment.reply(event.message_id)
        self._bot: Bot = bot
        self._message_event: MessageEvent = event
        
        self._mode = event.message_type

        if self._mode == "group":
            try:
                self.group_id = event.model_dump()["group_id"]
                if self.group_id is None:
                    raise ValueError("Is Group, But Group ID is None")
            except KeyError:
                raise ValueError("Is Group, But Group ID is Not Found")

        if event.sender.card:
            self.nickname = event.sender.card
        else:
            self.nickname = event.sender.nickname
    
    @property
    def bot(self):
        return self._bot

    @property
    def name_space(self):
        if self._mode == "group":
            return f"Group:{self.group_id}:{self.user_id}"
        else:
            return f"Private:{self.user_id}"
    
    @property
    def public_space_id(self):
        if self._mode == "group":
            return f"Group:{self.group_id}_Public_Space"
        else:
            return f"Private:{self.user_id}_Public_Space"
    
    @property
    def message(self) -> Message:
        if self._args is not None:
            return self._args
        else:
            return self._message_event.message
    
    @property
    def message_str(self) -> str:
        return self.message.extract_plain_text()
    
    @property
    def reply(self):
        return self._reply
    
    @property
    def mode(self) -> Literal['group', 'private']:
        return self._mode
    
    @property
    def noself_at_list(self):
        at_list: list[str] = []
        if self._message_event is None:
            return at_list
        for segment in self._message_event.message:
            if segment.type == "at":
                mentioned_id = segment.data["qq"]
                # 检查是否@的是非机器人用户
                if mentioned_id != self._bot.self_id:
                    at_list.append(mentioned_id)
        return at_list
    
    @property
    def at_list(self):
        at_list: list[str] = []
        if self._message_event is None:
            return at_list
        for segment in self._message_event.message:
            if segment.type == "at":
                at_list.append(segment.data["qq"])
        return at_list
    
    async def handle_at_with_name(self):
        return await handle_at_with_name(self._bot, self._message_event)
    
    async def image_to_text(self, format: str = "{text}", cite: bool = True) -> Message:
        return await image_to_text(self._bot, self.message, format, cite)
    
    @property
    def plaintext_message(self) -> str:
        return self.message.extract_plain_text()