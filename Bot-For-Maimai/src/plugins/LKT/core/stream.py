from ..libraries import roomdata, constantdata
from .divide import role, paper
from nonebot.log import logger

class Main_step:
    def __init__(self, user_id: str, group_id: str):  
        self.user_id = user_id
        self.group_id = group_id
        self.room_api = roomdata.Room_api(group_id, user_id)
        
    def create(self):  #STEP0-1:create room
        self.room_token = self.room_api.room.get_token()
        try:
            self.room_id = self.room_api.room.get_id()
        except Exception as e:
            logger.error(f"获取房间ID失败：{e}")
            self.room_id = 1
        self.room_name = f"三国杀房间{self.room_id}"
        re = self.room_api.create_room(self.room_name)
        if re == "FAILED":
            logger.error("房间创建失败")
            return "FAILED"
        
    def quitr(self):  #QUIT: quit room
        re = self.room_api.quit_room(self.room_token, self.user_id)
        return re
        
    def gather(self):  #STEP0-2:gather players
        self.room_api.join_room(self.room_token, self.user_id)
    
    def confirm(self):  #STEP1-1: Confirm players
        room = roomdata.Room_data(self.room_token)
        self.user_ids = room.user_ids
        if len(self.user_ids) < 2:
            logger.error("房间玩家不足，无法开始游戏")
            return False  # Not enough players to start the game
        room.room_step = 1  # Update room step to 1
        self.room = room
        logger.info(f"房间{self.room_token}玩家确认完毕，当前玩家列表：{self.user_ids}")
        return True  # Enough players to start the game
    
    def divide(self): #STEP1-2: Divide roles and load cards
        self.divide_role = role(self.user_ids)
        self.assigned_roles = self.divide_role.assign_roles()
        self.cards = constantdata.cards.copy()
        self.room.room_step = 2  # Update room step to 2
        return self.assigned_roles
        
    
    def step_2(self): #STEP2: select generals
        pass
    
    def step_3(self): #STEP3: game start
        pass
    
    def step_4(self): #STEP4: game end
        pass
    
#TODO： 游戏流程管理（Main_step）