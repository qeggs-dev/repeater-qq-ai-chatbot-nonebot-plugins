from typing import Literal
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment, Message
from nonebot.internal.matcher.matcher import Matcher
from ._core import ChatCore, RepeaterDebugMode, MAX_SINGLE_LINE_LENGTH, MIN_RENDER_IMAGE_TEXT_LINE, MAX_LENGTH
from ...assist._get_stranger_info import StrangerInfo, MessageSource
from ._response_body import ResponseBody
from nonebot import logger

async def send_msg(
        id: str,
        stranger_info: StrangerInfo,
        matcher: Matcher,
        response: ResponseBody,
        must: Literal["image", "text"] | None = None,
    ):
    chat_core = ChatCore(stranger_info.name_space)
    if must not in {"image", "text", None}:
        raise ValueError("Parameter 'must' must be 'image', 'text', or None.")
    if RepeaterDebugMode:
        await matcher.finish(stranger_info.reply + f'[{id}|{stranger_info.name_space}|{stranger_info.nickname}]：{stranger_info.message}')
    else:
        if response.status_code == 200:
            message = Message()
            lines = response.content.splitlines()
            max_line_length = max([len(line) for line in lines]) if lines else 0
            logger.debug(f"Response content has {len(lines)} lines, max line length is {max_line_length}.")
            if response.reasoning_content:
                render_response = await chat_core.text_render(response.reasoning_content)
                message.append(MessageSegment.image(render_response.image_url))
            
            if must is None:
                if (stranger_info.mode == MessageSource.GROUP and (len(lines) > MIN_RENDER_IMAGE_TEXT_LINE or max_line_length > MAX_SINGLE_LINE_LENGTH)) or len(response.content) > MAX_LENGTH:
                    if response.content:
                        render_response = await chat_core.text_render(response.content)
                        message.append(MessageSegment.image(render_response.image_url))
                else:
                    message.append(response.content)
            else:
                if must == "image":
                    if response.content:
                        render_response = await chat_core.text_render(response.content)
                        message.append(MessageSegment.image(render_response.image_url))
                elif must == "text":
                    message.append(response.content)
                else:
                    raise ValueError("Parameter 'must' must be 'image', 'text', or None.")
        
            await matcher.finish(stranger_info.reply + message)
        else:
            await matcher.finish(stranger_info.reply + f"====Chat.{id}====\n> {stranger_info.name_space}\n{response}\nHTTP Code: {response.status_code}")