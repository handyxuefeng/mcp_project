# 导入 FastMCP 类，用于搭建 MCP 服务器
from mcp.server.fastmcp import FastMCP

# 创建 FastMCP 实例，指定服务器名称为 "HTTP Server"
mcp = FastMCP(name="HTTP Server")

# 使用 MCP 的 tool 装饰器注册工具函数
@mcp.tool()
# 定义 greet 工具，接收参数 name，默认值为 "World"
def greet(name: str = "World") -> str:
    # 返回一个格式化的问候字符串
    return f"Hello, {name}，这里是来自mcp服务器的问候!"

# 判断当前文件是否作为主程序运行
if __name__ == "__main__":
    # 启动 MCP 服务器，采用 streamable-http 协议进行传输
    mcp.run(transport="streamable-http")
