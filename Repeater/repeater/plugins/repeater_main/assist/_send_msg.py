from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment, Message
from nonebot.internal.matcher.matcher import Matcher
from nonebot.exception import FinishedException
from ._stranger_info import StrangerInfo
from ._text_render import TextRender
from ._response_body import Response
from typing import Callable, Any, NoReturn
from nonebot import logger

class SendMsg:
    def __init__(
            self,
            component: str,
            matcher: Matcher,
            stranger_info: StrangerInfo,
        ):
        self.component: str = component
        self.stranger_info: StrangerInfo = stranger_info
        self.matcher: Matcher = matcher
        self._text_render = TextRender(namespace = self.stranger_info.namespace)
    
    async def send_debug_mode(
            self,
            reply: bool = True,
            continue_handler: bool = False,
        ):
        """
        用于调试模式的信息打印

        :param reply: 是否携带引用
        """
        await self._send(
            self.stranger_info.reply + (
                f"[{self.component}|{self.stranger_info.namespace}|{self.stranger_info.nickname}]: {self.stranger_info.message}"
            ),
            reply = reply,
            continue_handler = continue_handler,
        )
    
    async def send_response(
            self,
            response: Response,
            component: str | None = None,
            message_handler: Callable[[Response[Any]], str] | None = None,
            reply: bool = True,
            continue_handler: bool = False,
        ):
        """
        发送响应对象中的内容，主要用于错误提示

        :param response: 响应对象
        :param component: 组件名称
        :param message_handler: 自定义消息文本解析处理函数
        :param reply: 是否携带引用
        """
        if callable(message_handler):
            message = message_handler(response)
        else:
            message = response.text
        await self._send(
            self.stranger_info.reply + (
                f"===={component or self.component}====\n"
                f"> {self.stranger_info.namespace}\n"
                f"{message}\n"
                f"HTTP Code: {response.code}"
            ),
            reply = reply,
            continue_handler = continue_handler
        )
    
    async def send_text(
            self,
            text: str | None = None,
            reply: bool = True,
            continue_handler: bool = False
        ):
        """
        发送纯文本

        :param text: 文本内容
        :param reply: 是否携带引用
        """
        await self._send(
            Message(text),
            reply=reply,
            continue_handler = continue_handler
        )
    
    async def send_render(
            self,
            text: str | None = None,
            reply: bool = True,
            continue_handler: bool = False
        ):
        """
        发送渲染后的文本

        :param text: 渲染文本内容
        :param reply: 是否携带引用
        :param continue_handler: 是否继续运行当前处理流程
        """
        image = await self.text_render(text)
        await self._send(
            Message(image),
            reply=reply,
            continue_handler = continue_handler
        )
    
    async def send_any(
            self,
            message: Message,
            reply: bool = True,
            continue_handler: bool = False
        ):
        """
        发送任意消息

        :param message: 消息对象
        :param reply: 是否携带引用
        :param continue_handler: 是否继续运行当前处理流程
        """
        await self._send(
            message,
            reply=reply,
            continue_handler = continue_handler
        )
    
    async def _send(
            self,
            message: Message,
            reply: bool = True,
            continue_handler: bool = False
        ):
        """
        发送消息

        :param message: 消息对象
        :param reply: 是否携带引用
        :param continue_handler: 是否继续运行当前处理流程
        """
        if reply:
            message = self.stranger_info.reply + message
        await self.matcher.send(message)
        if not continue_handler:
            await self.break_handler()
    
    async def break_handler(self) -> NoReturn:
        """
        跳出当前处理函数
        """
        raise FinishedException

    async def text_render(self, text: str | None = None) -> MessageSegment:
        """
        渲染文本

        :param text: 渲染文本内容
        """
        if text:
            render_response = await self._text_render.render(text)
            if render_response.code == 200:
                message = MessageSegment.image(render_response.data.image_url)
            else:
                await self.send_response(render_response, text)
        return message