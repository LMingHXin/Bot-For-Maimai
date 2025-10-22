from .data import Data
import random, math, time
MAX_LEVEL = 20

class base():
    def __init__(self, user_id: int, group_id: str):
        self.user_data = {}  # type: ignore
        if Data.get_user_data(user_id, group_id):
            self.count_of_bread = Data.count_of_bread
            self.Is_bread_protected = Data.Is_bread_protected
            self.level = Data.level
            self.last_eat_time = Data.last_eat_time
        else:
            self.count_of_bread = 0
            self.Is_bread_protected = False
            self.level = 1.0
            self.bind_group = str(group_id)
            self.last_eat_time = ""
            Data.update_user_data(
                self.count_of_bread,
                self.Is_bread_protected,
                self.level, # type: ignore
                user_id,
                group_id,
                self.last_eat_time
            )
        self.target_bread = None
    
    def update_data(self, user_id: int, group_id: str) -> None:
        Data.update_user_data(
            self.count_of_bread,
            self.Is_bread_protected,
            self.level, # type: ignore
            user_id,
            group_id,
            self.last_eat_time
        )
        

class bread(base):
    def __init__(self, user_id: int, group_id: str):
        super().__init__(user_id, group_id)
        
    
    def get_bread(self, user_id: int, group_id: str) -> str: # get bread function
        dbread : int
        if self.level >= 10:
            dbread = random.randint(-self.count_of_bread, 10)
            if dbread < 0:
                self.count_of_bread += dbread
                if self.count_of_bread < 0:
                    self.count_of_bread = 0
                    base.update_data(self, user_id, group_id)
                    return f"买到坏面包了喵！\n 面包数量减少了{abs(dbread)} 个喵！\n 当前面包数量：{self.count_of_bread} 个喵！\n不想让你负债喵，人家帮你归零了喵~"
                else:
                    base.update_data(self, user_id, group_id)
                    return f"买到坏面包了喵！\n 面包数量减少了{abs(dbread)} 个喵！\n 当前面包数量：{self.count_of_bread} 个喵！"
            else:
                self.count_of_bread += dbread
                base.update_data(self, user_id, group_id)
                return f"成功购买了喵！\n 面包数量增加了{dbread} 个喵！\n 当前面包数量：{self.count_of_bread} 个喵！"
        if self.level >= 5:
            dbread = random.randint(-3, 5)
            if dbread < 0:
                self.count_of_bread += dbread
                if self.count_of_bread < 0:
                    self.count_of_bread = 0
                    base.update_data(self, user_id, group_id)
                    return f"买到坏面包了喵！\n 面包数量减少了{abs(dbread)} 个喵！\n 当前面包数量：{self.count_of_bread} 个喵！\n不想让你负债喵，人家帮你归零了喵~"
                else:
                    base.update_data(self, user_id, group_id)
                    return f"买到坏面包了喵！\n 面包数量减少了{abs(dbread)} 个喵！\n 当前面包数量：{self.count_of_bread} 个喵！"
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
        if self.Is_bread_protected:
            return "你开启了面包保护喵，偷取失败喵！"
        if len(usr_list) <= 1:
            return "当前群组内面包用户数量不足，无法偷取面包喵！"
        temp_list = usr_list.copy()
        while True:
            target_id = random.choice(temp_list)
            self.target_bread = base(int(target_id), str(group_id))
            if target_id != str(user_id) and not self.target_bread.Is_bread_protected and self.target_bread.count_of_bread > 0: 
                break
            temp_list.remove(target_id)
            if len(temp_list) <= 0:
                return "找不到可偷取面包的用户喵！"
        if self.level >= 10:
            sbread = random.randint(-10, self.target_bread.count_of_bread)
            self.steal_core(user_id, group_id, sbread, int(target_id))
            if sbread < 0:
                if self.count_of_bread < 0:
                    self.count_of_bread = 0
                    self.update_data(user_id, group_id)
                    return f"被防卫了喵！\n 用户{target_id}抢了你{abs(sbread)}个面包喵！\n 当前面包数量：{self.count_of_bread} 个喵！\n不想让你负债喵，人家帮你归零了喵~"
                return f"被防卫了喵！\n 用户{target_id}抢了你{abs(sbread)}个面包喵！\n 当前面包数量：{self.count_of_bread} 个喵！"
            return f"成功从用户{target_id}处偷取了{sbread}个面包喵！\n 当前面包数量：{self.count_of_bread} 个喵！"
        else:
            sbread = random.randint(1, self.target_bread.count_of_bread)
            self.steal_core(user_id, group_id, sbread, int(target_id))
            return f"成功从用户{target_id}处偷取了{sbread}个面包喵！\n 当前面包数量：{self.count_of_bread} 个喵！"
    
    def luck_eat_bread(self) -> str: # eat bread function
        if self.level < 5:
            return "normal"
        luck = random.randint(1, 100)
        if luck <= 3:
            self.debread = -self.debread
            return "badluck"
        if luck >= 98:
            self.debread = self.debread * 2
            return "bestluck"
        return "normal"
        
    def eat_bread(self, user_id, group_id) -> str: # eat bread function
        if self.count_of_bread <= 0:
            return f"杂鱼~你连面包都没有还想升级喵！"
        if self.level >= MAX_LEVEL:
            return f"你已经满级了喵！不能再升级了喵！"
        runtime = time.time()
        if self.last_eat_time == "":
            self.last_eat_time = str(runtime)
        else:
            last_time = float(self.last_eat_time)
            if runtime - last_time < 3600:
                next_eat = 3600 - (runtime - last_time)
                minutes = math.floor(next_eat / 60)
                seconds = math.floor(next_eat % 60)
                return f"距离下一次吃面包还有{minutes}分{seconds}秒喵！"
            else:
                self.last_eat_time = str(runtime)
        if self.level >= 10:
            self.debread = random.randint(1, self.count_of_bread)
            self.count_of_bread -= abs(self.debread)
            res = self.luck_eat_bread()
            self.level += abs(self.debread) / 200
            if self.count_of_bread < 0:
                self.count_of_bread = 0
            self.update_data(user_id, group_id)
            if res == "badluck":
                return f"吃坏肚子了喵！\n 面包数量减少了{abs(self.debread)} 个喵！\n 当前面包数量：{self.count_of_bread} 个喵！\n 等级变化：{self.debread/200} 级\n 当前等级：{math.floor(self.level)} 级"
            if  res == "bestluck":
                return f"运气爆棚喵！获得了双倍等级喵！\n 吃掉了{abs(self.debread/2)} 个面包喵！\n 当前面包数量：{self.count_of_bread} 个喵！\n 等级变化：{abs(self.debread)/200} 级\n 当前等级：{math.floor(self.level)} 级"
            return f"成功吃到面包了喵！\n 吃掉了{abs(self.debread)} 个面包喵！\n 当前面包数量：{self.count_of_bread} 个喵！\n 等级变化：{self.debread/200} 级\n 当前等级：{math.floor(self.level)} 级"
        if self.level >= 5:
            self.debread = random.randint(-1, self.count_of_bread)
            self.count_of_bread -= abs(self.debread)
            res = self.luck_eat_bread()
            self.level += abs(self.debread) / 100
            if self.count_of_bread < 0:
                self.count_of_bread = 0
            self.update_data(user_id, group_id)
            if res == "badluck":
                return f"吃坏肚子了喵！\n 面包数量减少了{abs(self.debread)} 个喵！\n 当前面包数量：{self.count_of_bread} 个喵！\n 等级变化：{self.debread/100} 级\n 当前等级：{math.floor(self.level)} 级"
            if res == "bestluck":
                return f"运气爆棚喵！获得了双倍等级喵！\n 吃掉了{abs(self.debread/2)} 个面包喵！\n 当前面包数量：{self.count_of_bread} 个喵！\n 等级变化：{abs(self.debread)/100} 级\n 当前等级：{math.floor(self.level)} 级"
            return f"成功吃到面包了喵！\n 吃掉了{abs(self.debread)} 个面包喵！\n 当前面包数量：{self.count_of_bread} 个喵！\n 等级变化：{self.debread/100} 级\n 当前等级：{math.floor(self.level)} 级"
        else:
            debread = random.randint(1, self.count_of_bread)
            self.count_of_bread -= debread
            self.level += debread / 10
            self.update_data(user_id, group_id)
            return f"成功吃到面包了喵！\n 吃掉了{debread} 个面包喵！\n 当前面包数量：{self.count_of_bread} 个喵！\n 等级变化：{debread/10} 级\n 当前等级：{math.floor(self.level)} 级"

    
    
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
        if Data.get_user_data(user_id, group_id):
            self.update_data(user_id, group_id)
            return f"成功将用户{user_id}面包数量已修改为{new_count}个"
        else:
            return f"修改用户{user_id}面包数量失败，可能是该用户不存在"
    
    
    def fix_level(self, user_id: int, group_id: str, new_level: int) -> str:
        self.level = new_level
        if Data.get_user_data(user_id, group_id):
            if new_level > MAX_LEVEL:
                self.level = MAX_LEVEL
            self.update_data(user_id, group_id)
            return f"成功将用户{user_id}面包等级已修改为{new_level}级"
        else:
            return f"修改用户{user_id}面包等级失败，可能是该用户不存在"
    
    
    def fix_protection(self, user_id: int, group_id: str, new_status: bool) -> str:
        self.Is_bread_protected = new_status
        if Data.get_user_data(user_id, group_id):
            self.update_data(user_id, group_id)
            protection_status = "开启" if new_status else "关闭"
            return f"成功将用户{user_id}面包保护已修改为{protection_status}状态"
        else:
            return f"修改用户{user_id}面包保护状态失败，可能是该用户不存在"