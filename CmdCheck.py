'''
    @Create time:   2022/2/21 14:15
    @Autohr:        Patrick.Yang
    @File:          CmdCheck.py.py
    @Software:      PyCharm
    -*- coding: utf-8 -*-
'''
import os
import re
import subprocess
import time

from apscheduler.schedulers.background import BlockingScheduler
from datetime import datetime
from time import sleep

'''1  abd shell cmd + blocking scheduler check'''
# adb_path = os.getcwd() + "/ADB_WIN_LIB"
# if os.path.isdir(adb_path):
#     print("path exist")
#     os.environ["PATH"] += os.pathsep + adb_path
#     # os.chdir("D:/tools/telit-tools")
#     cmd = "adb devices"
#     print(cmd)
#     r0 = subprocess.Popen(cmd, shell=True,
#                           stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     output, error = r0.communicate()
#     print(output.decode("utf-8"))
#
#     cmd = "adb shell"
#     r0 = subprocess.Popen(cmd, shell=True,
#                           stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     cmd = "ls"
#     cmds = [
#         "ls",
#         "ls -l",
#         "cd /mnt",
#         "ls",
#         "exit",
#     ]
#     cmdTest = "\n".join(cmds) + "\n"
#     print(cmdTest)
#     output = r0.communicate(cmdTest.encode("utf-8"))
#     for item in output:
#            print(item.decode("gbk").replace("\r\r", ""))
''' single command method begin '''
# r0 = subprocess.Popen("adb shell", shell=True, stdin=subprocess.PIPE,  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#
# r0.stdin.write(('ls\n'.encode("utf-8")))
# r0.stdin.write(('exit\n'.encode("utf-8")))
# output, error = r0.communicate()
# print(output.decode("gbk").replace("\r\r", ""))
''' single command method end '''

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
#     if(message == ''):
#         print("empty")
#     else:
#         print(message)
#     time.sleep(0.2)
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

'''7 to sieve out the device serial number '''

# str_1 = "adbbc1fe3      device"
# str_2 = re.search("device", str_1, re.I)
# str_3 = "list of devices"
# str_4 = re.search("device", str_3, re.I)
# str_5 = []
# str_5.append(str_1)
# str_5.append(str_3)
# print("str_2： %s" % str_2)
# print("str_4： %s" % str_4)
# print("str_2 group: %s" % str_2.group())
# print("str_4 group: %s" % str_4.group())
# print("str_1 without 'device'：%s" % str_1[0:str_2.span()[0]])
# print("str_3 without 'device'：%s" % str_3[0:str_4.span()[0]])
# str_3 = str_1[0:str_2.span()[0]].strip()
#
# devices = []
# for item in str_5:
#     device = None
#     device = re.search("device", item, re.I)
#     if device is not None:
#         if re.search("list", item, re.I) is None:
#             device = item[0:device.span()[0]]
#             devices.append(device.strip())
#
# print("devices list: {}".format(devices))
# print(str_3)

''' 8 to open binary '''
# def OpenAndPrint():
#     f = open(file="E:\\temp\\files\\dk_data", mode="rb")
#     print("result: {}\n".format(f))
#     text = f.read()
#     print(text)
#     f.close()
#
# OpenAndPrint()


'''9 generate QR Code'''
# import qrcode
# import datetime
# import os,getpass
# import json
#
#
# # #输入待转换的字符串
# # qrstr = input("Enter the string to be converted:")
# # print("Input :"+qrstr)
# # #采用默认方式生成二维码
# # qrimg = qrcode.make(qrstr)
#
# qrimg = qrcode.QRCode(
#     error_correction=qrcode.constants.ERROR_CORRECT_M,
#     box_size=10,
#     border=4
# )
# qrimg.add_data("https://api-pre.jf-mall.com/car/activate/v1.0/car/getByVin?vin=QCTESTVIN00000191&iccid=898608071922D0196641")
# qrimg.make(fit=True)
# img = qrimg.make_image(fill_color="blue", back_color="white")
#
# # #获取当前时间,转化成字符串
# timenow = datetime.datetime.now()
# timestr = timenow.strftime("%Y-%m-%d-%H-%M-%S")
# # #生成带时间的二维码图片名,图片保存在桌面上
# qrname = "{1}.png".format(getpass.getuser(), timestr)
# print("Save as :", qrname)
#
# # #保存二维码图片
# with open('test.png', 'wb') as qrname:
#     img.save(qrname)
# # img.show()



#
# # 实例化QRCode生成qr对象
# qr = qrcode.QRCode(
#     version=1,
#     error_correction=qrcode.constants.ERROR_CORRECT_Q,
#     box_size=10,
#     border=4
# )
# # 传入数据
# qr.add_data(data)
#
# qr.make(fit=True)
#
# # 生成二维码
# img = qr.make_image()
#
# # 保存二维码
# # img.save(img_file)
# with open('test.png', 'wb') as qrname:
#     print(qrname)
#     img.save(qrname)
# # 展示二维码


'''10 AES ECB pkcs5padding encryption'''
# import json
# from Crypto.Cipher import AES
# import base64
# import hashlib
#
#
#
# salt = "c87437fa-8bf4-1132-6616-c867479fce00"
# access_key = "dms"
#
# output = \
#     {
#         "code": 0,
#         "message": "请求成功"
#     }
#
# check_body = {
#     "carSales": [
#         {
#             "vinNo": "LNIC4SAH2MA002306",
#             "licensePlate": None,
#             "salesCity": None,
#             "vehicleUse": "1",
#             "carPurchaseField": "单位用车",
#             "operatingUnit": None,
#             "productionDate": "2022-09-22",
#             "saleDate": "2022-09-27",
#             "registrationDate": None,
#             "batteryType": None,
#             "batteryCode": None,00
#             "driveMotorModel": None,
#             "driveMotorCode": "RNIC1M04M23106",
#             "motorPosition": None,
#             "driveMotorSerial": None,
#             "serviceExpirationDate": None,
#             "insuranceExpirationDate": None,
#             "annualReviewDate": None,
#             "invoiceNumber": None,
#             "invoiceDate": None,
#             "invoicePicture": None,
#             "carOwnerName": "轻橙时代（重庆）销售服务有限公司",
#             "carOwnerMobile": "13924250339",
#             "identityNumber": "6220220823556826188",
#             "drivingLicenseBeginTime": None,
#             "drivingLicenseEndTime": None,
#             "drivingLicensePicture": None,
#             "driverLicenseBeginTime": None,
#             "driverLicenseEndTime": None,
#             "driverLicensePicture": None,
#             "salesCode": "NLN15A005008AT2"
#         }
#     ]
# }
#
# class Encryption:
#     def __init__(self, key):
#         self.key = key.encode("utf-8")
#         self.length = AES.block_size
#         self.aes = AES.new(self.key, AES.MODE_ECB)
#         # strip padding bytes
#         self.unpad = lambda data: data[0: -ord(data[-1])]
#
#     def pad(self, text):
#         count = len(text.encode("utf-8"))
#         add = self.length - (count % self.length)
#         entext = text + (chr(add) * add)
#         return entext
#
#     def encrypt(self, encryptData):
#         res = self.aes.encrypt(self.pad(encryptData).encode("utf-8"))
#         # msg = str(base64.b64encode(res), encoding ="utf8")
#         msg = res
#         return msg
#
#     def decrypt(self, decryptData):
#         # res = base64.decodebytes(decryptData.encode("utf-8"))
#         res = decryptData
#         msg = self.aes.decrypt(res).decode("utf-8")
#         return self.unpad(msg)
#
#
# '''sample begin '''
# # eg = Encryption("xxxxaaaabbbbcccc")
# # data = {"hotelCode": "330122892X", "realName": "张四五", "sex": "1"}
# # result = eg.encrypt(str(data))
# # print(result)
# # print(eg.decrypt(result))
# '''sample end '''
#
# time_stamp = "1669964210181"
# nonce = "KKnz0EI1EGMZGy3QssKeDQQ19JULM45n"
# val_joint = salt + time_stamp + nonce + access_key
# print("value joint: {}".format(val_joint))
#
# md5_text = hashlib.md5()
# md5_text.update(val_joint.encode("utf-8"))
# md5_hex = md5_text.hexdigest().upper()
# print("md5 result:{}".format(md5_hex))
# secret_key = md5_hex[0:16]
# print("secret key:{}".format(secret_key))
#
# ag = Encryption(secret_key)
# respond_dict = {"code": 0, "message": "请求成功"}
# respond = "{\"code\":0,\"message\":\"请求成功\"}"
# # data = json.dumps(output, indent=0, ensure_ascii=False)
#
# result = ag.encrypt(respond)
# print("result utf-8:{}".format(result))
# print("result hex:{}".format(result.hex().upper()))
# print(ag.decrypt(result))
# # print("{\"repairPhone\":\"18547854787\",\"customPhone\":\"12365478965\",\"captchav\":\"58m7\"}")
# # encrypt_temp = "27DD39BAD8CAE979EB9675B464E0BCDF3A578F6CCFCBA945FBDA6FD9FF4C12CA9EDCDA3A1EA40FA64A7904701162A3F71443E73D120A761C663CEF99265BBB228BF923361E13EFA5CEFD5BF7D02BB548";
# # byte_encrypt_temp = bytes.fromhex(encrypt_temp)
# # print(ag.decrypt(byte_encrypt_temp))
#
# result = ag.encrypt(json.dumps(respond_dict, separators=(',', ':'), ensure_ascii=False))
# print("result_dict utf-8:{}".format(result))
# print("result_dict hex:{}".format(result.hex().upper()))
# result = ag.encrypt(json.dumps(check_body, separators=(',', ':'), ensure_ascii=False))
# print(json.dumps(check_body, separators=(',', ':'), ensure_ascii=False))
# print("body_dict utf-8:{}".format(result))
# print("body_dict hex:{}".format(result.hex().upper()))
# print("body_dict hex:{}".format(result.hex().upper().encode("utf-8")))
#
# print(json.loads(respond))

text_str = "0:12:20:5787 Rx 1 343 s 8 CD 25 48 00 38 70 AC 62"
Array_a = text_str.split(" ")
print("array:{}".format(Array_a))
print("type:{}".format(type(Array_a)))
