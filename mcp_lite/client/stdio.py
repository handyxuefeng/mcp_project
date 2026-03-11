from pydantic import BaseModel, Field
from pathlib import Path
from queue import Queue
import threading

import subprocess
import sys
import os
from contextlib import asynccontextmanager, contextmanager

# 根据平台（Windows或非Windows）定义要继承的环境变量名字列表
_ENV_VARS = (
    # 如果是Windows系统，则使用以下环境变量名
    [
        "APPDATA",
        "HOMEDRIVE",
        "HOMEPATH",
        "LOCALAPPDATA",
        "PATH",
        "PATHEXT",
        "PROCESSOR_ARCHITECTURE",
        "SYSTEMDRIVE",
        "SYSTEMROOT",
        "TEMP",
        "USERNAME",
        "USERPROFILE",
    ]
    # 否则（非Windows，如Linux/Mac），使用下面的环境变量名
    if sys.platform == "win32"
    else ["HOME", "LOGNAME", "PATH", "SHELL", "TERM", "USER"]
)


class StdioServerParameters(BaseModel):
    """
    command='python'
    args=['/Users/hanxuefeng/project/mcp_project/1.mcp.py', 'serve']
    env=None
    cwd=None
    encoding='utf-8'
    encoding_error_handler='strict'
    """

    command: str
    args: list[str] = Field(default_factory=list)
    env: dict[str, str] | None = None
    cwd: str | None | Path = None
    encoding: str = "utf-8"
    encoding_error_handler: str = "strict"


# 定义 _env() 函数，返回过滤后的环境变量字典
def _env():
    # 遍历_ENV_VARS，只收集值非空且不以"()"开头的变量
    return {
        k: v for k in _ENV_VARS if (v := os.environ.get(k)) and not v.startswith("()")
    }


# 定义 stdio_client 上下文管理器函数，用于创建子进程并与之通信
@contextmanager
def stdio_client(server_params, errlog=sys.stderr):
    # 创建一个子进程来运行服务器,并重定向到 stdin 和 stdout

    read_q = Queue()  # 创建一个队列来存储子进程的输出

    write_q = Queue()  # 创建一个队列来存储要发送给子进程的输入

    # 在 Windows 上,如果 command 是一个 Python 脚本,我们需要使用 sys.executable 来确保使用当前的 Python 解释器
    cmd = (
        sys.executable
        if sys.platform == "win32" and server_params.command == "python"
        else server_params.command
    )

    env = {
        **_env(),  # 获取当前环境变量中需要继承的变量
        "PYTHONIOENCODING": "utf-8",  # 设置 Python 输入输出编码
        **(server_params.env or {}),  # 将用户提供的环境变量覆盖默认环境
    }

    sub_process = subprocess.Popen(
        [cmd] + server_params.args,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=errlog,
        env=env,
        cwd=server_params.cwd,
        text=True,
        encoding=server_params.encoding,
        errors=server_params.encoding_error_handler,
    )

    # 定义从子进程stdout读取数据的函数
    def read_from_process():
        while True:
            line = sub_process.stdout.readline()
            if line == "":
                break
            line = line.strip()
            if line:
                read_q.put(line)

    # 定义主进程向子进程stdin写入数据的函数
    def write_to_process():
        while (m := write_q.get()) is not None:

            # 向子进程stdin写入数据
            sub_process.stdin.write(m)
            sub_process.stdin.flush()

    # 创建两个线程分别处理读取和写入操作
    rt = threading.Thread(target=read_from_process, daemon=True)
    wt = threading.Thread(target=write_to_process, daemon=True)

    # 启动线程
    rt.start()
    wt.start()

    # 定义读写流类，提供 get 和 send 方法供调用者使用
    class ReadStream:
        def get(self):

            # 从读取队列中获取数据并返回
            return read_q.get()

    class WriteStream:

        # 定义 send 方法，用于向子进程发送数据
        def send(self, data):
            # 将数据放入写入队列中，等待写入线程处理
            write_q.put(data)

    try:
        yield ReadStream(), WriteStream()  # 将读写流对象作为上下文管理器的结果返回给调用者

    finally:
        write_q.put(None)  # 向写入队列中放入 None 作为结束信号，告诉写入线程可以退出了
        rt.join(timeout=3)  # 等待读取线程结束
        wt.join(timeout=2)  # 等待写入线程结束

        # 关闭子进程的读写管道
        sub_process.stdin.close()
        sub_process.stdout.close()

        sub_process.wait(2)

        # 如果子进程没有正常退出，则强制杀死子进程并等待其退出
        if sub_process.poll() is None:
            sub_process.kill()
            sub_process.wait()


"""
创建子进程时 stdin,stdout 和 stderr 都被重定向到管道,我们可以通过 process.stdin, 
process.stdout 和 process.stderr 来与子进程进行通信

    
"""
