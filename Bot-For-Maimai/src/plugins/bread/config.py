from pydantic import BaseModel


class Config(BaseModel):
    Acess_Group: list[int] = [1060336528]  # 可以使用的群
    Admin_user : list[int] = [1619445266, 2654625014]  # 管理员用户ID