import sys
from mcp.server.fastmcp import FastMCP
import json
from mcp.server.fastmcp.prompts import base
mcp = FastMCP(name="提示词mcp服务")


#使用@mcp.prompt装饰器注册一个提示词生成函数


@mcp.prompt(description="根据输入的文本生成提示词")
def greet_user(name: str, style: str) -> str:
    """根据姓名和风格生成问候语"""
    styles:dict[str,str] = {
        "friendly": "尊敬的{name}，您好！",
        "casual": "嗨，{name}！",
        "humorous": "嘿，{name}！准备好迎接一天的冒险了吗？",
        "poetic": "啊，{name}，如同晨露般清新，愿你的一天如诗般美好！"
    }
    return styles.get("friendly", "尊敬的{name}，您好！").format(name=name)



@mcp.prompt(title="调试助手")
def debug_assistant(error:str) -> list[base.Message]:
    """根据姓名和风格生成问候语"""
    messages = [
        # base.message(role="system", content="你是一个调试助手，帮助用户分析错误信息并提供解决方案。"),
        # base.message(role="user", content=f"我遇到了以下错误：{error}"),
        # base.message(role="assistant", content="请分析这个错误并提供可能的解决方案。")
        base.UserMessage("我遇到了以下错误："),
        

        #用户信息
        base.UserMessage(error),

        #第三条消息
        base.AssistantMessage("请分析这个错误并提供可能的解决方案。")

    ]
    return messages



#npx @modelcontextprotocol/inspector uv --directory /Users/hanxuefeng/project/mcp_project run prompt_server.py

if __name__ == "__main__":  
    mcp.run(transport="stdio")



      
