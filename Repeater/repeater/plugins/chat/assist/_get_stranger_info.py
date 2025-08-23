from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment, Message
from nonebot.adapters import Bot
from typing import Literal, Container
from ._assist_func import (
    handle_at_with_name,
    image_to_text
)
from ._namespace import MessageSource, Namespace

class StrangerInfo:
    def __init__(self, bot: Bot, event: MessageEvent, args: Message | None = None):
        self.group_id: str | None = None
        self.user_id: str = event.user_id
        self.nickname: str = ""
        self._mode: MessageSource = MessageSource.GROUP
        self._args: Message = args
        self._bot: Bot = bot
        self._message_event: MessageEvent = event
        
        self._mode = MessageSource(event.message_type.strip().lower())

        if self._mode == MessageSource.GROUP:
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
        if self._mode == MessageSource.GROUP:
            return Namespace(
                mode=MessageSource.GROUP,
                group_id=self.group_id,
                user_id=self.user_id
            )
        else:
            return Namespace(
                mode=MessageSource.PRIVATE,
                user_id=self.user_id
            )
    
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
        return MessageSegment.reply(self._message_event.message_id)
    
    @property
    def mode(self) -> MessageSource:
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
    
    async def image_to_text(self, format: str = "{text}", cite: bool = True, excluded_tags:Container[str] = {}) -> Message:
        """将图片转换为文字"""
        if "image" not in self.message:
            return self.message
        outmsg = Message()
        for segment in self.message:
            if segment.type == "image":
                ocrout = await self._bot.ocr_image(image = segment.data["url"])
                text = ""
                tag = segment.data.get("summary", "")
                for item in ocrout:
                    text += item["text"] + "\n"
                if text.endswith("\n"):
                    text = text[:-1]
                if tag not in excluded_tags:
                    text = f"[Image tag:{tag}]\n{text}"
                if text.strip():
                    text = format.format(text = text)
                    if cite:
                        text = text.replace("\n", "\n> ")
                    outmsg.append(MessageSegment(type = "text", data = {"text": text}))
                else:
                    outmsg.append(segment)
            else:
                outmsg.append(segment)
        return outmsg
    
    @property
    def plaintext_message(self) -> str:
        return self.message.extract_plain_text()