from pydantic import BaseModel


class Config(BaseModel):
    date_group: list = [1060336528]  # 可以使用约会功能的群
    admin_group: list = [1060336528]  # 可以使用管理功能的
    admin: list = [2654625014, 1619445266]  # 管理员QQ号
