import json

class data():
    def __init__(self) -> None:
        self.userlib = {str: list}
        with open("/home/sa/maiscoreupdate_userlib.json", "r", encoding="utf-8") as f:
            self.userlib = json.load(f)
        '''{
            "User_Id":[TOKEN, dftoken]
            }'''
    
    def get_user_token(self, user_id: int) -> str:
        with open("/home/sa/maiscoreupdate_userlib.json", "r", encoding="utf-8") as f:
            self.userlib = json.load(f)
        print(self.userlib[str(user_id)])
        try:
            token = self.userlib[str(user_id)][0]
            return token
        except:
            return ""
        
    def get_user_dftoken(self, user_id: int) -> str:
        with open("/home/sa/maiscoreupdate_userlib.json", "r", encoding="utf-8") as f:
            self.userlib = json.load(f)
        try:
            token = self.userlib[str(user_id)][1]
            return token
        except:
            return ""
        
    def check_user_exist(self, user_id: int) -> bool:
        with open("/home/sa/maiscoreupdate_userlib.json", "r", encoding="utf-8") as f:
            self.userlib = json.load(f)
        try:
            _ = self.userlib[str(user_id)]
            return True
        except:
            return False