from typing import Literal
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.internal.matcher.matcher import Matcher
from .core import ChatCore, RepeaterDebugMode, MAX_SINGLE_LINE_LENGTH, MIN_RENDER_IMAGE_TEXT_LINE, MAX_LENGTH
from ._get_stranger_info import StrangerInfo

async def send_msg(
        id: str,
        stranger_info: StrangerInfo,
        matcher: Matcher,
        message: dict[Literal["status_code", "response_text", "reasoning", "content"], str | int]
    ):
    chat_core = ChatCore(stranger_info.name_space)
    if RepeaterDebugMode:
        await matcher.finish(stranger_info.reply + f'[{id}|{stranger_info.name_space}|{stranger_info.nickname}]：{msg}')
    else:
        response = message
        lines = response['content'].split('\n')
        max_line_length = max(len(line) for line in lines) if lines else 0
        if response['status_code'] == 200:
            if (stranger_info.mode == "group" and (max_line_length < MAX_SINGLE_LINE_LENGTH or len(response['content'].split('\n')) > MIN_RENDER_IMAGE_TEXT_LINE)) or len(response['response_text']) > MAX_LENGTH:
                render_response = await chat_core.content_render(response['content'], response['reasoning'])
                message = MessageSegment.image(render_response['image_url'])
            else:
                message = response['content']
            await matcher.finish(stranger_info.reply + message)
        else:
            await matcher.finish(stranger_info.reply + f"====Chat.{id}====\n> {stranger_info.name_space}\n{response}\nHTTP Code: {response['status_code']}")