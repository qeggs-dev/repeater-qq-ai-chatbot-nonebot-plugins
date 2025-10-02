import random
from typing import Any
from pydantic import ValidationError
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters import Message
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.adapters import Bot
from nonebot.params import (
    CommandArg,
    ArgPlainText,
    Arg
)
from ...assist import StrangerInfo, MessageSource, RendedImage, TextRender

recent_speaking_ranking = on_command("recentSpeakingRanking", aliases={"rsr",'recent_speaking_ranking', 'Recent_Speaking_Ranking', 'RecentSpeakingRanking'}, rule=to_me(), block=True)

@recent_speaking_ranking.handle()
async def recent_speaking_ranking_handle(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot, event, args)
    mode = stranger_info.mode
    reply = stranger_info.reply
    
    if mode == MessageSource.PRIVATE:
        await recent_speaking_ranking.finish(reply + "====Recent_Speaking_Ranking====\n私聊模式下无法使用该功能")
    
    group_id = stranger_info.group_id
    
    try:
        n = int(args.extract_plain_text())
    except (ValueError, TypeError):
        await recent_speaking_ranking.finish(reply + "====Recent_Speaking_Ranking====\n请输入数字")
    if n > 0:
        text = ""
        message_list = await bot.get_group_msg_history(
            group_id = group_id,
            count = n
        )
        member_speech_count: dict[str, int] = {}
        validation_failure_counter: int = 0
        for message in message_list["messages"]:
            try:
                event = MessageEvent(**message)
                member_name = event.sender.card or event.sender.nickname
            except ValidationError:
                try:
                    member_name = message["sender"]["card"] or message["sender"]["nickname"]
                except KeyError:
                    validation_failure_counter += 1
                    continue
            if member_name not in member_speech_count:
                member_speech_count[member_name] = 1
            else:
                member_speech_count[member_name] += 1
        
        member_speech_count_list = list(member_speech_count.items())
        sorted_member_speech_count_list = sorted(member_speech_count_list, key=lambda x: x[1], reverse=True)

        text_list: list[str] = []
        for index, (name, speech_count) in enumerate(sorted_member_speech_count_list, start = 1):
            text_list.append(f"[{index}] {name}: {speech_count}")
        text = "\n".join(text_list)

        message = reply + f"====Recent_Speaking_Ranking====\n"
        if validation_failure_counter > 0:
            message += f"Warning: There are {validation_failure_counter} message verification failures.\n"
        line_count = text.count('\n') + 1
        
        if line_count > 10:
            text_render = TextRender(stranger_info.name_space)
            image = await text_render.render(text)
            if image.status_code == 200:
                message += MessageSegment.image(image.image_url)
            else:
                message += f"Error: Render Error\n{image.response_text}"
        else:
            message += text
        await recent_speaking_ranking.finish(message)
    else:
        await recent_speaking_ranking.finish(reply + "====Recent_Speaking_Ranking====\n请输入大于0的数字")