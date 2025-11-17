from nonebot.adapters.onebot.v11 import MessageSegment, Message
from nonebot.internal.matcher.matcher import Matcher
from ....chattts import ChatTTSAPI
from ....core_net_configs import storage_config
from ....assist import StrangerInfo, MessageSource, Response, TextRender, SendMsg as BaseSendMsg
from ._response_body import ChatResponse
from typing import NoReturn
from ....logger import logger as base_logger
import numpy as np

logger = base_logger.bind(module = "Chat.SendMsg")

class Send_msg(BaseSendMsg):
    def __init__(
            self,
            component: str,
            stranger_info: StrangerInfo,
            matcher: Matcher,
            response: Response[ChatResponse | None],
        ):
        super().__init__(f"Chat.{component}", matcher, stranger_info)
        self.response: Response[ChatResponse] = response
        self._text_render = TextRender(namespace = self._stranger_info.namespace)
        self._chat_tts_api = ChatTTSAPI()
    
    @staticmethod
    def text_length_score(text:str) -> float:
        lines = text.splitlines()
        line_lengths = np.array([len(line) for line in lines], dtype=np.int64)
        lines_score = len(lines) / storage_config.text_length_score_configs.lines
        single_line_score = line_lengths.max() / storage_config.text_length_score_configs.single_line_max
        mean_line_score = line_lengths.mean() / storage_config.text_length_score_configs.mean_line_max
        total_length_score = len(text) / storage_config.text_length_score_configs.total_length

        return (
            # lines: 33.3%
            lines_score +
            # single_line_score + mean_line_score: 33.3%
            (
                single_line_score +
                mean_line_score
            ) / 2.0 +
            # total_length: 33.3%
            total_length_score
        ) / 3.0
    
    def text_reaches_threshold(self, text: str) -> bool:
        return self.text_length_score(text) >= storage_config.text_length_score_configs.threshold
    
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
                if self._stranger_info.source == MessageSource.GROUP:
                    threshold = storage_config.text_length_score_configs.threshold.group
                else:
                    threshold = storage_config.text_length_score_configs.threshold.private
                if score >= threshold:
                    logger.warning(f"Response content socre to high: {score}, Expected to be below {threshold} ")
                    logger.warning("The text will be rendered as an image output.")
                    await self.send_image()
                else:
                    logger.info(f"Response content socre: {score}")
                    await self.send_text()
            else:
                await self._send_error_message()
    
    async def send_tts(self, send_picture_first: bool = False):
        if self.is_debug_mode:
            await self.send_debug_mode()
        else:
            if self.response.code == 200:
                message = Message()
                if self.response.data.reasoning_content:
                    render_response = await self.text_render(self.response.data.reasoning_content)
                    message.append(render_response)
                    if not send_picture_first:
                        await self._matcher.send(self._stranger_info.reply + message)
                
                if self.response.data.content:
                    if send_picture_first:
                        message.append(
                            await self.text_render(self.response.data.content)
                        )
                        message.append(self._stranger_info.reply)
                        await self._matcher.send(self._stranger_info.reply + message)
                    response = await self._chat_tts_api.text_to_speech(self.response.data.content)
                    if response.code == 200:
                        await self.send_any(MessageSegment.record(response.data.audio_files[0].url), reply=False)
                    else:
                        await self.send_response(response, message = "TTS Error.")
            else:
                await self._send_error_message()
            
    
    async def send_text(self, text: str | None = None) -> NoReturn:
        if self.is_debug_mode:
            await self.send_debug_mode()
        else:
            if self.response.code == 200:
                message = Message()
                message.append(self._stranger_info.reply)
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
    
    async def send_image(self, text: str | None = None) -> NoReturn:
        if self.is_debug_mode:
            await self.send_debug_mode()
        else:
            if self.response.code == 200:
                message = Message()
                message.append(self._stranger_info.reply)
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

    async def text_render(self, text: str | None = None) -> MessageSegment:
        if text:
            render_response = await self._text_render.render(text)
            if render_response.code == 200:
                message = MessageSegment.image(render_response.data.image_url)
            else:
                await self.send_response(render_response)
        return message