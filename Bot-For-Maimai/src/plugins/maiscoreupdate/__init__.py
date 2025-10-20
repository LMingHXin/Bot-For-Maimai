from nonebot import get_plugin_config, on_command, on_message
from nonebot.plugin import PluginMetadata
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Message, Event, Bot
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot_plugin_alconna.uniseg import message_recall
from .main import core

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="maiscoreupdate",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

# 注册事件响应器
maiupdate = on_command("maiscoreupdate", priority=5, block=False, aliases = {"导"})  #更新舞萌分数
maibind = on_command("maibind", priority=5, block=False)  #绑定舞萌TOKEN
dfbind = on_command("dfbind", priority=5, block=False)  #绑定水鱼TOKEN

@maiupdate.handle()
async def handle_maiupdate(bot: Bot, event: Event, state: T_State):
    user_id = int(event.get_user_id())
    core_instance = core(user_id)
    msg = await core_instance.update_maiscore()
    await maiupdate.finish(msg) 

@maibind.handle()
async def handle_maibind(bot: Bot, event: Event, state: T_State, cmd_arg: Message = CommandArg()):
    user_id = int(event.get_user_id())
    token = cmd_arg.extract_plain_text() # type: ignore
    core_instance = core(user_id)
    msg = core_instance.maibind_token(user_id, token)
    id = str(event.message_id)  # type: ignore
    await message_recall(id)
    await maibind.finish(msg)

@dfbind.handle()
async def handle_dfbind(bot: Bot, event: Event, state: T_State, cmd_arg: Message = CommandArg()):
    user_id = int(event.get_user_id())
    token = cmd_arg.extract_plain_text() # type: ignore
    core_instance = core(user_id)
    core_instance = core(user_id)
    msg = core_instance.dfbind_token(user_id, token)
    id = str(event.message_id)  # type: ignore
    await message_recall(id)
    await dfbind.finish(msg)