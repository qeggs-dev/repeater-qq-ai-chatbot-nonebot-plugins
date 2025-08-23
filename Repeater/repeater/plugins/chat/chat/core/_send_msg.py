from typing import Literal
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment, Message
from nonebot.internal.matcher.matcher import Matcher
from ._core import ChatCore, RepeaterDebugMode, MAX_SINGLE_LINE_LENGTH, MIN_RENDER_IMAGE_TEXT_LINE, MAX_LENGTH
from ...assist._get_stranger_info import StrangerInfo
from ._response_body import ResponseBody

async def send_msg(
        id: str,
        stranger_info: StrangerInfo,
        matcher: Matcher,
        response: ResponseBody,
        must_image: bool = False
    ):
    chat_core = ChatCore(stranger_info.name_space)
    if RepeaterDebugMode:
        await matcher.finish(stranger_info._reply + f'[{id}|{stranger_info.name_space}|{stranger_info.nickname}]：{stranger_info.message}')
    else:
        message = Message()
        lines = response.content.split('\n')
        max_line_length = max(len(line) for line in lines) if lines else 0
        if response.status_code == 200:
            if must_image or (stranger_info.mode == "group" and (max_line_length < MAX_SINGLE_LINE_LENGTH or len(response.content.split('\n')) > MIN_RENDER_IMAGE_TEXT_LINE)) or len(response.content) > MAX_LENGTH:
                if response.reasoning_content:
                    render_response = await chat_core.text_render(response.reasoning_content)
                    message = MessageSegment.image(render_response.image_url)
                if response.content:
                    render_response = await chat_core.text_render(response.content)
                    message += MessageSegment.image(render_response.image_url)
            else:
                message = response.content
            await matcher.finish(stranger_info._reply + message)
        else:
            await matcher.finish(stranger_info._reply + f"====Chat.{id}====\n> {stranger_info.name_space}\n{response}\nHTTP Code: {response['status_code']}")