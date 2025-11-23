from ..libraries import constantdata
from nonebot.log import logger
import random

class role: #角色分配
    def __init__(self, user_ids: list[str]):
        self.user_ids = user_ids
        self.assigned_roles = {}
    
    def assign_roles(self):
        idlen = len(self.user_ids)
        if idlen == 2 : # 特殊情况：双人局，测试用
            master_num = 1
            loyal_num = 0
            traitor_num = 0
            rebel_num = 1
            roles_list = (["主公"] * master_num +
                        ["反贼"] * rebel_num +
                        ["忠臣"] * loyal_num +
                        ["内奸"] * traitor_num)
            random.shuffle(roles_list)
            self.assigned_roles = dict(zip(self.user_ids, roles_list))
            return self.assigned_roles
        
        if idlen < 2:
            logger.error("玩家数量不足，无法分配角色")
        
        # 角色分配
        master_num = 1
        loyal_num = int(idlen // 3.5)
        traitor_num = idlen // 4
        rebel_num = idlen - master_num - loyal_num - traitor_num
        
        if idlen == 3: # 特殊情况：三人局，无忠臣
            master_num = 1
            loyal_num = 0
            traitor_num = 1
            rebel_num = 1
        
        roles_list = (["主公"] * master_num +
                      ["反贼"] * rebel_num +
                        ["忠臣"] * loyal_num +
                        ["内奸"] * traitor_num)
        
        random.shuffle(roles_list)
        self.assigned_roles = dict(zip(self.user_ids, roles_list))
        logger.info(f"角色分配完成：{self.assigned_roles}")
        
        return self.assigned_roles    

class general: #武将选择
    pass

class paper: #牌堆管理（发牌）
    pass