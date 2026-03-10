# 导入 Queue 类
from queue import Queue

# 创建一个无限大小的队列（maxsize 默认为 0，表示不限制）
q = Queue(3)

# 创建一个最多能放 10 个元素的队列，超过会阻塞
q_limited = Queue(maxsize=10)

q.put(1)  # 将元素 1 放入队列
q.put(2)  # 将元素 2 放入队列
q.put(3)  # 将元素 3 放入队列
# q.put(4)  # 将元素 4 放入队列

print(q.get())  # 从队列中取出一个元素，输出 1
print(q.get())  # 输出 2
print(q.get())  # 输出 3


print(q.get())  # 从队列中取出一个元素，输出 4
