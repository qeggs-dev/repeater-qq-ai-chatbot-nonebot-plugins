from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters import Message
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import (
    MessageEvent,
    MessageSegment
)
from nonebot.params import (
    CommandArg,
    ArgPlainText,
    Arg
)

reply_echo = on_command("replyEcho", aliases={'recho', 'reply_echo', 'Reply_Echo'}, rule=to_me(), block=True)

@reply_echo.handle()
async def reply_echo_handle(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text():
        matcher.set_arg("reply_echo_text", args)

@reply_echo.got("reply_echo_text", prompt="[Echo] Waiting for input...")
async def reply_echo_got_text(event: MessageEvent, args: Message = Arg('reply_echo_text')):
    reply = MessageSegment.reply(event.message_id) # 获取回复消息头
    if isinstance(args, Message):
        # 如果是消息对象，则直接返回
        await reply_echo.finish(args)
    else:
        # 回退到纯文本模式
        await reply_echo.finish(ArgPlainText())