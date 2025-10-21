from nonebot import get_plugin_config, on_command
from nonebot.typing import T_State
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11 import Message, Event, Bot
from nonebot.rule import to_me
from nonebot.params import CommandArg

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="help",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)


#注册事件响应器
help = on_command("help", priority=10, block=False, aliases={"帮助", "h"}, rule=to_me()) 

@help.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State, args: Message = CommandArg()): # type: ignore
    content = args.extract_plain_text()
    if content:
        await help.finish(f"笨蛋~你发了什么帮助喵~\n你是想问 '{content}' 吗？\n抱歉人家还不会回答这个问题喵~")
    msg = (
        "人家是一个多功能机器人喵~\n"
        "目前人家会的功能有：\n"
        "1. 约会功能（约、月、🈷）\n"
        "2. 更新功能（更新）\n"
        "3. 帮助功能（帮助、h、help）（就是这个！你正在用~杂鱼~）\n"
        "4. 舞萌数据导入功能，使用“导”来导入水鱼网数据，使用maibind&dfbind绑定token~\n"
        "5. 面包功能，使用“领取面包”来领取面包，使用“偷面包”来偷取他人面包，具体可以收纳柜用“面包帮助”指令了解\n"
        "6. 其他功能正在开发中喵~敬请期待喵~❤\n\n"
        "如果你是主人，可以使用 '更新' 命令来调教人家哦~❤\n"
        "如果你想了解某个功能的使用方法，可以发送 '功能名 帮助' 来获取帮助喵~\n"
        "比如：发送 '约 帮助、dhelp' 来获取约会功能的使用方法喵~\n"
        "记得@我哦~❤"
    )
    await help.finish(msg)

