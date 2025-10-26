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

