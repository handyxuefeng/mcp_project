# 导入 Flask 和请求/响应相关功能
from flask import Flask, request, jsonify

# 创建 Flask 应用实例
app = Flask(__name__)


# 定义两个简单的业务方法，供 JSON-RPC 调用
def add(a, b):
    """加法"""
    return a + b


def subtract(a, b):
    """减法"""
    return a - b


# 方法名到函数的映射，方便根据 method 字符串找到对应函数
METHODS = {
    "add": add,
    "subtract": subtract,
}


# 定义 /rpc 路由，只接受 POST 请求
@app.route("/rpc", methods=["POST"])
def handle_rpc():
    # 解析请求体中的 JSON，得到字典
    req = request.get_json(silent=True)

    # 如果解析失败或没有 jsonrpc 字段，返回无效请求错误
    if req is None or req.get("jsonrpc") != "2.0":
        return jsonify(
            {
                "jsonrpc": "2.0",
                "error": {"code": -32600, "message": "Invalid Request"},
                "id": req.get("id") if req else None,
            }
        )

    # 取出方法名、参数和请求 id
    method = req.get("method")
    params = req.get("params") or []
    req_id = req.get("id")

    # 如果方法不存在，返回方法未找到错误
    if method not in METHODS:
        return jsonify(
            {
                "jsonrpc": "2.0",
                "error": {"code": -32601, "message": "Method not found"},
                "id": req_id,
            }
        )

    # 尝试执行方法
    try:
        if isinstance(params, list):
            # 参数是数组，按位置传参：add(3, 5)
            result = METHODS[method](*params)
        else:
            # 参数是对象，按名称传参：add(a=3, b=5)
            result = METHODS[method](**params)
    except Exception as e:
        # 执行出错，返回内部错误
        return jsonify(
            {
                "jsonrpc": "2.0",
                "error": {"code": -32603, "message": str(e)},
                "id": req_id,
            }
        )

    # 成功，返回结果
    return jsonify(
        {
            "jsonrpc": "2.0",
            "result": result,
            "id": req_id,
        }
    )


# 程序入口：直接运行此文件时启动服务器
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000)
