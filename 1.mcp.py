import sys
import json

# from mcp import StdioServerParameters
# from mcp.client.stdio import stdio_client
from mcp_lite import StdioServerParameters, ClientSession
from mcp_lite.client.stdio import stdio_client
from mcp_lite.types import JSONRPCResponse

import asyncio
import os


def mcp_serve():
    """MCP 服务端逻辑"""
    while True:

        # 子进程从stdin读取数据
        line = sys.stdin.readline()
        if not line:
            break

        try:
            request = json.loads(line.strip())
            print(f"服务端收到请求: {request}", file=sys.stderr)

            if request.get("method") == "initialize":
                response = JSONRPCResponse(
                    jsonrpc="2.0",
                    id=request.get("id"),
                    result={
                        "protocolVersion": "2024-11-05",
                        "capabilities": {},
                        "serverInfo": {"name": "mcp-lite-server", "version": "0.1.0"},
                    },
                )
                print(response.model_dump_json(exclude_none=True), flush=True)
        except Exception as e:
            print(f"服务端错误: {e}", file=sys.stderr)


def mcp_client():
    """MCP 客户端逻辑"""
    params = StdioServerParameters(command="python", args=[__file__, "serve"])
    with stdio_client(params) as (readsteam, writestream):
        client_session = ClientSession(readsteam, writestream)

        client_session.initialize()
        print("初始化成功！")


def main():
    """
    params = StdioServerParameters(command="python",args=[__file__,"serve"])
    等价于
    python 1.mcp.py serve

    """
    if len(sys.argv) > 1 and sys.argv[1] == "serve":
        mcp_serve()
    else:
        mcp_client()


if __name__ == "__main__":
    main()
