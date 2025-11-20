from ...room import Room
from nonebot.log import logger
from typing import Dict, Any
import json

class Room_api(): # 房间数据接口封装
    def __init__(self, group_id: str, user_id: str):
        self.room = Room(group_id, user_id)
        
    def __str__(self) -> str:
        return self.room.room_token
        
    def create_room(self,room_name): # 创建房间
        self.room.download_room_data()
        re = self.room.create_room(room_name)
        if re == "ERROR":
            return "FAILED"
        self.room.update_room_data()
        
    def join_room(self, room_token: str, user_id: str) -> bool: # 加入房间
        self.room.download_room_data()
        if room_token in self.room.room_data.keys() and self.room.room_data[room_token]["status"] == True:  # type: ignore
            if user_id not in self.room.room_data[room_token]["user_ids"]: # type: ignore
                self.room.room_data[room_token]["user_ids"].append(user_id) # type: ignore
                self.room.update_room_data()
                return True
            else:
                return False
        else:
            return False
        
    def lock_room(self, room_token: str): # 锁定房间
        self.room.download_room_data()
        self.room.room_data[room_token]["status"] = False  # type: ignore
        self.room.update_room_data()
    
    def quit_room(self, room_token: str, user_id: str): # 退出房间
        self.room.download_room_data()
        re = self.room.quit_room(room_token, user_id)
        self.room.update_room_data()
        return re

class Room_data(): # 房间数据处理封装, 用于对局内获取房间各项数据
    def __init__(self, room_token: str):
        self.room_token = room_token
        self.room_data = {}
        self.load_room_data()
        
    def load_room_data(self): # 加载房间数据
        all_room_data: Dict[str, Any] = {}
        with open("/home/sa/room_data.json", "r") as f:
            all_room_data = json.load(f)
        if self.room_token in all_room_data.keys():
            self.room_data = all_room_data[self.room_token]
        else:
            logger.error(f"未能找到TOKEN为{self.room_token}的房间数据")
            return
        self.user_ids = self.room_data.get("user_ids", [])
        self.group_id = self.room_data.get("group_id", "")
        self.status = self.room_data.get("status", False)
        self.ID = self.room_data.get("ID", -1)
        self.room_name = self.room_data.get("room_name", "")
        logger.info(f"成功获取TOKEN为{self.room_token}的房间数据: {self.room_data}")
        self.room_step = 0  # 房间当前步骤，初始为0
        logger.info(f"房间{self.room_token}当前步骤成功设定为{self.room_step}")
        