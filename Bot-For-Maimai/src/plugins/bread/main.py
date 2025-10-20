from .data import Data
import random, math
MAX_LEVEL = 20

class base():
    def __init__(self, user_id: int, group_id: str):
        self.user_data = {}  # type: ignore
        if Data.get_user_data(user_id, group_id):
            self.count_of_bread = Data.count_of_bread
            self.Is_bread_protected = Data.Is_bread_protected
            self.level = Data.level
        else:
            self.count_of_bread = 0
            self.Is_bread_protected = False
            self.level = 1
            self.bind_group = str(group_id)
            Data.update_user_data(
                self.count_of_bread,
                self.Is_bread_protected,
                self.level,
                user_id,
                group_id,
            )
        self.target_bread = None
    
    def update_data(self, user_id: int, group_id: str) -> None:
        Data.update_user_data(
            self.count_of_bread,
            self.Is_bread_protected,
            self.level, # type: ignore
            user_id,
            group_id,
        )
        

class bread(base):
    def __init__(self, user_id: int, group_id: str):
        super().__init__(user_id, group_id)
        
    
    def get_bread(self, user_id: int, group_id: str) -> str: # get bread function
        dbread : int
        if self.level >= 10:
            dbread = random.randint(-5, 10)
            if dbread < 0:
                self.count_of_bread += dbread
                if self.count_of_bread < 0:
                    self.count_of_bread = 0
                    base.update_data(self, user_id, group_id)
                    return f"买到坏面包了喵！\n 面包数量减少了{dbread} 个喵！\n 当前面包数量：{self.count_of_bread} 个喵！\n不想让你负债喵，人家帮你归零了喵~"
                else:
                    base.update_data(self, user_id, group_id)
                    return f"买到坏面包了喵！\n 面包数量减少了{dbread} 个喵！\n 当前面包数量：{self.count_of_bread} 个喵！"
            else:
                self.count_of_bread += dbread
                base.update_data(self, user_id, group_id)
                return f"成功购买了喵！\n 面包数量增加了{dbread} 个喵！\n 当前面包数量：{self.count_of_bread} 个喵！"
        if self.level >= 5:
            dbread = random.randint(-2, 5)
            if dbread < 0:
                self.count_of_bread += dbread
                if self.count_of_bread < 0:
                    self.count_of_bread = 0
                    base.update_data(self, user_id, group_id)
                    return f"买到坏面包了喵！\n 面包数量减少了{dbread} 个喵！\n 当前面包数量：{self.count_of_bread} 个喵！\n不想让你负债喵，人家帮你归零了喵~"
                else:
                    base.update_data(self, user_id, group_id)
                    return f"买到坏面包了喵！\n 面包数量减少了{dbread} 个喵！\n 当前面包数量：{self.count_of_bread} 个喵！"
            else:
                self.count_of_bread += dbread
                base.update_data(self, user_id, group_id)
                return f"成功购买了喵！\n 面包数量增加了{dbread} 个喵！\n 当前面包数量：{self.count_of_bread} 个喵！"
        else:
            dbread = random.randint(1, 3)
            self.count_of_bread += dbread
            base.update_data(self, user_id, group_id)
            return f"成功购买了喵！\n 面包数量增加了{dbread} 个喵！\n 当前面包数量：{self.count_of_bread} 个喵！"

        
    def steal_core(self, user_id: int, group_id: str, sbread: int, target_id: int) -> None: # steal bread core function
        self.target_bread.count_of_bread -= sbread
        self.target_bread.update_data(target_id, group_id)
        self.count_of_bread += sbread
        self.update_data(user_id, group_id)
    def steal_bread(self, user_id: int, group_id: str) -> str: # steal bread function
        usr_list = Data.get_user_list(str(group_id))
        if len(usr_list) <= 1:
            return "当前群组内面包用户数量不足，无法偷取面包喵！"
        while True:
            target_id = random.choice(usr_list)
            if target_id != str(user_id) and not self.target_bread.Is_bread_protected and self.target_bread.count_of_bread > 0:
                break
        self.target_bread = base(int(target_id), str(group_id))
        if self.Is_bread_protected:
            return "你开启了面包保护喵，偷取失败喵！"
        if self.level >= 10:
            sbread = random.randint(-10, self.target_bread.count_of_bread)
            self.steal_core(user_id, group_id, sbread, int(target_id))
            if sbread < 0:
                if self.count_of_bread < 0:
                    self.count_of_bread = 0
                    self.update_data(user_id, group_id)
                    return f"被防卫了喵！\n 用户{target_id}抢了你{sbread}个面包喵！\n 当前面包数量：{self.count_of_bread} 个喵！\n不想让你负债喵，人家帮你归零了喵~"
                return f"被防卫了喵！\n 用户{target_id}抢了你{sbread}个面包喵！\n 当前面包数量：{self.count_of_bread} 个喵！"
            return f"成功从用户{target_id}处偷取了{sbread}个面包喵！\n 当前面包数量：{self.count_of_bread} 个喵！"
        else:
            sbread = random.randint(1, self.target_bread.count_of_bread)
            self.steal_core(user_id, group_id, sbread, int(target_id))
            return f"成功从用户{target_id}处偷取了{sbread}个面包喵！\n 当前面包数量：{self.count_of_bread} 个喵！"
    
    
    def eat_bread(self, user_id, group_id) -> str: # eat bread function
        if self.count_of_bread <= 0:
            return f"杂鱼~你连面包都没有还想升级喵！"
        if self.level >= MAX_LEVEL:
            return f"你已经满级了喵！不能再升级了喵！"
        if self.level >= 10:
            debread = random.randint(-self.count_of_bread, self.count_of_bread)
            self.count_of_bread -= abs(debread)
            self.level += debread / 100
            if self.count_of_bread < 0:
                self.count_of_bread = 0
            self.update_data(user_id, group_id)
            if debread < 0:
                return f"吃坏肚子了喵！\n 面包数量减少了{abs(debread)} 个喵！\n 当前面包数量：{self.count_of_bread} 个喵！\n 等级变化：{debread/100} 级\n 当前等级：{math.floor(self.level)} 级"
            return f"成功吃到面包了喵！\n 吃掉了{abs(debread)} 个面包喵！\n 当前面包数量：{self.count_of_bread} 个喵！\n 等级变化：{debread/100} 级\n 当前等级：{math.floor(self.level)} 级"
        if self.level >= 5:
            debread = random.randint(-math.floor(self.count_of_bread/2), self.count_of_bread)
            self.count_of_bread -= abs(debread)
            self.level += debread / 100
            if self.count_of_bread < 0:
                self.count_of_bread = 0
            self.update_data(user_id, group_id)
            if debread < 0:
                return f"吃坏肚子了喵！\n 面包数量减少了{abs(debread)} 个喵！\n 当前面包数量：{self.count_of_bread} 个喵！\n 等级变化：{debread/100} 级\n 当前等级：{math.floor(self.level)} 级"
            return f"成功吃到面包了喵！\n 吃掉了{abs(debread)} 个面包喵！\n 当前面包数量：{self.count_of_bread} 个喵！\n 等级变化：{debread/100} 级\n 当前等级：{math.floor(self.level)} 级"
        else:
            debread = random.randint(1, self.count_of_bread)
            self.count_of_bread -= debread
            self.level += debread / 100
            self.update_data(user_id, group_id)
            return f"成功吃到面包了喵！\n 吃掉了{debread} 个面包喵！\n 当前面包数量：{self.count_of_bread} 个喵！\n 等级变化：{debread/100} 级\n 当前等级：{math.floor(self.level)} 级"

    
    
class status(base):
    def __init__(self, user_id: int, group_id: str):
        super().__init__(user_id, group_id)
        
        
    def show_status(self) -> str:
        protection_status = "开启" if self.Is_bread_protected else "关闭"
        return f"面包数量：{self.count_of_bread} 个喵！\n 面包保护：{protection_status} \n 当前等级：{math.floor(self.level)} 级喵！"
    
    
    def toggle_protection(self, user_id: int, group_id: str) -> str:
        self.Is_bread_protected = not self.Is_bread_protected
        self.update_data(user_id, group_id)
        protection_status = "开启" if self.Is_bread_protected else "关闭"
        return f"面包保护已切换为{protection_status}状态喵！"
    


class admin(base):
    def __init__(self, user_id: int, group_id: str):
        super().__init__(user_id, group_id)
    #TODO: add administer functions
    
    def fix_count_of_bread(self, user_id: int, group_id: str, new_count: int) -> str:
        self.count_of_bread = new_count
        self.update_data(user_id, group_id)
        return f"成功将用户{user_id}面包数量已修改为{new_count}个"
    
    
    def fix_level(self, user_id: int, group_id: str, new_level: int) -> str:
        self.level = new_level
        self.update_data(user_id, group_id)
        return f"成功将用户{user_id}面包等级已修改为{new_level}级"
    
    
    def fix_protection(self, user_id: int, group_id: str, new_status: bool) -> str:
        self.Is_bread_protected = new_status
        self.update_data(user_id, group_id)
        protection_status = "开启" if new_status else "关闭"
        return f"成功将用户{user_id}面包保护已修改为{protection_status}状态"