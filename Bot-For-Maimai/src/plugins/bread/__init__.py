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
bread_help = on_command("面包帮助", priority=5, aliases={"breadhelp"})

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
    
@bread_help.handle()
async def handle_bread_help(bot: Bot, event: Event, state: T_State):
    help_msg = """面包系统帮助：
1. 领取面包/买面包：每天可以领取无限次面包，面包可以用来提升等级，保护自己不被偷面包。
2. 偷面包：可以尝试从其他用户那里偷取面包，但有被保护的用户无法偷取面包。
3. 吃面包：可以吃掉一定数量的面包来 提升等级，但有一定几率吃坏肚子导致面包数量减少。
4. 面包状态：查看自己当前的面包数量、保护状态和等级。
5. 切换面包保护：开启或关闭面包保护，开启后其他用户无法偷取你的面包。
管理员指令（仅限管理员使用）：
1. 修改面包 <用户ID> <面包数量>：修改指定用户的面包数量。
2. 修改等级 <用户ID> <等级>：修改指定用户的面包等级。
3. 修改状态 <用户ID> <开启/关闭>：修改指定  用户的面包保护状态。
"""    
    await bread_help.finish(help_msg)