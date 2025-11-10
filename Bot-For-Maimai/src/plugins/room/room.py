import json


class Room():
    def __init__(self, user_id: str, group_id: str): # 初始化房间对象
        self.user_id = user_id
        self.group_id = group_id
        self.room_data = {}
        '''{
            "group_id":{
                "room_name":"", 
                "user_ids": [str],
                "room_id": int
                "room_status": bool
            }
        }'''
        with open("/home/sa/room.json", "r", encoding="utf-8") as f:
            self.room_data = json.load(f)
        
    def create_room(self, room_name: str) -> None: # 创建房间
        id = 0
        try:
            for i in self.room_data:
                if self.room_data[i]["room_id"] > id:
                    id = self.room_data[i]["room_id"]
        except:
            id = 0
        self.room_data[self.group_id] = {
            "room_name": room_name,
            "user_ids": [self.user_id],
            "room_id": id + 1,
            "room_status": True
        }
        with open("/home/sa/room.json", "w", encoding="utf-8") as f:
            json.dump(self.room_data, f, ensure_ascii=False, indent=4)
            
    def join_room(self) -> str: # 加入房间
        if self.group_id in self.room_data:
            if self.user_id not in self.room_data[self.group_id]["user_ids"]:
                self.room_data[self.group_id]["user_ids"].append(self.user_id)
                with open("/home/sa/room.json", "w", encoding="utf-8") as f:
                    json.dump(self.room_data, f, ensure_ascii=False, indent=4)
                return f"成功加入房间 {self.room_data[self.group_id]['room_name']}！\n当前房间成员：{', '.join(self.room_data[self.group_id]['user_ids'])}"
            else:
                return f"你已经在该房间内！"
        else:
            return f"房间不存在！"
        
    def leave_room(self) -> str: # 离开房间
        if self.group_id in self.room_data:
            if self.user_id in self.room_data[self.group_id]["user_ids"]:
                self.room_data[self.group_id]["user_ids"].remove(self.user_id)
                with open("/home/sa/room.json", "w", encoding="utf-8") as f:
                    json.dump(self.room_data, f, ensure_ascii=False, indent=4)
                return f"成功离开房间 {self.room_data[self.group_id]['room_name']}！\n当前房间成员：{', '.join(self.room_data[self.group_id]['user_ids'])}"
            else:
                return f"你不在该房间内！"
        else:
            return f"房间不存在！"
        
    def del_room(self) -> str: # 解散房间，只有房主可以解散
        if self.group_id in self.room_data:
            if self.user_id in self.room_data[self.group_id]["user_ids"] and self.user_id == self.room_data[self.group_id]["user_ids"][0]:
                del self.room_data[self.group_id]
                with open("/home/sa/room.json", "w", encoding="utf-8") as f:
                    json.dump(self.room_data, f, ensure_ascii=False, indent=4)
                return f"成功解散房间！"
            else:
                return f"你不是房主，无法解散房间！"
        else:
            return f"房间不存在！"
        
    def get_room_info(self) -> str: # 获取房间信息
        if self.group_id in self.room_data:
            info = self.room_data[self.group_id]
            return f"房间名称：{info['room_name']}\n房间ID：{info['room_id']}\n房间状态：{'开启' if info['room_status'] else '关闭'}\n当前成员：{', '.join(info['user_ids'])}"
        else:
            return f"房间不存在！"
        
    def get_room_id(self) -> int: # 获取房间ID
        if self.group_id in self.room_data:
            return self.room_data[self.group_id]["room_id"]
        else:
            return 1
        
    def toggle_room_status(self) -> None: # 切换房间状态（开启/关闭）
        if self.group_id in self.room_data:
            self.room_data[self.group_id]["room_status"] = not self.room_data[self.group_id]["room_status"]
            with open("/home/sa/room.json", "w", encoding="utf-8") as f:
                json.dump(self.room_data, f, ensure_ascii=False, indent=4)