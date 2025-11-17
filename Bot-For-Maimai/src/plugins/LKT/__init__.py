from nonebot import get_plugin_config, on_command, on_message
from nonebot.plugin import PluginMetadata
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Message, Event, Bot
from nonebot.rule import to_me
from nonebot.params import CommandArg

from .core import stream, round
from .config import Config

__plugin_meta__ = PluginMetadata(
    name="ktt",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

start = on_command("ktt", priority=5, block=False, aliases={"开三国杀", "开始三国杀"}, rule=to_me())  #开始三国杀
join = on_command("join_ktt", priority=5, block=False, aliases={"加入三国杀", "加入ktt"}, rule=to_me())  #加入三国杀

@start.handle()
async def handle_start(bot: Bot, event: Event, state: T_State, args: Message = CommandArg()):
    uid = event.get_user_id()
    gid = event.group_id # type: ignore
    main_step = stream.Main_step(str(uid), str(gid))
    main_step.create()
    main_step.gather()
    state["room_token"] = main_step.room_token
    await bot.send_private_msg(user_id=int(uid), message=f"创建成功~\n房间TOKEN为{main_step.room_token}\n请复制token给群聊以便其他玩家加入~")
    await start.send(group_id=int(gid), message=f"创建了三国杀房间~\n已经私信通知他力！他将复制TOKEN给大家加入！", at_sender=True)