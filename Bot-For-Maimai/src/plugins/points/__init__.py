from nonebot import get_plugin_config, on_command, on_message
from nonebot.plugin import PluginMetadata
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Message, Event, Bot
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot_plugin_alconna.uniseg import message_recall

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="points",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

help = on_command("points_help", aliases={"积分帮助", "jf_help"})

@help.handle()
async def handle_help(bot: Bot, event: Event, state: T_State):
    help_text = (
        "积分系统使用说明：\n"
        "1. 签到获取基础积分，每日可签到一次。\n"
        "2. 积分可用于兑换面包或其他奖励。\n"
        "3. 面包等级越高，签到时获得的积分越多。\n"
        "4. 使用命令 'check_in' 进行签到。\n"
        "5. 使用命令 'points' 查询当前积分。"
        "积分结算机制：(面包等级/20 + 1) * 基础积分"
    )
    await help.finish(help_text)

