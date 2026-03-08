# 导入os模块，用于文件路径操作
import os
# 从pydantic库导入AnyUrl类型，用于资源URI的类型校验
from pydantic import AnyUrl
# 从mcp_lite导入ClientSession、StdioServerParameters和types
from mcp_lite import (
    ClientSession,
    StdioServerParameters,
    types,
)
# 从mcp_lite.client.stdio模块导入stdio_client工厂方法
from mcp_lite.client.stdio import stdio_client


def main() -> None:
    # 获取当前文件的绝对路径所在目录
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # 拼接得到服务器脚本的完整路径
    server_path = os.path.join(base_dir, "resources_server.py")
    # 配置以stdio方式启动服务器的参数
    server_params = StdioServerParameters(
        command="python",
        args=[server_path],
        env={},
    )
    # 建立到服务器的stdio连接
    with stdio_client(server_params) as (read, write):
        # 创建客户端会话并初始化
        session = ClientSession(read, write)
        session.initialize()
        # 列出已注册的静态资源（不带占位符的资源）
        resources = session.list_resources()
        print("[Resources]", [r.uri for r in resources.resources])
        # 列出资源模板（带占位符的资源）
        templates = session.list_resource_templates()
        print(
            "[ResourceTemplates]",
            [t.uri_template for t in templates.resource_templates],
        )
        # 读取静态资源 config://settings
        result_config = session.read_resource(AnyUrl("config://settings"))
        texts_config = []
        for block in result_config.contents:
            if isinstance(block, types.TextResourceContents):
                texts_config.append(block.text)
        print("[Read config://settings]", " | ".join(texts_config))
        # 读取模板资源 greeting://Alice
        result_greet = session.read_resource(AnyUrl("greeting://Alice"))
        texts_greet = []
        for block in result_greet.contents:
            if isinstance(block, types.TextResourceContents):
                texts_greet.append(block.text)
        print("[Read greeting://Alice]", " | ".join(texts_greet))
        # 读取模板资源 user://001 与 user://003
        for uid in ["001", "003"]:
            result_user = session.read_resource(AnyUrl(f"user://{uid}"))
            texts_user = []
            for block in result_user.contents:
                if isinstance(block, types.TextResourceContents):
                    texts_user.append(block.text)
            print(f"[Read user://{uid}]", " | ".join(texts_user))


if __name__ == "__main__":
    main()