# 导入 TypeAdapter
from pydantic import TypeAdapter
from pydantic.alias_generators import to_camel

# 创建适配器：验证 list[int] 类型
adapter = TypeAdapter(list[int])

# 从 Python 数据验证并转换
result = adapter.validate_python([1, 2, 3])
print("验证结果1111:", result)

# 从 JSON 字符串解析
result2 = adapter.validate_json("[10, 20, 30]")
print("解析结果:", result2)

print(to_camel("hello_world"))  # 输出: "helloWorld"