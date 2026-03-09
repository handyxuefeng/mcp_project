import sys

# from mcp import StdioServerParameters
# from mcp.client.stdio import stdio_client
from mcp_lite import StdioServerParameters
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
    with stdio_client(params) as sub_process:

        # 读取子进程中通过print输出的内容,并打印出来
        subprocess_output = (
            sub_process.stdout.readline()
        )  # 从子进程的标准输出中读取一行数据
        print(f"获取到子进程print的内容: {subprocess_output.strip()}")  # 打印

        print(f"read: {sub_process.stdin}, write: {sub_process.stdout}")
        pass


if __name__ == "__main__":
    main()
