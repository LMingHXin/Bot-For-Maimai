import json, time
from typing import Dict, List, Union
from nonebot.log import logger

class Room(): # 房间类封装，用于创建与管理房间
    def __init__(self, group_id: str, user_id: str): # 调用时，将产生房间标识符room_token，需要传入参数group_id与user_id作为创建房间的依据
        self.group_id = group_id
        self.user_id = user_id
        self.room_token = self.group_id + str(time.time())
        self.room_data :Dict[str, Dict[str, Union[str, List[str], bool, int, str]]]= {}
        """roomdata:
        {
            room_token: 
            {
            "group_id": str,
            "user_ids": List[str],
            "status": bool,
            "ID": int,
            "room_name": str
            }
        }"""
        self.room_id = 1
    
    def __str__(self):
        return self.room_token
        
    def download_room_data(self): # 从本地存储获取room_list，同时更新room_id
        with open("/home/sa/room_data.json", "r") as f:
            self.room_data = json.load(f)
        self.room_id = 1
        self.room_id += len(list(self.room_data.keys()))
        logger.info(f"成功下载房间数据，当前房间总数为{self.room_id-1}，下一个房间ID为{self.room_id}")
                 
    def create_room(self, room_name: str): # 创建房间，同时更新room_id
        for i in self.room_data.keys():
            if self.room_data[i]["group_id"] == self.group_id and self.user_id in self.room_data[i]["user_ids"]: # type: ignore
                logger.warning(f"用户{self.user_id}在群{self.group_id}中已创建房间，无法重复创建")
                return "ERROR"
        self.room_data[self.room_token] = {
            "group_id":self.group_id,
            "user_ids":[self.user_id],
            "status":True,
            "ID":self.room_id,
            "room_name":room_name
        }
        self.room_id += 1
        logger.success(f"成功创建房间，房间TOKEN为{self.room_token}，房间ID为{self.room_id-1}")
        
    def quit_room(self, room_token: str, user_id: str): # 退出房间
        if self.room_data[room_token]["status"] == False:
            logger.warning(f"房间{room_token}已关闭，无法退出")
            return "ROOM_CLOSED"
        self.room_data[room_token]["user_ids"].remove(user_id)  # type: ignore
        if len(self.room_data[room_token]["user_ids"]) == 0:  # type: ignore
            del self.room_data[room_token]
            logger.info(f"房间{room_token}已无玩家，房间已解散")
            return "INVALID_ROOM"
        
    def get_token(self) -> str: # 获取房间token
        return self.room_token
    
    def get_id(self) -> int: # 获取房间ID
        self.download_room_data()
        return len(self.room_data) # type: ignore
        
    def update_room_data(self): # 更新内存数据到本地存储
        with open("/home/sa/room_data.json", "w") as f:
            json.dump(self.room_data, f)
        logger.success(f"成功更新房间数据至本地存储")
    
    def get_room_info(self):
        self.download_room_data()
        return self.room_data