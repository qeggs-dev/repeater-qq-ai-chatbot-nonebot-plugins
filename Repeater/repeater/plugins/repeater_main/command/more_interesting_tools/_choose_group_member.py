import random
from typing import Any
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

choose_group_member = on_command("chooseGroupMember", aliases={"cgm",'choose_group_member', 'Choose_Group_Member', 'ChooseGroupMember'}, rule=to_me(), block=True)

@choose_group_member.handle()
async def choose_group_member_handle(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    stranger_info = StrangerInfo(bot, event, args)
    mode = stranger_info.mode
    reply = stranger_info.reply
    
    if mode == MessageSource.PRIVATE:
        await choose_group_member.finish(reply + "====Choose_Group_Member====\n私聊模式下无法使用该功能")
    
    group_id = stranger_info.group_id
    
    try:
        n = int(args.extract_plain_text())
    except (ValueError, TypeError):
        await choose_group_member.finish(reply + "====Choose_Group_Member====\n请输入数字")
    if n > 0:
        text = ""
        member_list = await bot.get_group_member_list(
            group_id = group_id,
            no_cache = False
        )
        if n > len(member_list):
            await choose_group_member.finish(reply + f"====Choose_Group_Member====\nN过大，请输入小于等于{len(member_list)}的数字")
        choiced: list[dict[str, Any]] = random.sample(member_list, n)
        text_list: list[str] = []
        for index, member in enumerate(choiced, start = 1):
            nickname = member.get("card")
            if not nickname:
                nickname = member.get("nickname")
            text_list.append(f"[{index}] {nickname}")
        text = "\n".join(text_list)
        message = reply + f"====Choose_Group_Member====\n"
        if n > 10:
            text_render = TextRender(stranger_info.name_space)
            image = await text_render.render(text)
            if image.status_code == 200:
                message += MessageSegment.image(image.image_url)
            else:
                message += f"Error: Render Error\n{image.response_text}"
        else:
            message += text
        await choose_group_member.finish(message)
    else:
        await choose_group_member.finish(reply + "====Choose_Group_Member====\n请输入大于0的数字")