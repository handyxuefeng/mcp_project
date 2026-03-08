import sys
from mcp.server.fastmcp import FastMCP, Context

mcp = FastMCP(name="MCP服务器")


@mcp.resource("data://message")
def static_message() -> str:
    """示例的静态资源：用于演示在工具中通过Context读取资源"""
    return "这是一条来自于data://message的资源内容"


@mcp.tool()
async def long_running_task(task_name: str, ctx: Context, steps: int = 5) -> str:
    """执行一个带进度的任务，期间输出日志、读取资源并返回总结"""
    if ctx is None:
        return "未注入Context，无法使用日志/进度/资源读取操作"
    steps = int(steps)
    # 向客户端发送debug级别的日志，通知开始执行任务
    await ctx.debug(f"开始执行任务:{task_name}")
    await ctx.info(f"初始化任务环境")
    # 可以使用ctx.read_resource读取服务器提供的资源
    resource_result = await ctx.read_resource("data://message")
    resource_preview = "<empty>"
    for block in resource_result:
        resource_preview = getattr(
            block, "text", getattr(block, "content", "<no-text>")
        )
        break
    await ctx.info(f"读取资源成功:{resource_preview}")
    for i in range(steps):
        # 计算当前进度
        progress = (i + 1) / steps
        # 通过context上报当前的进度progress
        await ctx.report_progress(
            progress=progress, total=1.0, message=f"步骤 {i+1}/{steps}"
        )
        await ctx.debug(f"进度 {i+1}/{steps}")
    req_id = ctx.request_id
    await ctx.info(f"任务完成:{task_name} req_id={req_id}")
    return f"任务{task_name}完成。读取到的资源为:{resource_preview}"


if __name__ == "__main__":
    print("启动MCP服务器(stdio模式)", file=sys.stderr)
    mcp.run(transport="stdio")



#npx @modelcontextprotocol/inspector uv --directory /Users/hanxuefeng/project/mcp_project run mcp_context_server.py