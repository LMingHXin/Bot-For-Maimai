import asyncio, json
from maimai_py import MaimaiClient, DivingFishProvider, PlayerIdentifier, ArcadeProvider
from .data import data

maimai = MaimaiClient()
diving_fish = DivingFishProvider(developer_token = "7bQMEdDJPiX8ysLlraSc9keUKAZn2Fqo")


class core():
    
    def __init__(self, user_id: int)-> None:
        self.userdata = data()
        self.user_id = user_id
        self.userlib = self.userdata.userlib
        
    async def update_maiscore(self) -> str:
        token =  self.userdata.get_user_token(self.user_id) # type: ignore
        dftoken = self.userdata.get_user_dftoken(self.user_id) # type: ignore
        if token == "" or dftoken == "":
            return f"未绑定水鱼TOKEN或未绑定舞萌TOKEN\n请使用指令'dfbind TOKEN'以及'maibind TOKEN'进行绑定"
        my_account = await maimai.qrcode(token)
        scores = await maimai.scores(my_account, provider=ArcadeProvider()) # type: ignore
        asyncio.gather(
        maimai.updates(PlayerIdentifier(credentials=dftoken), scores.scores, provider=diving_fish),
        )
        return "success"
    
    def maibind_token(self, user_id: int, token: str) -> str:
        if not self.userdata.check_user_exist(user_id):
            self.userlib[str(user_id)] = ["",""] # type: ignore
        self.userlib[str(user_id)][0] = token # type: ignore
        print(self.userlib[str(user_id)])  # type: ignore
        with open("/home/sa/maiscoreupdate_userlib.json", "w", encoding="utf-8") as f:
            json.dump(self.userlib, f, ensure_ascii=False, indent=4)
        return "舞萌绑定/更新成功！"

    def dfbind_token(self, user_id: int, token: str) -> str:
        if not self.userdata.check_user_exist(user_id):
            self.userlib[str(user_id)] = ["",""] # type: ignore
        self.userlib[str(user_id)][1] = token # type: ignore 
        print(self.userlib[str(user_id)])  # type: ignore
        with open("/home/sa/maiscoreupdate_userlib.json", "w", encoding="utf-8") as f:
            json.dump(self.userlib, f, ensure_ascii=False, indent=4)
        return "水鱼绑定/更新成功！"