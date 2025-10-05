from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="temp",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)


import nonebot

bot = nonebot.get_bot("2858178630")
print(bot)
print("temp插件加载成功")
async def temp_send():
    await bot.send_private_msg(user_id=2654625014, message="temp插件加载成功")
print("temp插件发送消息成功")

#这里是临时测试代码
  
