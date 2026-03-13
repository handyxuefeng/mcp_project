import sys
import os
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
from mcp.server.fastmcp import FastMCP
import asyncio

# AnyUrl是用来进行资源URI的类型校验
from pydantic import AnyUrl


async def run_client():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    server_path = os.path.join(base_dir, "resources_server.py")
    server_params = StdioServerParameters(command="python", args=[server_path])
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 1.初始化对话，完成握手
            await session.initialize()

            # 列出mcp服务的资源
            """
            列出mcp服务的资源
            resource_list = {
                "resources": [
                        {
                        "name": "get_settings",
                        "uri": "config://settings",
                        "description": "",
                        "mimeType": "application/json"
                        }
                    ]
                }
            """
            resource_list = await session.list_resources()
            for resource in resource_list.resources:
                print("resource.uri=", resource.uri)

            # 读取具体的某个资源
            resource_uri = "config://settings"
            result = await session.read_resource(AnyUrl(resource_uri))
            contents = result.contents
            texts_list = []
            for content in contents:
                # print("content.uri=", content.uri)
                # print("content.mimeType=", content.mimeType)
                # print("content.text=", content.text)
                if isinstance(content, types.TextResourceContents):
                    print("content.text=", content.text)
                    texts_list.append(content.text)

            print("texts_list=", "\n".join(texts_list))

            # 读取资源模版
            """
            resource_templte = {
                "resourceTemplates": [
                    {
                    "name": "get_resource",
                    "uriTemplate": "greeting://{name}",
                    "description": "",
                    "mimeType": "text/plain"
                    },
                    {
                    "name": "get_user",
                    "uriTemplate": "user://{user_id}",
                    "description": "",
                    "mimeType": "text/plain"
                    }
                ]
            }
            """
            resource_templte = await session.list_resource_templates()
            for template in resource_templte.resourceTemplates:
                print("template.name=", template.name)
                print("template.uriTemplate=", template.uriTemplate)
                print("template.description=", template.description)
                print("template.mimeType=", template.mimeType)
                print("=" * 20)

            # 传入参数给资源模板，返回具体的资源实例
            """
            @mcp.resource("greeting://{name}", mime_type="text/plain")
            """
            resource_uri = "greeting://Alice"
            result = await session.read_resource(AnyUrl(resource_uri))
            contents = result.contents
            texts_list = []
            for content in contents:
                if isinstance(content, types.TextResourceContents):
                    texts_list.append(content.text)

            print("texts_list=", "\n".join(texts_list))

            # 传入参数给资源模板，返回具体的资源实例
            """
            @mcp.resource("user://{user_id}", mime_type="text/plain")
            
            """
            resource_uri = "user://001"
            result = await session.read_resource(AnyUrl(resource_uri))
            contents = result.contents
            texts_list = []
            for content in contents:
                if isinstance(content, types.TextResourceContents):
                    texts_list.append(content.text)

            print("texts_list=", "\n".join(texts_list))


if __name__ == "__main__":
    asyncio.run(run_client())
