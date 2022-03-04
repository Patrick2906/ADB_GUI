'''
    @Create time:   2022/2/21 14:15
    @Autohr:        Patrick.Yang
    @File:          CmdCheck.py.py
    @Software:      PyCharm
    -*- coding: utf-8 -*-
'''
import os
import subprocess
from apscheduler.schedulers.background import BlockingScheduler
from datetime import datetime
from time import sleep

# adb_path = os.getcwd() + "/ADB_WIN_LIB"
# if os.path.isdir(adb_path):
#     print("path exist")
#     os.environ["PATH"] += os.pathsep + adb_path
#     # os.chdir("D:/tools/telit-tools")
#     cmd = "adb devices"
#     print(cmd)
#     r0 = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     output, error = r0.communicate()
#     print(output.decode())
#     cmd = "adb get-state"
#     r0 = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     output, error = r0.communicate()
#     print(output)
#     print(error)
#
# scheduler = BlockingScheduler()
#
# def func1():
#     time = datetime.now().strftime("%H:%M:%S")
#     cmd_func1 = 'net user'
#     re1 = subprocess.Popen(cmd_func1, shell=False)
#     re1.communicate()
#     print(time)
#     print("func1")
#     sleep(5)
#
# def func2():
#     time = datetime.now().strftime("%H:%M:%S")
#     cmd_func2 = 'net accounts'
#     re1 = subprocess.Popen(cmd_func2, shell=False)
#     re1.communicate()
#     print(time)
#     print("func2")
#
# if __name__ == "__main__":
#     scheduler.add_job(func=func1, trigger="interval", seconds=2)
#     scheduler.add_job(func=func2, trigger="interval", seconds=4)
#     try:
#         scheduler.start()
#     except KeyboardInterrupt:
#         pass


from threading import Thread
import subprocess
from queue import Queue

num_threads = 3
ips = ['127.0.0.1', '172.30.188.130']
q = Queue()


def pingme(i, queue):
    while True:
        ip = queue.get()
        print('Thread %s pinging %s' % (i, ip))

        ret = subprocess.Popen('ping %s' % ip, shell=False,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out = ret.communicate()[0]

        print(out)
        # if ret == 0:
        #     print('%s is alive!' % ip)
        # elif ret == 1:
        #     print('%s is down...' % ip)
        queue.task_done()

    # start num_threads threads

print("start.............")
for i in range(num_threads):
    t = Thread(target=pingme, args=(i, q))
    t.setDaemon(True)
    t.start()

for ip in ips:
    q.put(ip)
print('main thread waiting...')

q.join();
print('Done')





