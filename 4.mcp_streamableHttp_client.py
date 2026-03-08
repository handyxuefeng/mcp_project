import sys
import os
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
import asyncio


# 通用的消息处理器，用于处理服务器推送过来的消息，比如说进度通知等
def on_message(message):
    # 获取消息根对象，可能就是消息本身
    root = getattr(message, "root", message)
    # 获取方法名
    method = getattr(root, "method", "notifications/message")
    if method == "notifications/progress":
        parmas = getattr(root, "parmas", {})
        if parmas is not None:
            progress = getattr(parmas, "progress", 0)
            total = getattr(parmas, "total", 1)
            message = getattr(parmas, "message", "")
            print(f"[PROGRESS] {progress}/{total} - {message}")


# 进度回调函数 显示实时进度
def on_progress(progress: float, total: float | None, message: str | None):
    print(f"[进度] {progress}/{total} - {message}")


# 日志回调函数，当服务器发送日志消息时调用
def on_logging(params: types.LoggingMessageNotificationParams):
    level = getattr(params, "level", "info")
    data = getattr(params, "data", "")
    logger = getattr(params, "logger", "logger")
    print(f"[日志][{level}]", str(data), logger)


async def run_client():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    server_path = os.path.join(base_dir, "context_server.py")
    server_params = StdioServerParameters(command="python", args=[server_path])
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(
            read, write, logging_callback=on_logging, message_handler=on_message
        ) as session:
            # 1.初始化对话，完成握手
            await session.initialize()
            # 2.调用工具
            result = await session.call_tool(
                "long_running_task",
                {"task_name": "读取资源任务", "steps": 3},
                progress_callback=on_progress,
            )
            texts = []
            for block in result.content:
                if isinstance(block, types.TextContent):
                    texts.append(block.text)
            print(f"工具执行结果:", "|".join(texts))


if __name__ == "__main__":
    asyncio.run(run_client())
