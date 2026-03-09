# 导入 subprocess 和 sys
import subprocess
import sys
from contextlib import contextmanager

"""
python的subprocess 类似nodejs的child_process.spawn,
它会创建一个新的进程来运行指定的命令,并且可以通过管道与该进程进行通信
const { spawn } = require('child_process');
"""


# Popen是边执行边输出
sub_process = subprocess.Popen(
    [
        sys.executable,
        "-c",
        "import time; [ print(f' 子进程消息: {i}') or time.sleep(0.5) for i in range(5) ]",
    ],
    stdout=subprocess.PIPE,
    stdin=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1,
)

for line in sub_process.stdout:
    print(f"收到子进程{sub_process.pid}发来的消息: {line.strip()}\n")

    ## 立即刷新，确保及时显示
    sys.stdout.flush()


# 等待子进程结束
sub_process.wait()
# 打印返回码
print("返回码:", sub_process.returncode)
