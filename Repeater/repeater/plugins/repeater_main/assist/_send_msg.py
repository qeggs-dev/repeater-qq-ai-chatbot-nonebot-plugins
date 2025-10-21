from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment, Message
from nonebot.internal.matcher.matcher import Matcher
from nonebot.exception import FinishedException
from ..core_net_configs import RepeaterDebugMode, HELLO_CONTENT
from ._http_code import HTTP_Code
from ._stranger_info import StrangerInfo
from ._text_render import TextRender
from ._response_body import Response
from typing import Callable, Any, NoReturn, TypeVar, Type

T_RESPONSE = TypeVar("T_RESPONSE")

class SendMsg:
    def __init__(
            self,
            component: str,
            matcher: Type[Matcher],
            stranger_info: StrangerInfo,
        ):
        self._component: str = component
        self._stranger_info: StrangerInfo = stranger_info
        self._matcher: Type[Matcher] = matcher
        self._text_render = TextRender(namespace = self._stranger_info.namespace)
        self._prefix: Message = Message()
    
    def add_prefix(self, prefix: MessageSegment | str):
        self._prefix.append(prefix)
    
    def clear_prefix(self):
        self._prefix = Message()
    
    @property
    def is_debug_mode(self) -> bool:
        return RepeaterDebugMode
    
    @property
    def stranger_info(self) -> StrangerInfo:
        return self._stranger_info
    
    @property
    def matcher(self) -> Type[Matcher]:
        return self._matcher
    
    @property
    def component(self) -> str:
        return self._component
    
    @property
    def hello_content(self) -> str:
        return HELLO_CONTENT
    
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
            self._stranger_info.reply + (
                f"[{self._component}|{self._stranger_info.namespace}|{self._stranger_info.nickname}]: {self._stranger_info.message}"
            ),
            reply = reply,
            continue_handler = continue_handler,
        )

    
    async def send_response(
            self,
            response: Response[T_RESPONSE],
            message: Callable[[Response[T_RESPONSE]], str] | str | None = None,
            reply: bool = True,
            continue_handler: bool = False,
        ):
        """
        发送响应对象中的内容，主要用于HTTP错误提示

        :param response: 响应对象
        :param component: 组件名称
        :param message_handler: 自定义消息文本解析处理函数
        :param reply: 是否携带引用
        """
        if callable(message):
            message = message(response)
        elif isinstance(message, str):
            message = message
        else:
            message = response.text
        await self.send_prompt(
            (
                f"{message}\n"
                f"HTTP Code: {response.code}({HTTP_Code(response.code)})"
            ),
            reply = reply,
            continue_handler = continue_handler
        )
    
    async def send_prompt(
            self,
            prompt: str,
            reply: bool = True,
            continue_handler: bool = False
        ):
        """
        发送提示信息

        :param prompt: 提示信息
        :param reply: 是否携带引用
        :param continue_handler: 是否继续处理
        """
        await self._send(
            (
                f"==== {self._component} ====\n"
                f"> [{self._stranger_info.namespace}]\n"
                f"{prompt}"
            ),
            reply = reply,
            continue_handler = continue_handler
        )
    
    async def send_error(
            self,
            error: str,
            reply: bool = True,
            continue_handler: bool = False
        ):
        """
        发送错误信息

        :param error: 错误信息
        :param reply: 是否携带引用
        :param continue_handler: 是否继续处理
        """
        if isinstance(error, Exception):
            await self.send_prompt(
                (
                    f"{error.__class__.__name__}: {error}"
                ),
                reply = reply,
                continue_handler = continue_handler
            )
        else:
            await self.send_prompt(
                (
                    f"Error: {error}"
                ),
                reply = reply,
                continue_handler = continue_handler
            )
    
    async def send_warning(
            self,
            warning: str,
            reply: bool = True,
            continue_handler: bool = True
        ):
        """
        发送警告信息

        :param warning: 警告信息
        :param reply: 是否携带引用
        :param continue_handler: 是否继续处理
        """
        await self.send_prompt(
            (
                f"Warning: {warning}"
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
        send_msg = self._prefix + message
        if reply:
            send_msg = self._stranger_info.reply + send_msg
        await self._matcher.send(send_msg)
        if not continue_handler:
            await self.break_handler()