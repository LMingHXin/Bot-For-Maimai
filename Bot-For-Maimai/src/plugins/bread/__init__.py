from nonebot import get_plugin_config, on_command, on_message
from nonebot.plugin import PluginMetadata
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Message, Event, Bot
from nonebot.rule import to_me
from nonebot.params import CommandArg

from .config import Config
from .data import Data
from .main import bread, status, admin

__plugin_meta__ = PluginMetadata(
    name="bread",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

# 注册事件响应器
get_bread = on_command("领取面包", priority=5, aliases={"买面包", "gbread"})
steal_bread = on_command("偷面包", priority=5, aliases={"sbread"})
check_status = on_command("面包状态", priority=5, aliases={"bstatus"})
toggle_protection = on_command("切换面包保护", priority=5, aliases={"switchbread"})
eat_bread = on_command("吃面包", priority=5, aliases={"ebread"})
bread_admin_fix_bread = on_command("修改面包", priority=5, rule=to_me(), aliases={"breadadmin"})
bread_admin_fix_level = on_command("修改等级", priority=5, rule=to_me(), aliases={"leveladmin"})
bread_admin_fix_status = on_command("修改状态", priority=5, rule=to_me(), aliases={"statusadmin"})

@get_bread.handle()
async def handle_get_bread(bot: Bot, event: Event, state: T_State):
    user_id = int(event.get_user_id())
    group_id = str(event.group_id) # type: ignore
    bread_instance = bread(user_id, group_id)
    msg = bread_instance.get_bread(user_id, group_id)
    await get_bread.finish(msg)
    
    
@steal_bread.handle()
async def handle_steal_bread(bot: Bot, event: Event, state: T_State):
    user_id = int(event.get_user_id())
    group_id = str(event.group_id) # type: ignore
    bread_instance = bread(user_id, group_id)
    msg = bread_instance.steal_bread(user_id, group_id)
    await steal_bread.finish(msg)
    

@eat_bread.handle()
async def handle_eat_bread(bot: Bot, event: Event, state: T_State):
    user_id = int(event.get_user_id())
    group_id = str(event.group_id) # type: ignore
    bread_instance = bread(user_id, group_id)
    msg = bread_instance.eat_bread(user_id, group_id)
    await eat_bread.finish(msg)
    
@check_status.handle()
async def handle_check_status(bot: Bot, event: Event, state: T_State):
    user_id = int(event.get_user_id())
    group_id = str(event.group_id) # type: ignore
    status_instance = status(user_id, group_id)
    msg = status_instance.show_status()
    await check_status.finish(msg)
    
@toggle_protection.handle()
async def handle_toggle_protection(bot: Bot, event: Event, state: T_State):
    user_id = int(event.get_user_id())
    group_id = str(event.group_id) # type: ignore
    status_instance = status(user_id, group_id)
    msg = status_instance.toggle_protection(user_id, group_id)
    await toggle_protection.finish(msg)
    
@bread_admin_fix_bread.handle()
async def handle_bread_admin_fix_bread(bot: Bot, event: Event, state: T_State, cmd_arg: Message = CommandArg()):
    if int(event.get_user_id()) not in config.Admin_user: # type: ignore
        await bread_admin_fix_bread.finish("你没有权限使用这个指令喵！")
    user_id = int(event.get_user_id())
    content = cmd_arg.extract_plain_text().split(" ")
    group_id = str(event.group_id) # type: ignore
    admin_instance = admin(user_id, group_id)
    try:
        msg = admin_instance.fix_count_of_bread(int(content[0]), group_id, int(content[1]))
    except:
        msg = "指令格式错误喵！请使用：修改面包 <用户ID> <面包数量>"
    await bread_admin_fix_bread.finish(msg)
    
@bread_admin_fix_level.handle()
async def handle_bread_admin_fix_level(bot: Bot, event: Event, state: T_State, cmd_arg: Message = CommandArg()):
    if int(event.get_user_id()) not in config.Admin_user: # type: ignore
        await bread_admin_fix_level.finish("你没有权限使用这个指令喵！")
    user_id = int(event.get_user_id())
    content = cmd_arg.extract_plain_text().split(" ")
    group_id = str(event.group_id) # type: ignore
    admin_instance = admin(user_id, group_id)
    try:
        msg = admin_instance.fix_level(int(content[0]), group_id, int(content[1]))
    except:
        msg = "指令格式错误喵！请使用：修改等级 <用户ID> <等级>"
    await bread_admin_fix_level.finish(msg)

@bread_admin_fix_status.handle()
async def handle_bread_admin_fix_status(bot: Bot, event: Event, state: T_State, cmd_arg: Message = CommandArg()):
    if int(event.get_user_id()) not in config.Admin_user: # type: ignore
        await bread_admin_fix_status.finish("你没有权限使用这个指令喵！")
    user_id = int(event.get_user_id())
    content = cmd_arg.extract_plain_text().split(" ")
    group_id = str(event.group_id) # type: ignore
    admin_instance = admin(user_id, group_id)
    try:
        new_status = True if content[1] == "开启" else False
        msg = admin_instance.fix_protection(int(content[0]), group_id, new_status)
    except:
        msg = "指令格式错误喵！请使用：修改状态 <用户ID> <开启/关闭>"
    await bread_admin_fix_status.finish(msg)