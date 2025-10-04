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
date = on_command("🈷", priority=5, block=False, aliases={"约", "月"})  #发起约！
join_date = on_command("join_date", priority=5, block=False, aliases={"参加约", "jdate"})  #参加约！
quit_date = on_command("quit_date", priority=5, block=False, aliases={"退出约", "qdate"})  #退出约！
list_date = on_command("list_date", priority=5, block=False, aliases={"约列表", "ldate"})  #约列表
date_help = on_command("date_help", priority=4, block=True, aliases={"约帮助", "dhelp"})  #教你约！
date_setting = on_command("date_setting", priority=3, block=False, aliases={"约设置", "dsetting"})  #神！权！

@date.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State): # type: ignore
    user_id = event.get_user_id()
    group_id = event.group_id # type: ignore
    if group_id not in config.date_group: # type: ignore
        await date.finish("笨蛋~这个群不能约会哦~")
    content = str(event.get_message())[1: ]
    if not content:
        await date.finish("笨蛋~谁知道你要月什么喵~")
    val = maindate.create_date(user_id, group_id, content) # type: ignore
    if val != "success":
        state["date_id"] = int(val)
        await date.send(f"已经有相同主题的约会喵~\n主题：{content}\n约会ID：{val}\n发送 'yes' 确认参加，发送 'no' 取消") # type: ignore
    if val == "success":
        await date.finish(f"月！主题：{content}\n约会ID：{maindate.date_id}\n发送 'join_date {maindate.date_id}' 就可以参加约会了哦~") # type: ignore
    
@date.got("confirm", prompt="请确认是否加入已经存在的约会喵~")
async def handle_confirm(bot: Bot, event: Event, state: T_State): # type: ignore
    user_id = event.get_user_id()
    msg = str(event.get_message()).strip().lower()
    if msg in {"yes", "y", "是", "对", "好", "参加", "加入"}:
        date_id = state.get("date_id")
        if not date_id:
            await date.finish("笨蛋~没有约会ID喵~")
        if maindate.join_date(user_id, date_id): # type: ignore
            await date.finish(f"成功加入ID为{date_id}的约会了喵~祝你玩的愉快喵~")
        else:
            await date.finish(f"无法参加约会ID {date_id}，可能已参加或ID无效")
    else:
        await date.finish("好吧~不参加也行喵~")
    
    
@join_date.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State): # type: ignore
    user_id = event.get_user_id()
    msg = str(event.get_message()).split(' ')[1].strip()
    print(msg)
    if not msg.isdigit():
        await join_date.finish("请输入有效的约会ID")
    date_id = int(msg[0])
    if maindate.join_date(user_id, date_id): # type: ignore
        await join_date.finish(f"成功参加约会ID {date_id}")
    else:
        await join_date.finish(f"无法参加约会ID {date_id}，可能已参加或ID无效")
        
        
@quit_date.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State): # type: ignore
    user_id = event.get_user_id()
    msg = str(event.get_message()).split(" ")[1].strip() # type: ignore
    if not msg.isdigit():
        await quit_date.finish("请输入有效的约会ID, 如 'quit_date 1'")
    date_id = int(msg)
    if maindate.quit_date(user_id, date_id): # type: ignore
        await quit_date.finish(f"成功退出约会ID {date_id}")
    else:
        await quit_date.finish(f"无法退出约会ID {date_id}，可能未参加或ID无效")
        
        
@list_date.handle()
async def handle_first_receive(bot: Bot, event:Event, state: T_State): # type: ignore
    group_id = event.group_id # type: ignore
    if group_id not in config.date_group: # type: ignore
        await list_date.finish("本群未启用约会功能")
    Rmaindate = maindate.get_date_list(group_id) # type: ignore
    if not Rmaindate:
        await list_date.finish("当前群暂无约会")
    msg = "当前群约会列表：\n"
    for date in Rmaindate: # type: ignore
        msg += f"ID: {date['id']}, 主题: {date['主题']}, 参与人员: {date.get('参与人员', [])}\n"
    await list_date.finish(msg)
    
    
@date_help.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State): # type: ignore
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
    group_id = event.group_id # type: ignore
    if user_id not in config.admin: # type: ignore
        await date_setting.finish("你不是管理员，无权使用此功能")
    msg = str(event.get_message()).strip()
    if msg == "查看设置":
        await date_setting.finish(f"当前约会功能启用群：{config.date_group}\n当前管理员群：{config.admin_group}\n当前管理员：{config.admin}") # type: ignore
    if msg == "":
        await date_setting.finish("请输入设置命令，如 '删除约会 约会ID'")
    if msg.startswith("删除约会"):
        parts = msg.split()
        if len(parts) != 2 or not parts[1].isdigit():
            await date_setting.finish("格式错误，请使用 '删除约会 约会ID'")
        del_date_id = int(parts[1])
        if maindate.delete_date(del_date_id): # type: ignore
            await date_setting.finish(f"成功删除约会ID：{del_date_id}")
        else:
            await date_setting.finish(f"无法删除约会ID：{del_date_id}，可能ID无效")
        await date_setting.finish("未找到该约会ID")
    