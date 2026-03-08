# 导入类型注解模块，用于类型提示
from typing import Any

# 导入 httpx，用于异步 HTTP 请求
import httpx
# 从 MCP SDK 导入 FastMCP，用于快速创建 MCP 服务器
from mcp.server.fastmcp import FastMCP

# 创建名为 "weather" 的 FastMCP 服务器实例
mcp = FastMCP(name="获取中国城市天气预报服务", port=8001)

# 定义异步函数：向中国天气预报 API 发起请求，返回 JSON 或 None
@mcp.tool()
async def get_china_weather(city: str) -> dict[str, Any] | None:
    """获取中国城市的天气预报。"""
    # 中国天气预报 API 的基础 URL，使用免费接口
    API_URL = f"https://wttr.in/{city}?format=j1"
    # 创建异步 HTTP 客户端上下文
    async with httpx.AsyncClient() as client:
        # 捕获请求过程中的异常
        try:
            # 发起 GET 请求，超时 30 秒
            response = await client.get(API_URL, timeout=30.0)
            # 若 HTTP 状态码为 4xx/5xx 则抛出异常
            response.raise_for_status()
            # 解析并返回 JSON 响应体
            return response.json()
        # 发生任何异常时返回 None，不中断程序
        except Exception:
            return None
        
# 判断当前文件是否作为主程序运行
if __name__ == "__main__":
    mcp.run(transport="streamable-http")