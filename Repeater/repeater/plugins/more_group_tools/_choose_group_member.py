import random
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

choose_group_member = on_command("chooseGroupMember", aliases={"cgm",'choose_group_member', 'Choose_Group_Member', 'ChooseGroupMember'}, rule=to_me(), block=True)

@choose_group_member.handle()
async def choose_group_member_handle(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    reply = MessageSegment.reply(event.message_id) # 获取回复消息头
    if args.extract_plain_text():
        try:
            whatever, group_id, user_id = event.get_session_id().split('_')  # 获取当前群聊id，发起人id，返回的格式为group_groupid_userid
            session_id = f"Group:{group_id}:{user_id}"
            mode = "group"
        except:  # 如果上面报错了，意味着发起的是私聊，返回格式为userid
            group_id = None
            user_id = event.get_session_id()
            session_id = f"Private:{user_id}"
            mode = "private"
        
        if mode == "private":
            await choose_group_member.finish(reply + "====Choose_Group_Member====\n私聊模式下无法使用该功能")
        
        try:
            n = int(args.extract_plain_text())
        except (ValueError, TypeError):
            await choose_group_member.finish(reply + "====Choose_Group_Member====\n请输入数字")
        if n > 0 and n < 20:
            text = ""
            member_list = await bot.get_group_member_list(
                group_id = group_id,
                no_cache = False
            )
            if n >= len(member_list):
                await choose_group_member.finish(reply + f"====Choose_Group_Member====\nN过大，请输入小于{len(member_list)}的数字")
            choiced = random.sample(member_list, n)
            for index, member in enumerate(choiced, start = 1):
                nickname = member.get("card")
                if not nickname:
                    nickname = member.get("nickname")
                text += f"[{index}] {nickname}\n"
            if text.endswith("\n"):
                text = text[:-1]
            await choose_group_member.finish(reply + f"====Choose_Group_Member====\n{text}")
        else:
            await choose_group_member.finish(reply + "====Choose_Group_Member====\n请输入1-19之间的数字")


choose_group_member_no_self = on_command("chooseGroupMemberNoSelf", aliases={"cgmns",'choose_group_member_no_self', 'Choose_Group_Member_No_Self', 'ChooseGroupMemberNoSelf'}, rule=to_me(), block=True)

@choose_group_member_no_self.handle()
async def choose_group_member_no_self_handle(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    reply = MessageSegment.reply(event.message_id) # 获取回复消息头
    if args.extract_plain_text():
        try:
            whatever, group_id, user_id = event.get_session_id().split('_')  # 获取当前群聊id，发起人id，返回的格式为group_groupid_userid
            session_id = f"Group:{group_id}:{user_id}"
            mode = "group"
        except:  # 如果上面报错了，意味着发起的是私聊，返回格式为userid
            group_id = None
            user_id = event.get_session_id()
            session_id = f"Private:{user_id}"
            mode = "private"
        
        if mode == "private":
            await choose_group_member_no_self.finish(reply + "====Choose_Group_Member_No_Self====\n私聊模式下无法使用该功能")
        
        try:
            n = int(args.extract_plain_text())
        except (ValueError, TypeError):
            await choose_group_member_no_self.finish(reply + "====Choose_Group_Member_No_Self====\n请输入数字")
        if n > 0 and n < 20:
            text = ""
            member_list = await bot.get_group_member_list(
                group_id = group_id,
                no_cache = False
            )
            if n >= len(member_list):
                await choose_group_member_no_self.finish(reply + f"====Choose_Group_Member_No_Self====\nN过大，请输入小于{len(member_list)}的数字")
            choiced = random.sample(member_list, n)
            for index, member in enumerate(choiced, start = 1):
                nickname = member.get("card")
                if not nickname:
                    nickname = member.get("nickname")
                text += f"[{index}] {nickname}\n"
            if text.endswith("\n"):
                text = text[:-1]
            await choose_group_member_no_self.finish(reply + f"====Choose_Group_Member_No_Self====\n{text}")
        else:
            await choose_group_member_no_self.finish(reply + "====Choose_Group_Member_No_Self====\n请输入1-19之间的数字")