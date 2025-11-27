from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment, Message
from nonebot.internal.matcher.matcher import Matcher
from nonebot.exception import FinishedException
from ..core_net_configs import RepeaterDebugMode, storage_config
from ._http_code import HTTP_Code
from ._persona_info import PersonaInfo
from ._namespace import MessageSource
from ._text_render import TextRender
from ._response_body import Response
from ..chattts import ChatTTSAPI
from typing import (
    Callable,
    Any,
    NoReturn,
    TypeVar,
    Type,
    overload,
    Literal,
)
from datetime import datetime
from ..logger import logger
import numpy as np

T_RESPONSE = TypeVar("T_RESPONSE")

class SendMsg:
    def __init__(
            self,
            component: str,
            matcher: Type[Matcher],
            persona_info: PersonaInfo,
        ):
        self._component: str = component
        self._persona_info: PersonaInfo = persona_info
        self._matcher: Type[Matcher] = matcher
        self._text_render = TextRender(namespace = self._persona_info.namespace)
        self._prefix: Message = Message()
        self._chat_tts_api = ChatTTSAPI()
    
    def add_prefix(self, prefix: MessageSegment | str):
        self._prefix.append(prefix)
    
    def clear_prefix(self):
        self._prefix = Message()
    
    @property
    def is_debug_mode(self) -> bool:
        return RepeaterDebugMode
    
    @property
    def persona_info(self) -> PersonaInfo:
        return self._persona_info
    
    @property
    def matcher(self) -> Type[Matcher]:
        return self._matcher
    
    @property
    def component(self) -> str:
        return self._component
    
    @property
    def hello_content(self) -> str:
        now = datetime.now()
        if len(storage_config.welcome_messages_by_weekday) == 0:
            return storage_config.hello_content
        weekday = now.weekday() + 1
        weekday_str = now.strftime('%A')
        weekday_abridge = now.strftime('%a')
        if weekday in storage_config.welcome_messages_by_weekday:
            return storage_config.welcome_messages_by_weekday[weekday]
        elif str(weekday) in storage_config.welcome_messages_by_weekday:
            return storage_config.welcome_messages_by_weekday[str(weekday)]
        elif weekday_str in storage_config.welcome_messages_by_weekday:
            return storage_config.welcome_messages_by_weekday[weekday_str]
        elif weekday_abridge in storage_config.welcome_messages_by_weekday:
            return storage_config.welcome_messages_by_weekday[weekday_abridge]
        else:
            return storage_config.hello_content
    
    @overload
    async def send_debug_mode(
            self,
            reply: bool = True,
            continue_handler: Literal[False] = False,
        ) -> NoReturn: ...

    @overload
    async def send_debug_mode(
            self,
            reply: bool = True,
            continue_handler: Literal[True] = True,
        ) -> None: ...
    
    async def send_debug_mode(
            self,
            reply: bool = True,
            continue_handler: bool = False,
        ):
        """
        用于调试模式的信息打印

        :param reply: 是否携带引用
        :param continue_handler: 是否继续运行当前处理流程
        """
        await self._send(
            self._persona_info.reply + (
                f"[{self._component}|{self._persona_info.namespace}|{self._persona_info.nickname}]: {self._persona_info.message}"
            ),
            reply = reply,
            continue_handler = continue_handler,
        )
    
    @overload
    async def send_response(
            self,
            response: Response[T_RESPONSE],
            message: Callable[[Response[T_RESPONSE]], str] | str | None = None,
            reply: bool = True,
            continue_handler: Literal[False] = False,
        ) -> NoReturn: ...

    @overload
    async def send_response(
            self,
            response: Response[T_RESPONSE],
            message: Callable[[Response[T_RESPONSE]], str] | str | None = None,
            reply: bool = True,
            continue_handler: Literal[True] = True,
        ) -> None: ...
    
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
        :param continue_handler: 是否继续运行当前处理流程
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
    
    @overload
    async def send_multiple_responses(
            self,
            *responses: Response[T_RESPONSE] | tuple[Response[T_RESPONSE], str],
            reply: bool = True,
            continue_handler: Literal[False] = False
        ) -> NoReturn: ...
    
    @overload
    async def send_multiple_responses(
            self,
            *responses: Response[T_RESPONSE] | tuple[Response[T_RESPONSE], str],
            reply: bool = True,
            continue_handler: Literal[True] = True
        ) -> None: ...
    
    async def send_multiple_responses(
            self,
            *responses: Response[T_RESPONSE] | tuple[Response[T_RESPONSE], str],
            reply: bool = True,
            continue_handler: bool = False,
        ):
        """
        发送多个响应对象中的内容，主要用于HTTP错误提示

        :param responses: 响应对象
        :param reply: 是否携带引用
        :param continue_handler: 是否继续运行当前处理流程
        """
        text_buffer: list[str] = []
        failed: int = 0
        for index, response in enumerate(responses, start=1):
            if isinstance(response, tuple):
                text_buffer.append(f"[{response[1]}] HTTP Code: {response[0].code}({HTTP_Code(response[0].code)})")
                if response[0].code != 200:
                    failed += 1
            elif isinstance(response, Response):
                text_buffer.append(f"[{index}] HTTP Code: {response.code}({HTTP_Code(response.code)})")
                if response.code != 200:
                    failed += 1
            else:
                raise TypeError(f"Unsupported type: {type(response)}")
        
        if failed == 0:
            text_buffer.append("All requests are successful.")
        else:
            text_buffer.append(f"{failed} requests failed.")
        
        await self.send_prompt(
            "\n".join(text_buffer),
            reply = reply,
            continue_handler = continue_handler
        )
    
    @overload
    async def send_hello(
            self,
            reply: bool = True,
            continue_handler: Literal[False] = False,
        ) -> NoReturn: ...
    
    @overload
    async def send_hello(
            self,
            reply: bool = True,
            continue_handler: Literal[True] = True,
        ) -> None: ...
    
    async def send_hello(
            self,
            reply: bool = True,
            continue_handler: bool = False,
        ):
        """
        发送欢迎信息

        :param reply: 是否携带引用
        :param continue_handler: 是否继续运行当前处理流程
        """
        await self.send_text(
            self.hello_content,
            reply = reply,
            continue_handler = continue_handler
        )
    
    @overload
    async def send_prompt(
            self,
            prompt: str,
            reply: bool = True,
            continue_handler: Literal[False] = False,
        ) -> NoReturn: ...

    @overload
    async def send_prompt(
            self,
            prompt: str,
            reply: bool = True,
            continue_handler: Literal[True] = True,
        ) -> None: ...
    
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
        :param continue_handler: 是否继续运行当前处理流程
        """
        await self._send(
            (
                f"==== {self._component} ====\n"
                f"> [{self._persona_info.namespace}]\n"
                f"{prompt}"
            ),
            reply = reply,
            continue_handler = continue_handler
        )
    
    @overload
    async def send_error(
            self,
            error: str,
            reply: bool = True,
            continue_handler: Literal[False] = False,
        ) -> NoReturn: ...

    @overload
    async def send_error(
            self,
            error: str,
            reply: bool = True,
            continue_handler: Literal[True] = True,
        ) -> None: ...
    
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
        :param continue_handler: 是否继续运行当前处理流程
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
    
    @overload
    async def send_warning(
            self,
            warning: str,
            reply: Message = None,
            continue_handler: Literal[True] = True
        ) -> None: ...

    @overload
    async def send_warning(
            self,
            warning: str,
            reply: Message = None,
            continue_handler: Literal[False] = False
        ) -> NoReturn: ...
    
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
        :param continue_handler: 是否继续运行当前处理流程
        """
        await self.send_prompt(
            (
                f"Warning: {warning}"
            ),
            reply = reply,
            continue_handler = continue_handler
        )
    @overload
    async def send_text(
            self,
            text: str | None = None,
            reply: bool = True,
            continue_handler: Literal[False] = False
        ) -> NoReturn: ...
    
    async def send_text(
            self,
            text: str | None = None,
            reply: bool = True,
            continue_handler: Literal[True] = True
        ) -> None: ...
    
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
        :param continue_handler: 是否继续运行当前处理流程
        """
        await self._send(
            Message(text),
            reply=reply,
            continue_handler = continue_handler
        )
    
    @overload
    
    async def send_mixed_render(
            self,
            text: str,
            text_to_render: str,
            reply: bool = False,
            continue_handler: Literal[False] = False
        ) -> NoReturn: ...
    
    @overload
    async def send_mixed_render(
            self,
            text: str,
            text_to_render: str,
            reply: bool = False,
            continue_handler: Literal[True] = True
        ) -> None: ...
    
    async def send_mixed_render(
            self,
            text: str,
            text_to_render: str,
            reply: bool = False,
            continue_handler: bool = False
        ):
        """
        发送混合渲染文本

        :param text: 普通文本内容
        :param text_to_render: 需要渲染的文本内容
        :param reply: 是否携带引用
        :param continue_handler: 是否继续运行当前处理流程
        """
        image = await self.text_render(text)
        await self._send(
            Message(
                [
                    MessageSegment.text(text_to_render),
                    image,
                ]
            ),
            reply=reply,
            continue_handler = continue_handler
        )

    @overload
    async def send_render(
            self,
            text: str | None = None,
            reply: bool = True,
            continue_handler: Literal[False] = False
        ) -> NoReturn: ...
    
    @overload
    async def send_render(
            self,
            text: str | None = None,
            reply: bool = True,
            continue_handler: Literal[True] = True
        ) -> None: ...
    
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
    
    @overload
    async def send_tts(
            self,
            text: str | None = None,
            reply: bool = False,
            continue_handler: Literal[False] = False
        ) -> NoReturn: ...

    @overload
    async def send_tts(
            self,
            text: str | None = None,
            reply: bool = False,
            continue_handler: Literal[True] = True
        ) -> None: ...
    
    async def send_tts(
            self,
            text: str | None = None,
            send_error_message: bool = True,
            reply: bool = False,
            continue_handler: bool = False
        ):
        """
        发送tts

        :param text: 文本
        :param reply: 是否回复
        :param continue_handler: 是否继续处理流程
        """
        response = await self._chat_tts_api.text_to_speech(text)
        if response.code == 200:
            await self._send(
                message = MessageSegment.record(response.data.audio_files[0].url),
                reply = reply,
                continue_handler = continue_handler
            )
        elif send_error_message:
            await self.send_response(response, message = "TTS Error.")
        else:
            logger.error(f"Send TTS Error: {response.code} {response.text}")
    
    @overload
    async def send_check_length(
            self,
            text: str | None = None,
            threshold: float = 1.0,
            reply: bool = True,
            continue_handler: Literal[False] = False
        ) -> NoReturn: ...
    
    @overload
    async def send_check_length(
            self,
            message: Message,
            threshold: float = 1.0,
            reply: bool = True,
            continue_handler: Literal[True] = True
        ) -> None: ...
    
    async def send_check_length(
            self,
            message: Message | str | None = None,
            threshold: float = 1.0,
            reply: bool = True,
            continue_handler: Literal[False] = False
        ):
        length_score = self.text_length_score(message)
        if length_score >= threshold:
            self.send_render(
                message,
                reply = reply,
                continue_handler = continue_handler
            )
        else:
            self.send_text(
                message,
                reply = reply,
                continue_handler = continue_handler
            )
    
    @overload
    async def send_any(
            self,
            message: Message,
            reply: bool = False,
            continue_handler: Literal[False] = False
        ) -> NoReturn: ...

    @overload
    async def send_any(
            self,
            message: MessageSegment,
            reply: bool = False,
            continue_handler: Literal[True] = True
        ) -> None: ...
    
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
    
    @overload
    async def _send(
            self,
            message: Message,
            reply: bool = True,
            continue_handler: Literal[False] = False
        ) -> NoReturn: ...
    
    @overload
    async def _send(
            self,
            message: Message,
            reply: bool = True,
            continue_handler: Literal[True] = True
        ) -> None: ...
    
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
            send_msg = self._persona_info.reply + send_msg
        await self._matcher.send(send_msg)
        if not continue_handler:
            await self.break_handler()
    
    @staticmethod
    def text_length_score(text:str) -> float:
        lines = text.splitlines()
        line_lengths = np.array([len(line) for line in lines], dtype=np.int64)
        lines_score = len(lines) / storage_config.text_length_score_configs.max_lines
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
    
    @property
    def text_length_score_threshold(self) -> float:
        if self._persona_info.source == MessageSource.GROUP:
            threshold = storage_config.text_length_score_configs.threshold.group
        else:
            threshold = storage_config.text_length_score_configs.threshold.private

        return threshold