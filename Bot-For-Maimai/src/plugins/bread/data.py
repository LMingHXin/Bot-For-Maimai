import json

class data():
    def __init__(self):
        self.user_data = {}
        '''{
            "Group_Id": {
                "User_Id": {
                    "count_of_bread": int,
                    "Is_bread_protected": bool,
                    "level": int,
                }
            }
        }'''
        self.count_of_bread: int
        self.Is_bread_protected: bool
        self.level: float
        
    def get_user_data(self, user_id: int, group_id: str) -> bool:
        with open("/home/sa/bread_data.json", "r", encoding="utf-8") as f:
            self.user_data = json.load(f)
        try:
            self.count_of_bread = self.user_data[group_id][str(user_id)]["count_of_bread"]
            self.Is_bread_protected = self.user_data[group_id][str(user_id)]["Is_bread_protected"]
            self.level = self.user_data[group_id][str(user_id)]["level"]   
            return True
        except:
            return False
    
    def update_user_data(self, count_of_bread: int, Is_bread_protected: bool, level: int, user_id: int, group_id: str) -> None:
        with open("/home/sa/bread_data.json", "w", encoding="utf-8") as f:
            self.user_data[group_id][str(user_id)] = {
                "count_of_bread": count_of_bread,  
                "Is_bread_protected": Is_bread_protected,
                "level": level,
            }
            json.dump(self.user_data, f, ensure_ascii=False, indent=4)
    
    def get_user_list(self, group_id: str) -> list:
        with open("/home/sa/bread_data.json", "r", encoding="utf-8") as f:
            self.user_data = json.load(f)
        try:
            user_list = list(self.user_data[group_id].keys())
            return user_list
        except:
            return []

Data = data() #type: ignore