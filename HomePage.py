'''
    @Create time:   2022/2/26 16:06
    @Autohr:        Patrick.Yang
    @File:          HomePage.py.py
    @Software:      PyCharm
    -*- coding: utf-8 -*-
'''

'''
    -------------
    | ADB debug |       -> to use adb command to enable adb port
    -------------
    |   Quit    |       -> exit GUI
    -------------   

'''
import subprocess
from tkinter.messagebox import showinfo
from tkinter import *
import sys
from config import *
import os
import re

ADB_PATH = os.getcwd() + "/ADB_WIN_LIB"

MAIN_PAGE_SIZE = (300, 180)


class HomePage(object):
    def __init__(self, master=None):
        self.page = None
        self.status = 0
        self.root = master
        # self.root.geometry('%dx%d' % (300, 180))  # MainPage size
        self.createPage()

    def createPage(self):
        self.page = Frame(self.root)  # create frame while initialize
        self.page.grid(padx=100, pady=60, sticky=W + E + N + S)
        # self.page.pack()  # pack the components

        self.connectButton = Button(self.page, text='ADB Connect', width=12, command=self.adbConnect)
        self.connectButton.grid(stick=N, pady=10)

        self.quitButton = Button(self.page, text='Quit', width=12, command=self.homePageRun)
        self.quitButton.grid(stick=N, pady=10)

    def adbConnect(self):
        if os.path.isdir(ADB_PATH):
            print("path exist")
            os.environ["PATH"] += os.pathsep + ADB_PATH
            # os.chdir("D:/tools/telit-tools")
            cmd = "adb devices"
            print(cmd)
            r0 = subprocess.Popen(cmd, shell=True,
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = r0.communicate()
            print(output.decode("utf-8"))

            cmd_valid = False
            adb_cmd = "adb devices"
            out = ""

            try:
                r0 = subprocess.Popen(adb_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out = r0.communicate()[0]  # [0] output message, [1] error message
                cmd_valid = True
            except OSError as err:
                print(err, file=sys.stderr)
                showinfo('Message', err)

            if cmd_valid:
                out = out.decode("gbk").split("\r\n")   # todo: utf-8? short term solution with Chinese windows system
                """  answer will be probably below:
                ## start initialize ##
                List of devices attached
                1b6b1fc4	device
                """
                device_name = getAdbDevices(out)
                if device_name:  # check in the list
                    print("list found:")
                    for x in device_name:
                        print(x)
                    self.connectButton.grid_remove()
                    self.quitButton.grid_remove()
                    self.page.grid_remove()
                    self.page.quit()
                    self.status = PAGE_STATUS_SWITCHPAGE  # exit page number 1
                else:
                    self.emptyList()

        else:
            showinfo('Message', 'Path invalid')

    def emptyList(self):
        print('device not found')
        showinfo('Message', 'device not found')

    def homePageRun(self):
        self.page.quit()
        self.status = PAGE_STATUS_INIT
        return self.status


def getAdbDevices(list):
    devices = []
    for item in list:
        device = None
        device = re.search("device", item, re.I)
        if device is not None:
            if re.search("list", item, re.I) is None:
                device = item[0:device.span()[0]]
                devices.append(device.strip())

    return devices


# root = Tk()
# root.title('adb test')
#
# HomePage(root)
# root.mainloop()
