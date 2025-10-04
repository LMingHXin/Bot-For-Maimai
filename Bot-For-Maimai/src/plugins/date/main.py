from nonebot import get_plugin_config

from .config import Config

config = get_plugin_config(Config)

class maindate():
    def __init__(self):
        self.date_list = []  # 约会列表
        self.date_id = 0  # 约会ID
        self.user_dates = {}  # 用户的约会 {user_id: [date_id, ...]}
        self.group_dates = {}  # 群的约会 {group_id: [date_id, ...]}
    
    def create_date(self, user_id, group_id, content) -> dict:  # 创建约会
        self.date_id += 1
        date = {
            "id": self.date_id,
            "参与人员": [],
            "群聊": group_id,
            "主题": content,
        }
        date["参与人员"].append(user_id)
        self.date_list.append(date) # type: ignore
        if user_id not in self.user_dates:
            self.user_dates[user_id] = []
        self.user_dates[user_id].append(self.date_id)
        if group_id not in self.group_dates:
            self.group_dates[group_id] = []
        self.group_dates[group_id].append(self.date_id)
        return date
    
    def join_date(self, user_id, date_id) -> bool:  # 参加约会
        for date in self.date_list: # type: ignore
            if date["id"] == date_id:
                if "参与人员" not in date:
                    date["参与人员"] = []
                if user_id not in date["参与人员"]:
                    date["参与人员"].append(user_id)
                    if user_id not in self.user_dates:
                        self.user_dates[user_id] = []
                    self.user_dates[user_id].append(date_id)
                    return True
                else:
                    return False
        return False  
    
    def quit_date(self, user_id, date_id) -> bool:  # 退出约会
        for date in self.date_list: # type: ignore
            if date["id"] == date_id:
                if "参与人员" in date and user_id in date["参与人员"]:
                    date["参与人员"].remove(user_id)
                    if user_id in self.user_dates and date_id in self.user_dates[user_id]:
                        self.user_dates[user_id].remove(date_id)
                    return True
                else:
                    return False
        return False
    
    def get_date_list(self, group_id) -> list:  # 获取群的约会列表
        if group_id in self.group_dates:
            print(date for date in self.date_list if date["id"] in self.group_dates[group_id]) # type: ignore
            return [date for date in self.date_list if date["id"] in self.group_dates[group_id]] # type: ignore # 返回该群的约会列表
        return [] # 返回空值
    
    def get_date(self, date_id) -> dict:  # 获取约会详情
        for date in self.date_list: # type: ignore
            if date["id"] == date_id:
                return date
        return None  # type: ignore # 返回None表示未找到
    
    def delete_date(self, date_id) -> bool:  # 删除约会
        for date in self.date_list: # type: ignore
            if date["id"] == date_id:
                self.date_list.remove(date) # type: ignore
                group_id = date["群聊"]
                if group_id in self.group_dates and date_id in self.group_dates[group_id]:
                    self.group_dates[group_id].remove(date_id)
                for user_id in date.get("参与人员", []):
                    if user_id in self.user_dates and date_id in self.user_dates[user_id]:
                        self.user_dates[user_id].remove(date_id)
                return True
        return False  # 返回False表示未找到
    
maindate = maindate() # type: ignore