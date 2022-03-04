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

MAIN_PAGE_SIZE = (300, 180)


class HomePage(object):
    def __init__(self, master=None):
        self.page = None
        self.root = master
        self.root.geometry('%dx%d' % (300, 180))  # MainPage size
        self.createPage()

    def createPage(self):
        self.page = Frame(self.root)  # create frame while initialize
        self.page.pack()  # pack the components
        Button(self.page, text='ADB Connect', width=12, command=self.AdbConnect).grid(row=1, stick=N, pady=10, column=1)
        Button(self.page, text='Quit', width=12, command=self.page.quit).grid(row=2, stick=N, column=1)

    def AdbConnect(self):
        cmd_valid = False
        adb_cmd = "adb devices"
        # adb_cmd = 'ipconfig'
        out = ''

        try:
            r0 = subprocess.Popen(adb_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out = r0.communicate()[0]   # [0] output message, [1] error message
            cmd_valid = True
        except OSError as err:
            print(err, file=sys.stderr)
            showinfo('Message', err)

        if cmd_valid:
            if out != '':  # check in the list
                print("list found")
                print(out)
            else:
                self.emptyList()

        print('debug')


    def emptyList(self):
        print('device not found')
        showinfo('Message', 'device not found')


root = Tk()
root.title('adb test')

HomePage(root)
root.mainloop()
