import threading
"""
线程锁
"""
count = 0
loop_num = 1000000


def add(lock):
    global count
    global loop_num
    for i in range(loop_num):
        with lock:
            count += 1


def reduce(lock):
    global count
    for i in range(loop_num):
        with lock:
            count -= 1


lock = threading.Lock()

thread1 = threading.Thread(target=add, args=(lock,))
thread2 = threading.Thread(target=reduce, args=(lock,))
thread1.start()
thread2.start()
thread1.join()
thread2.join()
print(count)
