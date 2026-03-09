from contextlib import contextmanager


@contextmanager
def my_context():
    # yield 之前的代码：进入 with 时执行（相当于 __enter__）
    print("进入 with，做准备工作")
    try:
        # yield 后面的值会赋给 as 后面的变量
        yield "你好"
        # yield 之后的代码：退出 with 时执行（相当于 __exit__）
    finally:
        # 用 finally 确保退出时一定会执行清理
        print("退出 with，做清理工作")


if __name__ == "__main__":
    with my_context() as value:
        print(f"在 with 块内，value 的值是: {value}")
