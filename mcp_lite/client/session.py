import json
import sys
from mcp_lite.types import (
    LATEST_PROTOCAL_VERSION,
    ClientCapablities,
    Implemented,
    InitializeRequestParams,
    InitializeRequest,
    JSONRPCRequest,
    JSONRPCResponse,
    jsonrpc_message_adapter,
)


class ClientSession:
    def __init__(self, read_stream, write_stream):
        self.read_stream = read_stream
        self.write_stream = write_stream

        self._req_id = 0

    def send_request(self, req_params: JSONRPCRequest):
        current_req_id = self._req_id
        self._req_id += 1

        d = req_params.model_dump(by_alias=True, mode="json", exclude_none=True)

        jsonrpc_request = JSONRPCRequest(
            jsonrpc="2.0",
            id=current_req_id,
            method=d["method"],
            params=d["params"],
        )

        request_json = jsonrpc_request.model_dump_json(by_alias=True, exclude_none=True)
        print("客户端请求的request", request_json, file=sys.stderr)

        self.write_stream.send(request_json + "\n")

        # response_line = self.read_stream.get()
        # print("服务端响应的response", response_line, file=sys.stderr)

        # response_data = json.loads(response_line)
        # response = jsonrpc_message_adapter.validate_python(response_data)

        # return response

    def initialize(
        self, version=LATEST_PROTOCAL_VERSION, client_capablities=ClientCapablities()
    ):
        params = InitializeRequestParams(
            protocal_version=version,
            capabilities=client_capablities,
            clientInfo=Implemented(name="mcp-client", version="0.1.0").model_dump(
                by_alias=True, exclude_none=True
            ),
        )
        request = InitializeRequest(
            jsonrpc="2.0",
            id=self._req_id,
            method="initialize",
            params=params,
        )

        # 向mcp服务端发送初始化请求
        response = self.send_request(request)

        # 初始化成功后，客户端必须发送一个通知
        """
        {
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        }
        """
