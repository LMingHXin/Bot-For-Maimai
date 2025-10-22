from pydantic import BaseModel


class Config(BaseModel):
    access_groups: list[int] = [106033652, 1025615469]  # 可使用该功能的群号列表
