import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.server.fastmcp import FastMCP
import asyncio

mcp = FastMCP(name="MCP工具服务器")


# 使用装饰器注册工具，工具名称为hello
@mcp.tool()
def hello():
    return "Hello from MCP server"


@mcp.tool()
def calculate_sum(a: int, b: int):
    return a + b


async def run_client():
    # python 1.mcp.py serve
    server_params = StdioServerParameters(command="python", args=[__file__, "serve"])
    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            # 1.初始化对话，完成握手
            await session.initialize()
            # 2. 获取mcp server 服务器的工具列表
            tools = await session.list_tools()

            # 调用名为hello的工具

            result = await session.call_tool("hello", arguments={})
            tool_texts = []
            print("result=", type(result.content))
            for content in result.content:
                if isinstance(content, dict) and content.get("text") == "text":
                    tool_texts.append(content.get("text", ""))
                elif hasattr(content, "text"):
                    tool_texts.append(content.text)

            print("[Call Hello]的结果为：", "\n".join(tool_texts))

            # 调用名为calculate_sum的工具
            """
            result={
                content:[
                    0:{
                        type:"text"
                        text:"3"
                    }
                ]
                isError:
                false
            }
            """
            result = await session.call_tool(
                "calculate_sum", arguments={"a": 1, "b": 2}
            )
            tool_texts = []
            print("result=", type(result.content))
            for content in result.content:
                if isinstance(content, dict) and content.get("text") == "text":
                    print("content=", "类型为字典")
                    tool_texts.append(content.get("text", ""))
                elif hasattr(content, "text"):
                    print("elseesee=", content.text)
                    tool_texts.append(content.text)

            print("[Call calculate_sum]的结果为：", "\n".join(tool_texts))


def run_server():
    print("启动MCP服务器(stdio模式)", file=sys.stderr)
    mcp.run(transport="stdio")


def main():
    # Inspector 或直接运行（uv run tool_server.py）时需要以 stdio 服务器模式启动
    # 只有显式传 "client" 时才跑客户端示例
    if len(sys.argv) >= 2 and sys.argv[1] == "client":
        asyncio.run(run_client())
    else:
        run_server()


if __name__ == "__main__":
    main()
