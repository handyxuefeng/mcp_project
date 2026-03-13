import sys
from mcp_lite.types import jsonrpc_message_adapter


def server_stdio(handle):
    """
    服务器端标准输入输出流
    """
    while True:
        line = sys.stdin.readline()
        if line is None:
            break
        else:
            line = line.strip()

        try:
            msg = jsonrpc_message_adapter.validate_json(line, by_name=False)
            response = handle(msg)

        except Exception as e:
            print(f"发送数据时出错: {e}", sys.exc_info(), file=sys.stderr)
            pass
