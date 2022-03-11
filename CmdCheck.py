'''
    @Create time:   2022/2/21 14:15
    @Autohr:        Patrick.Yang
    @File:          CmdCheck.py.py
    @Software:      PyCharm
    -*- coding: utf-8 -*-
'''
import os
import subprocess
import time

from apscheduler.schedulers.background import BlockingScheduler
from datetime import datetime
from time import sleep

'''1  abd shell cmd + blocking scheduler check'''
adb_path = os.getcwd() + "/ADB_WIN_LIB"
if os.path.isdir(adb_path):
    print("path exist")
    os.environ["PATH"] += os.pathsep + adb_path
    # os.chdir("D:/tools/telit-tools")
    cmd = "adb devices"
    print(cmd)
    r0 = subprocess.Popen(cmd, shell=True,
                          stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = r0.communicate()
    print(output.decode("utf-8"))

    cmd = "adb shell"
    r0 = subprocess.Popen(cmd, shell=True,
                          stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cmd = "ls"
    cmds = [
        "ls",
        "ls -l",
        "cd /mnt",
        "ls",
        "exit",
    ]
    cmdTest = "\n".join(cmds) + "\n"
    print(cmdTest)
    output = r0.communicate(cmdTest.encode("utf-8"))
    for item in output:
           print(item.decode("gbk").replace("\r\r", ""))
    """ single command method begin """
    # r0 = subprocess.Popen("adb shell", shell=True, stdin=subprocess.PIPE,  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #
    # r0.stdin.write(('ls\n'.encode("utf-8")))
    # r0.stdin.write(('exit\n'.encode("utf-8")))
    # output, error = r0.communicate()
    # print(output.decode("gbk").replace("\r\r", ""))
    """ single command method end """

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

'''2 thread with subprocess module'''
# from threading import Thread
# import subprocess
# from queue import Queue
#
# num_threads = 3
# ips = ['127.0.0.1', '172.30.188.130']
# q = Queue()
#
#
# def pingme(i, queue):
#     while True:
#         ip = queue.get()
#         print('Thread %s pinging %s' % (i, ip))
#
#         ret = subprocess.Popen('ping %s' % ip, shell=False,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#         out = ret.communicate()[0]
#
#         print(out)
#         # if ret == 0:
#         #     print('%s is alive!' % ip)
#         # elif ret == 1:
#         #     print('%s is down...' % ip)
#         queue.task_done()
#
#     # start num_threads threads
#
# print("start.............")
# for i in range(num_threads):
#     t = Thread(target=pingme, args=(i, q))
#     t.setDaemon(True)
#     t.start()
#
# for ip in ips:
#     q.put(ip)
# print('main thread waiting...')
#
# q.join();
# print('Done')

'''3 decorate function play'''
# import functools
#
#
# def use_logging(func):
#     @functools.wraps(func)
#     def _deco(*args, **kwargs):
#         print("%s is running" % func.__name__)
#         func(*args, **kwargs)
#
#     return _deco
#
#
# @use_logging
# def bar():
#     print('i am bar')
#     print(bar.__name__)
#
#
# bar()

'''4 subprocess non blocking'''
# import subprocess
# import time
#
# p = subprocess.Popen(['ping', 'www.baidu.com'],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# n=None
#
# while n is None:
#     # print('Still pinging')
#     n = p.poll()
#     message = p.stdout.readline().decode("gbk")
#     print(message)
#     time.sleep(1)
#
# print('Not sleeping any longer.  Exited with returncode %d' % p.returncode)

'''5 non-blocking asyncscheduler '''
"""
Demonstrates how to use the asyncio compatible scheduler to schedule a job that executes on 3
second intervals.
"""

# import asyncio
# import os
# from datetime import datetime
#
# from apscheduler.schedulers.background import BackgroundScheduler
#
#
# def tick():
#     print('Tick! The time is: %s' % datetime.now())
#     global _abc
#     _abc += 1
#     print(_abc)
#
#
# if __name__ == '__main__':
#     global _abc
#     _abc = 0
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(tick, 'interval', seconds=1)
#     scheduler.start()
#     print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
#
#     try:
#         # This is here to simulate application activity (which keeps the main thread alive).
#         while True:
#             time.sleep(2)
#             if _abc > 5:
#                 break
#     except (KeyboardInterrupt, SystemExit):
#         # Not strictly necessary if daemonic mode is enabled but should be done if possible
#         scheduler.shutdown()
#     print("shutdown")


'''6 threading tk '''
# from tkinter import *
# import threading
#
#
# def func3(parameter):
#   threading.Thread(target=lambda: Plottingandselect(parameter)).start()
#   #using threading to call  the
#   #another window due to which above error is coming after opening and
#   #closing it 2-3 times
#
# def Plottingandselect(rollno):
#       window=Toplevel()
#       window.title("Marks Distribution")
#       Label(window, text=rollno).grid(row=1,column=2)
#
#       Label(window,text="X axis").grid(row=2,column=1)
#       Label(window, text="Marks",relief=SUNKEN).grid(row=3, column=1)
#       Label(window,text="Y axis").grid(row=2,column=3,padx=22)
#       OPTIONS1 = [
#         "Physics",
#         "Maths",
#         "Chemistry",
#         "Biology",
#       ]
#       list1 = Listbox(window, selectmode="multiple", relief=SUNKEN, font=("Times New Roman", 10))
#   #then user will select above parameters and graphs will be plotted and
#   #it is plotting also perfectly multiple times also , but when i am closing
#  # this plotting window and again I select another roll number and do the
#  #same 2-3 times it gives the following error
#  # mt_debug I am using because I thought that mttkinter will handle it
#
# root = Tk()
# root.geometry('454x567')
# B = Button(root, text='Plot window', command=lambda: func3(1)).grid(row=1, column=2, padx=10, pady=10)
# root.mainloop()
