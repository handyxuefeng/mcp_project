import sys

# from mcp import StdioServerParameters
# from mcp.client.stdio import stdio_client
from mcp_lite import StdioServerParameters, ClientSession
from mcp_lite.client.stdio import stdio_client

import asyncio
import os


def main():
    """
    params = StdioServerParameters(command="python",args=[__file__,"serve"])
    等价于
    python 1.mcp.py serve

    """
    params = StdioServerParameters(command="python", args=[__file__, "serve"])

    # 创建一个mcp客户端,通过stdio_client上下文管理器与子进程通信
    with stdio_client(params) as (readsteam, writestream):
        # 创建客户端会话
        client_session = ClientSession(readsteam, writestream)

        # 初始化
        client_session.initialize()


if __name__ == "__main__":
    main()
