import threading
"""
在一个线程中，我们在部分代码中使用了锁lock.acquire()还没有释放锁时，
调用了另一个方法，方法中又使用了锁，这样如果使用同一把普通的锁很容易出现死锁。
这时我们可以使用Rlock，但是要注意使用了几次Rlock.acquire()，就必须使用几次Rlock.release()
链接：https://www.jianshu.com/p/191be5f10a94
"""
count = 0
loop_num = 1000000


def dosomething(rlock):
    rlock.acquire()
    # do something
    rlock.release()


def add(rlock):
    global count
    for i in range(loop_num):
        rlock.acquire()
        count += 1
        dosomething(rlock)
        rlock.release()


def reduce(rlock):
    global count
    for i in range(loop_num):
        rlock.acquire()
        count -= 1
        dosomething(rlock)
        rlock.release()


# 造成死锁,程序一直运行
# rlock = threading.Lock()
rlock = threading.RLock()
thread1 = threading.Thread(target=add, args=(rlock,))
thread2 = threading.Thread(target=reduce, args=(rlock,))
thread1.start()
thread2.start()
thread1.join()
thread2.join()
print(count)
