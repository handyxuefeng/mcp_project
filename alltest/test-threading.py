import threading

import time

from queue import Queue


# 定义生产者函数，参数q是共享的队列
def producer(q):

    for i in range(5):

        item = f"item-{i}"

        print(f"生产者生产了{item}")

        q.put(item)  # 将生产的物品放入队列

        time.sleep(1)  # 模拟生产时间

    # 放入 None 作为结束信号，告诉消费者可以退出了
    q.put(None)


def consumer(q):

    while True:

        item = q.get()  # 从队列中获取物品

        if item is None:  # 如果获取到 None，说明生产者已经结束了
            break

        print(f"消费者消费了{item}")

        time.sleep(2)  # 模拟消费时间


q = Queue()  # 创建一个共享的队列

# 创建生产者线程，target 是函数名，args 是传给函数的参数（元组）
t1 = threading.Thread(target=producer, args=(q,))

# 创建消费者线程,target 是函数名，args 是传给函数的参数（元组）
t2 = threading.Thread(target=consumer, args=(q,))


t1.start()  # 启动生产者线程
t2.start()  # 启动消费者线程


t1.join()  # 主线程等待生产者线程结束
t2.join()  # 主线程等待消费者线程结束

print("生产者和消费者都结束了")
