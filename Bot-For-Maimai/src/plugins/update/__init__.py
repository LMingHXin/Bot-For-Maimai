from nonebot import get_plugin_config, on_command
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Message, Event, Bot
from nonebot.plugin import PluginMetadata

from .config import Config

import git

__plugin_meta__ = PluginMetadata(
    name="update",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

update = on_command("update", priority=0, block=True, aliases={"更新"})

class GitRepo():
    def __init__(self, path: str):
        self.repo = git.Repo(path)

    def pull(self):
        origin = self.repo.remotes.origin
        self.repo.git.stash()
        origin.pull()

@update.handle()
async def _(bot: Bot, event: Event, state: T_State):
    usrid = event.get_user_id()
    if str(usrid) != str(config.master_qq):
        await update.finish(Message("只有主人可以使用此命令"))
    msg = str(event.get_message()).strip()
    if msg == "":
        repo = GitRepo(path="/home/sa/Bot-For-Maimai")
        repo.pull()
        await update.finish("更新成功，请重启生效")
    else:
        await update.finish(None)