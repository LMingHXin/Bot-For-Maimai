from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
import time, nonebot

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
import asyncio

t = time.gmtime()
ts = time.strftime("%M", t)

async def main():
    if ts == "22":
        await temp_send()
        print("temp插件发送消息成功")

asyncio.run(main())


  
