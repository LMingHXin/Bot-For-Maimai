from nonebot import get_plugin_config, on_command
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11 import Message, Event, Bot
from nonebot.typing import T_State
from nonebot.params import CommandArg

from .config import Config
from .data import CheckInData, Time
from ..points.data import PointsData

import time, random

__plugin_meta__ = PluginMetadata(
    name="check_in",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

check_in = on_command("check_in", aliases={"签到", "qd"})

@check_in.handle()
async def handle_check_in(bot: Bot, event: Event, state: T_State):
    group_id = int(event.group_id)  # type: ignore
    user_id = int(event.get_user_id())
    ckid = CheckInData(user_id, group_id)
    point = PointsData(user_id, group_id)
    t = Time(user_id, group_id)
    if t.check_time():
        last_check_in_time = time.localtime(ckid.get_user_data())
        formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", last_check_in_time)
        await bot.send_group_msg(
            group_id=group_id,
            message=f"你今天已经签到过了哦~ 上次签到时间：{formatted_time}"
        )
        await check_in.finish(f"你今天已经签到过了哦~ 上次签到时间：{formatted_time}", reply_message = True)
    else:
        points_earned = random.randint(1, 10)
        point.update_points(points_earned)
        ckid.update_check_in()
        await check_in.finish(f"签到成功！恭喜获得{points_earned}点基础积分！\n您当前总积分为：{point.get_points():.2f}点！", reply_message = True)