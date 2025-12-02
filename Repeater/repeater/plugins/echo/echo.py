from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters import Message
from nonebot.matcher import Matcher
from nonebot.params import (
    CommandArg,
    ArgPlainText,
    Arg
)

echo = on_command("echo", aliases={"Echo"}, rule=to_me(), block=True)

@echo.handle()
async def echo_handle(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text():
        matcher.set_arg("echo_text", args)

@echo.got("echo_text", prompt="[Echo] Waiting for input...")
async def echo_got_text(args: Message = Arg("echo_text")):
    if isinstance(args, Message):
        # 如果是消息对象，则直接返回
        await echo.finish(args)
    else:
        # 回退到纯文本模式
        await echo.finish(ArgPlainText())