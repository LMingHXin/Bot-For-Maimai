from ..libraries import roomdata
from .divide import role, paper

class Main_step:
    def __init__(self, user_id: str, group_id: str):  #STEP0:create room and gather players
        self.room_data = roomdata.RoomData(user_id, group_id)
        self.room_data.create_room(f"三国杀{self.room_data.get_room_id()}")
    
    def __str__(self):
        return f"三国杀房间创建成功！\n房间ID：{self.room_data.get_room_id()}\n请玩家加入房间，等待房主开始游戏！"
    
    def step_1(self):  #STEP1: Confirm players and divide roles
        pass
    
    def step_2(self): #STEP2: select generals
        pass
    
    def step_3(self): #STEP3: game start
        pass
    
    def step_4(self): #STEP4: game end
        pass
        