from ...room import Room
import json

class RoomData(): # 总房间操作，将 room.py 中的 Room 类进行封装
    def __init__(self, user_id: str, group_id: str):
        self.room = Room(user_id, group_id)
        
    def create_room(self, room_name: str) -> None:
        self.room.create_room(room_name)
        
    def join_room(self) -> str:
        return self.room.join_room()
    
    def leave_room(self) -> str:
        return self.room.leave_room()
    
    def change_room_status(self) -> None:
        self.room.toggle_room_status()
        
    def get_room_id(self) -> int:
        return self.room.get_room_id()
        
class ControllerRoomData():# 针对局内的房间操作
    def __init__(self, group_id: str, room_id: int): # 根据群号和房间号初始化房间数据
        self.group_id = group_id
        self.room_id = room_id
        with open("/home/sa/room.json", "r", encoding="utf-8") as f:
            room_data = json.load(f)
        room_data_list = room_data.get(group_id, None)
        self.room_data = room_data_list if room_data_list and room_data_list["room_id"] == room_id else None
        if not self.room_data:
            raise ValueError("Room not found")
        self.room_controller = self.room_data["user_ids"][0]
        self.room_step = 0
        self.room_players = self.room_data["user_ids"]
        
    def set_room_step(self, step: int) -> None: # 根据房间当前step，将房间上锁，即禁止其它玩家加入
        self.room_step = step
        if step == 1:
            roomdata = RoomData(self.room_controller, self.group_id)
            roomdata.change_room_status()
    
    def get_room_step(self) -> int: # 获取当前房间step
        return self.room_step
        
    def update_room(self) -> None: # 更新房间数据到文件
        with open("/home/sa/room.json", "r", encoding="utf-8") as f:
            room_data = json.load(f)
        room_data[self.group_id] = self.room_data
        with open("/home/sa/room.json", "w", encoding="utf-8") as f:
            json.dump(room_data, f, ensure_ascii=False, indent=4)
            
    def del_room(self, user_id: str) -> str: # 解散房间，只有房主可以解散
        if user_id == self.room_controller:
            roomdata = RoomData(self.room_controller, self.group_id)
            roomdata.leave_room()
            with open("/home/sa/room.json", "r", encoding="utf-8") as f:
                room_data = json.load(f)
            if self.group_id in room_data:
                del room_data[self.group_id]
            with open("/home/sa/room.json", "w", encoding="utf-8") as f:
                json.dump(room_data, f, ensure_ascii=False, indent=4)
            return f"房间已解散！"
        else:
            return f"只有房主才能解散房间！"
    
    def Isplayer_in_room(self, user_id: str): #判断玩家是否在房间内，影响该玩家是否能够创建房间或加入其它房间
        with open("/home/sa/room.json", "r", encoding="utf-8") as f:
            room_data = json.load(f)
        room_data_list = room_data.get(self.group_id, None)
        if room_data_list and room_data_list["room_id"] == self.room_id:
            return user_id in room_data_list["user_ids"]
    
        
        
    