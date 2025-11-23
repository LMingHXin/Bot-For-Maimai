from nonebot import get_plugin_config, on_command, on_message
from nonebot.plugin import PluginMetadata
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Message, Event, Bot
from nonebot_plugin_alconna.uniseg import message_recall
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

gather = on_command("ktt", priority=5, block=False, aliases={"开三国杀", "开始三国杀"}, rule=to_me())  #开始三国杀
start = on_command("start_ktt", priority=5, block=False, aliases={"开始游戏", "开始ktt"}, rule=to_me())  #开始游戏
join = on_command("join_ktt", priority=5, block=False, aliases={"加入三国杀", "加入ktt"}, rule=to_me())  #加入三国杀
quit = on_command("quit_ktt", priority=5, block=False, aliases={"退出三国杀", "退出ktt"}, rule=to_me())  #退出三国杀
choose_general = on_command("choose_general", priority=5, block=False, aliases={"选择武将"}, rule=to_me())  #选择武将
seek_room = on_command("seek_ktt", priority=5, block=False, aliases={"查找三国杀房间", "查找ktt房间"}, rule=to_me())  #查找三国杀房间

@seek_room.handle()
async def handle_seek(bot: Bot, event: Event, state: T_State, args: Message = CommandArg()):
    uid = event.get_user_id()
    gid = event.group_id # type: ignore
    room_api = stream.Main_step(str(uid), str(gid)).room_api
    room_api.room.download_room_data()
    active_rooms = room_api.seek_group_rooms(str(gid))
    if not active_rooms:
        await seek_room.finish("当前群内暂无三国杀房间~", at_sender=True)
    msg = "当前群内的三国杀房间有：\n"
    for token, data in active_rooms.items():
        status = "进行中" if not data["status"] else "等待中"
        msg += f"房间名称：{data['room_name']}\n房间状态：{status}\n当前玩家数：{len(data['user_ids'])}\n---\n"

@gather.handle()
async def handle_gather(bot: Bot, event: Event, state: T_State, args: Message = CommandArg()):
    uid = event.get_user_id()
    gid = event.group_id # type: ignore
    main_step = stream.Main_step(str(uid), str(gid))
    re = main_step.create()
    if re == "FAILED":
        await gather.finish("房间创建失败，可能是以下两个原因：\n1.您已加入/创建房间，无法创建新的房间\n2.您所在的群内可能有房间正在进行三国杀游戏，请您等待结束后再创建三国杀房间", reply=True)
    main_step.gather()
    state["room_token"] = main_step.room_token
    await bot.send_private_msg(user_id=int(uid), message=f"创建成功~\n房间TOKEN为{main_step.room_token}\n请复制token给群聊以便其他玩家加入~")
    await gather.send(group_id=int(gid), message=f"创建了三国杀房间~\n已经私信通知他力！他将复制TOKEN给大家加入！", at_sender=True)
    
@join.handle()
async def handle_join(bot: Bot, event: Event, state: T_State, args: Message = CommandArg()):
    uid = event.get_user_id()
    gid = event.group_id # type: ignore
    room_token = args.extract_plain_text().strip()
    if not room_token:
        await join.finish("请提供房间TOKEN以加入房间~", at_sender=True)
    room_api = stream.Main_step(str(uid), str(gid)).room_api
    success = room_api.join_room(room_token, str(uid))
    if success:
        id = str(event.message_id)  # type: ignore
        await message_recall(id)
        await join.send(group_id=int(gid), message=f"加入了房间~", at_sender=True)
    else:
        await join.finish("加入房间失败，请检查TOKEN是否正确或您是否已在房间中~\n当然，这个房间可能已经开始游戏了，无法加入新的玩家", at_sender=True)
        
@quit.handle()
async def handle_quit(bot: Bot, event: Event, state: T_State, args: Message = CommandArg()):
    uid = event.get_user_id()
    gid = event.group_id # type: ignore
    room_token = args.extract_plain_text().strip()
    if not room_token:
        await quit.finish("请提供房间TOKEN以退出房间~", at_sender=True)
    room_api = stream.Main_step(str(uid), str(gid)).room_api
    re = room_api.quit_room(room_token, str(uid))
    if re == "ROOM_CLOSED":
        await quit.finish("房间已关闭，无法退出~", at_sender=True)
    id = str(event.message_id)  # type: ignore
    await message_recall(id)
    await quit.send(group_id=int(gid), message=f"玩家{uid}退出了房间~")
    if re == "INVALID_ROOM":
        await quit.send(group_id=int(gid), message=f"房间{room_token}已无玩家，房间已解散~")
        
@start.handle()
async def handle_start(bot: Bot, event: Event, state: T_State, args: Message = CommandArg()):
    uid = event.get_user_id()
    gid = event.group_id # type: ignore
    room_token = args.extract_plain_text().strip()
    if not room_token:
        await start.finish("请提供正确的房间TOKEN以开始游戏~")
    main_step = stream.Main_step(str(uid), str(gid))
    main_step.room_token = room_token
    confirmed = main_step.confirm()
    if not confirmed:
        await start.finish("无法开始游戏~可能是以下三个原因之一\n1. 玩家不足，至少需要3名玩家才能开始游戏\n2. 玩家过多，建议控制在10人以内\n3. 只有房主可以确认开始游戏~", at_sender=True)
    assigned_roles = main_step.divide()
    for user_id, role in assigned_roles.items():
        await bot.send_private_msg(user_id=int(user_id), message=f"游戏开始啦！\n您的身份是：{role}，请牢记您的身份哦~")
        if role == "主公":
            await start.send(group_id=int(gid), message=f"游戏开始啦！\n玩家{user_id}是本局的主公!!")
    await start.finish("角色分配完毕，已经私信通知\n游戏正式开始！请各位玩家开始选择武将")