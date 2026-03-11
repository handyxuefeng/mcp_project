from pydantic import BaseModel, ConfigDict

# to_camel 是把蛇形命名转换成驼峰命名
from pydantic.alias_generators import to_camel


class MCPModel(BaseModel):

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class User(MCPModel):
    first_name: str
    last_name: str


user = User(first_name="nick", last_name="linda")

# 输出：{'firstName': 'nick', 'lastName': 'linda'}
print(user.model_dump(by_alias=True))
