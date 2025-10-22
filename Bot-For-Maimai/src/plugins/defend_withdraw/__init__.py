from nonebot import get_plugin_config, on_notice
from nonebot.plugin import PluginMetadata
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Message, GroupRecallNoticeEvent, Bot

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="defend_withdraw",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

defend_withdraw = on_notice()

@defend_withdraw.handle()
async def _(bot: Bot, event: GroupRecallNoticeEvent, state: T_State):
    if event.group_id in config.access_groups: # type: ignore
        mid = event.message_id
        response = await bot.get_msg(message_id = mid)
        print(response['message'])
        print(1)
        await bot.send_group_msg(
            group_id=event.group_id,
            message=Message(f"检测到撤回消息：\n发送者：{event.user_id}\n消息ID：{mid}\n消息内容：{response['message']}"),
        )