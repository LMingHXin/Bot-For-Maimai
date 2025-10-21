from nonebot import get_plugin_config, on_command, on_message
from nonebot.plugin import PluginMetadata
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Message, Event, Bot
from nonebot.rule import to_me
from nonebot.params import CommandArg


from .config import Config

__plugin_meta__ = PluginMetadata(
    name="version",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)


#注册事件响应器
version = on_command("version", priority=10, block=False, aliases={"版本", "v"}, rule=to_me())


@version.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State, args: Message = CommandArg()): # type: ignore
    content = args.extract_plain_text()
    msg = (
        "人家现在的版本是 1.0.0 喵~\n"
        "开发人员是铭心和美好一天哦~❤\n"
        "他们也是我的主人哦~❤\n"
        "有问题可以找他们哦~❤\n"
    )
    await version.finish(msg)

