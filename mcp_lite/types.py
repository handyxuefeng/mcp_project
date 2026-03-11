from tkinter import N
from pydantic import BaseModel, ConfigDict, Field, TypeAdapter

# to_camel 是把蛇形命名转换成驼峰命名
from pydantic.alias_generators import to_camel
from typing import Any, Literal

"""
{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2025-11-25",
        "capabilities": {
            "roots": {"listChanged": true},
            "sampling": {},
            "elicitation": {"form": {}, "url": {}},
        },
        "clientInfo": {
            "name": "ExampleClient",
            "title": "Example Client",
            "version": "1.0.0",
        },
    },
}
"""
RequestID = int | str
LATEST_PROTOCAL_VERSION = "2026-03-10"


class MCPModel(BaseModel):
    # 这里的定义是表示把所有的字段都转换成驼峰命名
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


# 定义客户端实现的信息的结构体
class Implemented(MCPModel):
    name: str = ""
    version: str = ""
    title: str | None = ""
    description: str | None = None


class ClientCapablities(MCPModel):

    # 客户端支持的实验性功能
    experimental: dict[str, dict[str, Any]] | None = None


class JSONRPCRequest(BaseModel):

    # jsonrpc协议的版本号
    jsonrpc: Literal["2.0"] = "2.0"

    # 请求的id
    id: RequestID

    # 要请求服务端的那个方法
    method: str = ""

    params: dict[str, Any] | None = None


class JSONRPCNoticefication(BaseModel):

    # jsonrpc协议的版本号
    jsonrpc: Literal["2.0"] = "2.0"

    # 要请求服务端的那个方法
    method: str = ""

    params: dict[str, Any] | None = None


class JSONRPCResponse(BaseModel):

    # jsonrpc协议的版本号
    jsonrpc: Literal["2.0"] = "2.0"
    id: RequestID = None
    result: dict[str, Any] | None = None


class Errordata(BaseModel):
    code: int = 0

    message: str = ""

    data: Any = None


class JSONRPCError(BaseModel):

    # jsonrpc协议的版本号
    jsonrpc: Literal["2.0"] = "2.0"
    id: RequestID | None = None
    error: Errordata | None = None


# 定义所有JSONRPc的联合类型

JSONMessage = JSONRPCRequest | JSONRPCNoticefication | JSONRPCResponse | JSONRPCError


# 定义jsonrpc消息类型适配器，用于类型自动推断和校验
jsonrpc_message_adapter = TypeAdapter(JSONMessage)


class InitializeRequestParams(MCPModel):
    protocal_version: str = LATEST_PROTOCAL_VERSION
    capabilities: ClientCapablities = ClientCapablities()
    clientInfo: dict[str, Any] | None = None


class InitializeRequest(MCPModel, JSONRPCRequest):
    id: RequestID = None
    jsonrpc: Literal["2.0"] = "2.0"
    method: Literal["initialize"] = "initialize"
    params: InitializeRequestParams = None
