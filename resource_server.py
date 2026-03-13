import sys
import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="mcp资源列表服务器")


# 通过@mcp.resource装饰器来配置资源
# 配置资源，资源的类型为json
@mcp.resource("config://settings", mime_type="application/json")
async def get_settings():
    return json.dumps(
        {"code": 0, "msg": "success", "data": "mcp 资源列表"},
        ensure_ascii=False,
        indent=2,
    )


@mcp.resource("greeting://{name}", mime_type="text/plain")
async def get_resource(name: str):
    return f"你好，{name}, 这是mcp资源列表服务器"


@mcp.resource("user://{user_id}", mime_type="text/plain")
async def get_user(user_id: str):
    if user_id == "0001":
        return "用户0001，Alice，角色：admin"
    elif user_id == "0002":
        return "用户0002，Bob，角色：user"
    else:
        return f"用户{user_id}不存在"


if __name__ == "__main__":
    print("mcp资源列表服务器启动")
    mcp.run(transport="stdio")


# npx @modelcontextprotocol/inspector uv --directory /Users/hanxuefeng/project/mcp_project run resource_server.py
