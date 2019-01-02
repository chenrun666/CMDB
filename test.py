import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def task(i):
    time.sleep(1)
    print(i)


p = ThreadPoolExecutor(10)  # 最多开10个线程
for row in range(100):
    p.submit(task, row)
