from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment, Message
from nonebot.internal.matcher.matcher import Matcher
from ._core import ChatCore, RepeaterDebugMode, MAX_SINGLE_LINE_LENGTH, MIN_RENDER_IMAGE_TEXT_LINE, MAX_LENGTH
from ....assist import StrangerInfo, MessageSource, Response, TextRender, RendedImage
from ._response_body import ChatResponse
from typing import Callable, Any
from nonebot import logger

class Send_msg:
    def __init__(
            self,
            component: str,
            stranger_info: StrangerInfo,
            matcher: Matcher,
            response: Response[ChatResponse],
        ):
        self.component: str = component
        self.stranger_info: StrangerInfo = stranger_info
        self.matcher: Matcher = matcher
        self.response: Response[ChatResponse] = response
        self._text_render = TextRender(namespace = self.stranger_info.namespace)

    async def send(self):
        if RepeaterDebugMode:
            await self.send_debug_mode()
        else:
            if self.response.code == 200:
                message = Message()
                lines = self.response.data.content.splitlines()
                max_line_length = max([len(line) for line in lines]) if lines else 0
                logger.debug(f"Response content has {len(lines)} lines, max line length is {max_line_length}.")

                if self.response.data.reasoning_content:
                    render_response = await self.text_render(self.response.data.reasoning_content)
                    message.append(render_response)
                
                if (self.stranger_info.mode == MessageSource.GROUP and (len(lines) > MIN_RENDER_IMAGE_TEXT_LINE or max_line_length > MAX_SINGLE_LINE_LENGTH)) or len(self.response.data.content) > MAX_LENGTH:
                    if self.response.data.content:
                        render_response = await self.text_render(self.response.data.content)
                        message.append(render_response)
                else:
                    message.append(self.response.data.content)
            
                await self.matcher.finish(self.stranger_info.reply + message)
            else:
                await self.send_error(self.response)
    
    async def send_debug_mode(self):
        await self.matcher.finish(self.stranger_info.reply + f'[{self.component}|{self.stranger_info.namespace}|{self.stranger_info.nickname}]: {self.stranger_info.message}')
    
    async def send_error(
            self,
            response: Response,
            component: str | None = None,
            message_handler: Callable[[Response[Any]], str] | None = None,
        ):
        if callable(message_handler):
            message = message_handler(response)
        else:
            message = response.text
        await self.matcher.finish(self.stranger_info.reply + f"===={component or self.component}====\n> {self.stranger_info.namespace}\n{message}\nHTTP Code: {response.code}")
    
    async def send_text(self, text: str | None = None):
        if RepeaterDebugMode:
            await self.send_debug_mode()
        else:
            if self.response.code == 200:
                message = Message()
                message.append(self.stranger_info.reply)
                # 推理内容必须渲染为图片
                if self.response.data.reasoning_content:
                    message.append(
                        await self.text_render(self.response.data.reasoning_content)
                    )
                if self.response.data.content:
                    message.append(text or self.response.data.content)
                else:
                    message.append("Message is empty.")
                await self.matcher.finish(message)
            else:
                await self.send_error(self.response, text)
    
    async def send_image(self, text: str | None = None):
        if RepeaterDebugMode:
            await self.send_debug_mode()
        else:
            if self.response.code == 200:
                message = Message()
                message.append(self.stranger_info.reply)
                if self.response.data.reasoning_content:
                    message.append(
                        await self.text_render(self.response.data.reasoning_content)
                    )
                if self.response.data.content:
                    message.append(
                        await self.text_render(self.response.data.content)
                    )
                else:
                    message.append("Message is empty.")
                await self.matcher.finish(message)
            else:
                await self.send_error(self.response, text)

    async def text_render(self, text: str | None = None) -> MessageSegment:
        if text:
            render_response = await self._text_render.render(text)
            if render_response.code == 200:
                message = MessageSegment.image(render_response.data.image_url)
            else:
                await self.send_error(render_response, text)
        return message