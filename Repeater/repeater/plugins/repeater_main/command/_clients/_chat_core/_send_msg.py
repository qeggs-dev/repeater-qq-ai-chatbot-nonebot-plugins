from nonebot.adapters.onebot.v11 import MessageSegment, Message
from nonebot.internal.matcher.matcher import Matcher
from ....assist import PersonaInfo, MessageSource, Response, TextRender, SendMsg as BaseSendMsg
from ._response_body import ChatResponse
from ....chattts import ChatTTSAPI
from typing import NoReturn
from ....logger import logger as base_logger
import numpy as np

logger = base_logger.bind(module = "Chat.SendMsg")

class Send_msg(BaseSendMsg):
    def __init__(
            self,
            component: str,
            persona_info: PersonaInfo,
            matcher: Matcher,
            response: Response[ChatResponse | None],
        ):
        super().__init__(f"Chat.{component}", matcher, persona_info)
        self.response: Response[ChatResponse] = response
        self._text_render = TextRender(namespace = self._persona_info.namespace)
        self._chat_tts_api = ChatTTSAPI()
    
    async def _send_error_message(self):
        if self.response.data is None:
            await self.send_response(self.response)
        else:
            await self.send_response(
                self.response,
                message = self.response.data.content
            )


    async def send(self):
        if self.is_debug_mode:
            await self.send_debug_mode()
        else:
            if self.response.code == 200:
                score = self.text_length_score(self.response.data.content)
                threshold = self.text_length_score_threshold
                logger.info(f"Response content socre: {score}")
                if score >= threshold:
                    logger.warning(f"Response content socre to high: {score}, Expected to be below {threshold} ")
                    logger.warning("The text will be rendered as an image output.")
                    await self.send_image_mode()
                else:
                    await self.send_text_mode()
            else:
                await self._send_error_message()
    
    async def send_tts_mode(self, text: str | None = None) -> NoReturn:
        if self.is_debug_mode:
            await self.send_debug_mode()
        else:
            if self.response.code == 200:
                await self.send_render(
                    self.response.data.reasoning_content,
                    reply = True,
                    continue_handler = True
                )
                await self.send_tts(
                    text or self.response.data.content,
                    reply = False,
                    continue_handler = False
                )
            else:
                await self._send_error_message()
            
    
    async def send_text_mode(self, text: str | None = None) -> NoReturn:
        if self.is_debug_mode:
            await self.send_debug_mode()
        else:
            if self.response.code == 200:
                message = Message()
                message.append(self._persona_info.reply)
                # 推理内容必须渲染为图片
                if self.response.data.reasoning_content:
                    message.append(
                        await self.text_render(self.response.data.reasoning_content)
                    )
                if self.response.data.content:
                    message.append(text or self.response.data.content)
                else:
                    message.append("Message is empty.")
                await self._matcher.finish(message)
            else:
                await self._send_error_message()
    
    async def send_image_mode(self, text: str | None = None) -> NoReturn:
        if self.is_debug_mode:
            await self.send_debug_mode()
        else:
            if self.response.code == 200:
                message = Message()
                message.append(self._persona_info.reply)
                if self.response.data.reasoning_content:
                    message.append(
                        await self.text_render(self.response.data.reasoning_content)
                    )
                if self.response.data.content:
                    message.append(
                        await self.text_render(self.response.data.content)
                    )
                else:
                    message.append("[Message is empty.]")
                await self._matcher.finish(message)
            else:
                await self._send_error_message()