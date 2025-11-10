from nonebot import get_plugin_config, on_command, on_message
from nonebot.plugin import PluginMetadata
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Message, Event, Bot
from nonebot.rule import to_me
from nonebot.params import CommandArg

from .config import Config
from .room import Room

__plugin_meta__ = PluginMetadata(
    name="room",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

get_room = on_command("房间信息", rule=to_me(), priority=5, block=True, aliases={"查看房间, roominfo, ri"})

@get_room.handle()
async def handle_room_info(bot: Bot, event: Event, state: T_State, msg: Message = CommandArg()):
    group_id = str(event.group_id) # type: ignore
    user_id = str(event.user_id) # type: ignore

    room = Room(group_id, user_id)
    info = room.get_room_info()
    await get_room.finish(info, reply_message=True)