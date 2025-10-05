from nonebot import get_plugin_config, on_command, on_message
from nonebot.plugin import PluginMetadata
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Message, Event, Bot
from nonebot.rule import to_me
from nonebot.params import CommandArg

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
join_date = on_command("join_date", priority=5, block=False, aliases={"参加约", "jdate"}, rule=to_me())  #参加约！
quit_date = on_command("quit_date", priority=5, block=False, aliases={"退出约", "qdate"}, rule=to_me())  #退出约！
list_date = on_command("list_date", priority=5, block=False, aliases={"约列表", "ldate"}, rule=to_me())  #约列表
date_help = on_command("date_help", priority=4, block=False, aliases={"约帮助", "dhelp"}, rule=to_me())  #教你约！
date_setting = on_command("date_setting", priority=4, block=False, aliases={"约设置", "dsetting"}, rule=to_me())  #神！权！
my_date = on_command("my_date", priority=5, block=False, aliases={"我的约会", "mdate", "md"}, rule=to_me())  #我的约会


@date.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State, args: Message = CommandArg()): # type: ignore
    user_id = event.get_user_id()
    group_id = event.group_id # type: ignore
    if group_id not in config.date_group: # type: ignore
        await date.finish("笨蛋~这个群不能约会哦~")
    content = args.extract_plain_text()
    if not content:
        await date.finish("笨蛋~谁知道你要月什么喵~")
    val = maindate.create_date(user_id, group_id, content) # type: ignore
    if val[0]:
        state["date_id"] = val
        state["context"] = content
        await date.send(f"已经有相同主题的约会喵~\n主题：{content}\n约会ID：{val[1:]}\n发送 'yes' 确认参加，发送 'no' 取消, 当然，你也可以发个 'new' 创建新的约会~") # type: ignore
    if not val[0]:
        await date.finish(f"月！主题：{content}\n约会ID：{maindate.date_id}\n发送 'join_date {maindate.date_id}' 就可以参加约会了哦~") # type: ignore
    
    
@date.got("confirm", prompt="请确认是否加入已经存在的约会喵~")
async def handle_confirm(bot: Bot, event: Event, state: T_State): # type: ignore
    user_id = event.get_user_id()
    group_id = event.group_id # type: ignore
    msg = str(event.get_message()).split(" ")
    print(msg)
    if msg[0] in {"yes", "y", "是", "对", "好", "参加", "加入"}:
        try:
            date_id = int(msg[1])
        except:
            await date.reject("笨蛋~没有约会ID喵~")
        date_id = msg[1]
        if date_id in state.get("date_id"): # type: ignore
            await date.finish("笨蛋~没有约会ID喵~")
        if maindate.join_date(user_id, date_id, group_id): # type: ignore
            await date.finish(f"成功加入ID为{date_id}的约会了喵~祝你玩的愉快喵~")
        else:
            await date.finish(f"无法参加约会ID {date_id}，可能已参加或ID无效")
    if msg[0] in {"new", "创建新的", "创建新约会", "new date", "n"}:
        content = state.get("context")
        print(content)
        if content == "":
            await date.reject("笨蛋~谁知道你要月什么喵~")
        maindate.create_repeat_date(user_id, event.group_id, content) # type: ignore
        await date.finish(f"行吧~居然不和别人一块约会~真是孤高自傲呢~\n主题：{content}\n约会ID：{maindate.date_id}\n发送 'join_date {maindate.date_id}' 就可以参加约会了哦~") # type: ignore
    if msg[0] in {"no", "n", "不是", "不对", "算了", "取消"}:
        await date.finish("好吧~不参加也行喵~")
    else:
        await date.reject("请输入有效的选项喵~\n发送 'yes+id' 确认参加，发送 'no' 取消, 当然，你也可以发个 'new' 创建新的约会~")
    
    
@join_date.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State, args: Message = CommandArg()): # type: ignore
    user_id = event.get_user_id()
    msg = args.extract_plain_text().strip()
    group_id = event.group_id # type: ignore
    print(msg)
    if not msg.isdigit():
        await join_date.finish("请输入有效的约会ID")
    date_id = int(msg[0])
    if maindate.join_date(user_id, date_id, group_id): # type: ignore
        await join_date.finish(f"成功参加约会ID {date_id}")
    else:
        await join_date.finish(f"无法参加约会ID {date_id}，可能已参加或ID无效")
        
        
@quit_date.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State, args: Message = CommandArg()): # type: ignore
    group_id = event.group_id # type: ignore
    user_id = event.get_user_id()
    msg = args.extract_plain_text().strip() # type: ignore
    if not msg.isdigit():
        await quit_date.finish("请输入有效的约会ID, 如 'quit_date 1'")
    date_id = int(msg)
    if maindate.quit_date(user_id, date_id, group_id): # type: ignore
        await quit_date.finish(f"成功退出约会ID {date_id}")
    else:
        await quit_date.finish(f"无法退出约会ID {date_id}，可能未参加或ID无效")
        
        
@list_date.handle()
async def handle_first_receive(bot: Bot, event:Event, state: T_State, args: Message = CommandArg()): # type: ignore
    group_id = event.group_id # type: ignore
    if group_id not in config.date_group: # type: ignore
        await list_date.finish("笨蛋~这个群不能约会哦~")
    Rmaindate = maindate.get_date_list(group_id) # type: ignore
    if not Rmaindate:
        await list_date.finish("现在群里没有约会喵~快来发起一个吧~")
    msg = "当前群约会列表：\n"
    for date in Rmaindate: # type: ignore
        msg += f"ID: {date['id']}, 主题: {date['主题']}, 参与人员: {date.get('参与人员', [])}\n"
    await list_date.finish(msg)
    
    
@my_date.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State, args: Message = CommandArg()): # type: ignore
    user_id = event.get_user_id()
    Rmaindate = maindate.get_user_dates(user_id) # type: ignore
    if not Rmaindate:
        await my_date.finish("你还没有参加任何约会喵~快去参加一个吧~")
    msg = "你参加的约会列表：\n"
    for date in Rmaindate: # type: ignore
        msg += f"ID: {date['id']}, 主题: {date['主题']}, 参与人员: {date.get('参与人员', [])}, 群聊: {date.get('群聊', [])}\n"
    await my_date.finish(msg)
    
    
@date_help.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State, args: Message = CommandArg()): # type: ignore
    msg = (
        "约会功能使用说明（注意！注意！记得@我哦）：\n"
        "1. 发起约会（这个不用@我哦）：发送 '月/约/🈷 主题' 创建一个新约会。\n"
        "2. 参加约会：发送 'join_date/jdate 约会ID' 参加指定ID的约会。\n"
        "3. 退出约会：发送 'quit_date/qdate 约会ID' 退出指定ID的约会。\n"
        "4. 查看约会列表：发送 'list_date/ldate' 查看当前群的所有约会。\n"
        "5. 查看我的约会：发送 'my_date/mdate/md' 查看你参加的所有约会。\n"
        "6. 管理员设置：发送 'date_setting/dsetting' 进行约会功能的管理设置（仅限管理员）。\n"
    )
    await date_help.finish(msg)
    
    
@date_setting.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State, args: Message = CommandArg()): 
    user_id = int(event.get_user_id())
    if user_id not in config.admin: # type: ignore
        await date_setting.finish("杂鱼~你不是管理员哦~")
    msg = args.extract_plain_text().strip()
    print(msg)
    if msg == "查看设置":
        await date_setting.finish(f"当前约会功能启用群：{config.date_group}\n当前管理员群：{config.admin_group}\n当前管理员：{config.admin}") # type: ignore
    if msg == "":
        await date_setting.finish("请输入设置命令，如 '删除约会 约会ID'")
    parts = msg.split()
    if len(parts) != 2 or parts[0] != "删除约会":
        await date_setting.finish("格式错误，请使用 '删除约会 约会ID'")
    if not parts[1].isdigit():
        await date_setting.finish("格式错误，请使用 '删除约会 约会ID'")
    del_date_id = int(parts[1])
    if maindate.delete_date(del_date_id): # type: ignore
        await date_setting.finish(f"成功删除约会ID：{del_date_id}")
    else:
        await date_setting.finish(f"无法删除约会ID：{del_date_id}，可能ID无效")
    await date_setting.finish("未找到该约会ID")
    