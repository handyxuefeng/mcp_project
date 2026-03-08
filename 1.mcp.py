import sys
#from mcp import StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio

from mcp_lite import StdioServerParameters
from mcp_lite.client.stdio import stdio_client

def main():

    """
    params = StdioServerParameters(command="python",args=[__file__,"serve"])
    等价于
    python 1.mcp.py serve
    
    """
    params = StdioServerParameters(command="python",args=[__file__,"serve"])
    
    #创建一个mcp客户端
    with stdio_client(params) as (read,write):
        print(f"read: {read}, write: {write}")
        #向服务器发送消息
        #await write("Hello, MCP Server!")
        
        #从服务器接收消息
        #esponse = await read()
        #print(f"Received from server: {response}")
        pass

if __name__ == "__main__":
    main()