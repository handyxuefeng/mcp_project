# 导入 TypeAdapter
from pydantic import TypeAdapter

# 验证 dict[str, int]：键为字符串，值为整数
adapter = TypeAdapter(dict[str, int])
# 从字典验证
data = adapter.validate_python({"a": 1, "b": 2, "c": 3})
print("字典:", data)

# 从 JSON 解析
json_str = '{"x": 10, "y": 20}'
data2 = adapter.validate_json(json_str)
print("解析:", data2)
