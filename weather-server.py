# 导入类型注解模块，用于类型提示
from typing import Any

# 导入 httpx，用于异步 HTTP 请求
import httpx
# 从 MCP SDK 导入 FastMCP，用于快速创建 MCP 服务器
from mcp.server.fastmcp import FastMCP

# 创建名为 "weather" 的 FastMCP 服务器实例
mcp = FastMCP("weather")
# 美国国家气象局 API 的基础 URL
NWS_API_BASE = "https://api.weather.gov"
# 请求时使用的 User-Agent，NWS API 要求必须提供
USER_AGENT = "weather-app/1.0"



# 定义异步函数：向 NWS API 发起请求，返回 JSON 或 None
async def make_nws_request(url: str) -> dict[str, Any] | None:
    # 函数的文档字符串，说明用途
    """请求 NWS API，带错误处理。"""
    # 设置请求头：User-Agent 为必填项，Accept 指定返回 GeoJSON 格式
    headers = {"User-Agent": USER_AGENT, "Accept": "application/geo+json"}
    # 创建异步 HTTP 客户端上下文
    async with httpx.AsyncClient() as client:
        # 捕获请求过程中的异常
        try:
            # 发起 GET 请求，超时 30 秒
            response = await client.get(url, headers=headers, timeout=30.0)
            # 若 HTTP 状态码为 4xx/5xx 则抛出异常
            response.raise_for_status()
            # 解析并返回 JSON 响应体
            return response.json()
        # 发生任何异常时返回 None，不中断程序
        except Exception:
            return None


# 定义函数：将单条警报数据格式化为可读字符串
def format_alert(feature: dict) -> str:
    # 函数的文档字符串
    """将警报数据格式化为可读字符串。"""
    # 从 GeoJSON feature 中取出 properties 字段
    props = feature["properties"]
    # 使用 f-string 拼接多行文本，包含事件、区域、严重程度、描述和指导
    return f"""
    Event: {props.get("event", "Unknown")}
    Area: {props.get("areaDesc", "Unknown")}
    Severity: {props.get("severity", "Unknown")}
    Description: {props.get("description", "No description available")}
    Instructions: {props.get("instruction", "No specific instructions provided")}
    """


# 使用 @mcp.tool() 装饰器，将该函数注册为 MCP 工具
@mcp.tool()
# 定义异步工具函数：根据州代码获取该州的天气警报
async def get_alerts(state: str) -> str:
    # 文档字符串：说明工具用途及参数
    """获取美国某州的天气警报。

    Args:
        state: 两字母州代码（如 CA, NY）
    """
    # 拼接 NWS 警报 API 的 URL
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    # 发起异步请求获取数据
    data = await make_nws_request(url)

    # 若请求失败或响应中无 features 字段，返回提示信息
    if not data or "features" not in data:
        return "无法获取警报或未找到警报。"

    # 若 features 为空列表，说明该州暂无警报
    if not data["features"]:
        return "该州暂无活跃警报。"

    # 用列表推导式将每条警报格式化为可读字符串
    alerts = [format_alert(f) for f in data["features"]]
    # 用分隔符拼接多条警报并返回
    return "\n---\n".join(alerts)


# 使用 @mcp.tool() 装饰器，将该函数注册为 MCP 工具
@mcp.tool()
# 定义异步工具函数：根据经纬度获取天气预报
async def get_forecast(latitude: float, longitude: float) -> str:
    # 文档字符串：说明工具用途及参数
    """获取某经纬度的天气预报。

    Args:
        latitude: 纬度
        longitude: 经度
    """
    # 拼接 NWS 点位 API 的 URL，用于获取该坐标的元数据
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    # 请求点位数据，其中包含预报接口的 URL
    points_data = await make_nws_request(points_url)

    # 若点位请求失败，返回提示信息
    if not points_data:
        return "无法获取该位置的预报数据。"

    # 从点位数据的 properties 中取出预报接口 URL
    forecast_url = points_data["properties"]["forecast"]
    # 请求详细预报数据
    forecast_data = await make_nws_request(forecast_url)

    # 若预报请求失败，返回提示信息
    if not forecast_data:
        return "无法获取详细预报。"

    # 从预报数据中取出各时段列表
    periods = forecast_data["properties"]["periods"]
    # 初始化用于存放格式化预报的列表
    forecasts = []
    # 遍历前 5 个时段（如今天、今晚、明天等）
    for period in periods[:5]:
        # 将每个时段的名称、温度、风力、详细描述格式化为字符串并追加
        forecasts.append(f"""
        {period["name"]}:
        Temperature: {period["temperature"]}°{period["temperatureUnit"]}
        Wind: {period["windSpeed"]} {period["windDirection"]}
        Forecast: {period["detailedForecast"]}
        """)

    # 用分隔符拼接各时段预报并返回
    return "\n---\n".join(forecasts)



    # 定义主函数，用于启动 MCP 服务器
def main():
    # 以 stdio 传输方式运行服务器，通过标准输入/输出与客户端通信
    mcp.run(transport="stdio")


# 当脚本被直接执行（而非被导入）时，调用 main 启动服务器
if __name__ == "__main__":
    main()