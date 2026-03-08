# 导入 FastMCP 高层服务器类
from mcp.server.fastmcp import FastMCP
# 导入 json 模块，用于序列化配置数据
import json
# 导入 sys 模块，用于访问标准流
import sys
# 创建 FastMCP 实例，命名为 Resources MCP Server
mcp = FastMCP(name="Resources MCP Server")

# 通过 @mcp.resource 装饰器注册静态资源，URI 为 config://settings，指定 MIME 类型为 application/json
@mcp.resource("config://settings", mime_type="application/json")
# 定义静态资源处理函数，不带参数，返回配置的 JSON 字符串
async def get_settings() -> str:
    # 返回应用的 JSON 配置文本，包含主题、语言和调试开关
    return json.dumps(
        {"theme": "dark", "language": "zh-CN", "debug": False},
        ensure_ascii=False,
        indent=2,
    )

# 注册模板资源，URI 为 greeting://{name}，支持动态参数 name，MIME 类型为 text/plain
@mcp.resource("greeting://{name}", mime_type="text/plain")
# 定义模板资源处理函数，参数 name 必须和 URI 占位符一致
async def greeting(name: str) -> str:
    # 根据传入的 name 返回个性化问候语
    return f"Hello, {name}! 欢迎使用 MCP 资源。"

# 注册另一个模板资源，URI 为 user://{id}，MIME 类型为 text/plain
@mcp.resource("user://{id}", mime_type="text/plain")
# 定义用户信息资源处理函数，参数 id 必须和 URI 占位符一致
async def user_profile(id: str) -> str:
    # 判断 id 是否为 001，如果是则返回 Alice 的信息
    if id == "001":
        return "用户 001：Alice，角色：admin"
    # 判断 id 是否为 002，如果是则返回 Bob 的信息
    if id == "002":
        return "用户 002：Bob，角色：viewer"
    # 其他情况返回未找到用户的提示信息
    return f"未找到用户 {id}"

# 如果当前模块作为主程序运行
if __name__ == "__main__":
    # 检查 sys.stdout 是否支持 reconfigure 方法（用于设置编码）
    if hasattr(sys.stdout, 'reconfigure'):
        # "PYTHONIOENCODING": "utf-8"
        # 设置标准输出编码为 utf-8，避免中文乱码
        sys.stdout.reconfigure(encoding='utf-8')
        # 设置标准输入编码为 utf-8
        sys.stdin.reconfigure(encoding='utf-8')
    # 使用 stdio 作为通信方式启动 MCP 服务器
    mcp.run(transport="stdio")