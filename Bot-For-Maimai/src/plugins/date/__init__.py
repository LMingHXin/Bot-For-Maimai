from nonebot import get_plugin_config, on_command, on_message
from nonebot.plugin import PluginMetadata
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Message, Event, Bot

from .config import Config
from .main import maindate

__plugin_meta__ = PluginMetadata(
    name="date",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

#注册事件响应器
date = on_command("date", priority=5, block=False, aliases={"约", "月"})  #发起约！
join_date = on_command("join_date", priority=5, block=False, aliases={"参加约", "jdate"})  #参加约！
quit_date = on_command("quit_date", priority=5, block=False, aliases={"退出约", "qdate"})  #退出约！
list_date = on_command("list_date", priority=5, block=False, aliases={"约列表", "ldate"})  #约列表
date_help = on_command("date_help", priority=4, block=True, aliases={"约帮助", "dhelp"})  #教你约！
date_setting = on_command("date_setting", priority=3, block=False, aliases={"约设置", "dsetting"})  #神！权！

@date.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    user_id = event.get_user_id()
    group_id = event.group_id
    if group_id not in config.date_group:
        await date.finish("本群未启用约会功能")
    content = str(event.get_message())[1: ]
    maindate.create_date(user_id, group_id, content)
    await date.finish(f"约会已创建，主题：{content}\n约会ID：{maindate.date_id}\n发送 'join_date {maindate.date_id}' 参加约会")
    
    
@join_date.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    user_id = event.get_user_id()
    msg = str(event.get_message()).split(' ')[1].strip()
    print(msg[0])
    if not msg[0].isdigit():
        await join_date.finish("请输入有效的约会ID")
    date_id = int(msg[0])
    if maindate.join_date(user_id, date_id):
        await join_date.finish(f"成功参加约会ID {date_id}")
    else:
        await join_date.finish(f"无法参加约会ID {date_id}，可能已参加或ID无效")
        
        
@quit_date.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    user_id = event.get_user_id()
    msg = str(event.get_message()).strip()
    if not msg.isdigit():
        await quit_date.finish("请输入有效的约会ID")
    date_id = int(msg)
    if maindate.quit_date(user_id, date_id):
        await quit_date.finish(f"成功退出约会ID {date_id}")
    else:
        await quit_date.finish(f"无法退出约会ID {date_id}，可能未参加或ID无效")
        
        
@list_date.handle()
async def handle_first_receive(bot: Bot, event:Event, state: T_State):
    group_id = event.group_id
    if group_id not in config.date_group:
        await list_date.finish("本群未启用约会功能")
    Rmaindate = maindate.date_list
    if not Rmaindate:
        await list_date.finish("当前群暂无约会")
    msg = "当前群约会列表：\n"
    for date in Rmaindate:
        msg += f"ID: {date['id']}, 主题: {date['主题']}, 参与人员: {date.get('参与人员', [])}\n"
    await list_date.finish(msg)
    
    
@date_help.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    msg = (
        "约会功能使用说明：\n"
        "1. 发起约会：发送 'date 主题' 创建一个新约会。\n"
        "2. 参加约会：发送 'join_date 约会ID' 参加指定ID的约会。\n"
        "3. 退出约会：发送 'quit_date 约会ID' 退出指定ID的约会。\n"
        "4. 查看约会列表：发送 'list_date' 查看当前群的所有约会。\n"
        "5. 管理员设置：发送 'date_setting' 进行约会功能的管理设置（仅限管理员）。\n"
    )
    await date_help.finish(msg)
    
    
@date_setting.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State): 
    user_id = int(event.get_user_id())
    group_id = event.group_id
    if user_id not in config.admin:
        await date_setting.finish("你不是管理员，无权使用此功能")
    msg = str(event.get_message()).strip()
    if msg == "查看设置":
        await date_setting.finish(f"当前约会功能启用群：{config.date_group}\n当前管理员群：{config.admin_group}\n当前管理员：{config.admin}")
    if msg == "":
        await date_setting.finish("请输入设置命令，如 '删除约会 约会ID'")
    if msg.startswith("删除约会"):
        parts = msg.split()
        if len(parts) != 2 or not parts[1].isdigit():
            await date_setting.finish("格式错误，请使用 '删除约会 约会ID'")
        del_date_id = int(parts[1])
        if maindate.delete_date(del_date_id):
            await date_setting.finish(f"成功删除约会ID：{del_date_id}")
        else:
            await date_setting.finish(f"无法删除约会ID：{del_date_id}，可能ID无效")
        await date_setting.finish("未找到该约会ID")
    