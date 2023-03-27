'''
    @Create time:   2023/2/14 14:53
    @Autohr:        Patrick.Yang
    @File:          ApiPage.py
    @Software:      PyCharm
    -*- coding: utf-8 -*-
'''

'''

    |------------|------------|------------|------------|
    |  salesCode |  QR code   |  reserved  |  reserved  |  
    |------------|------------|------------|------------|
@salesCode
add sales code

@QR code 
car activate QR code

'''
import subprocess
from tkinter.messagebox import showinfo
from tkinter import *
from datetime import datetime
from Frame.FrameOtaLog import *
from Frame.FrameSalesCode import *
from Frame.FrameQrCode import *
import functools
import os
from apscheduler.schedulers.background import BackgroundScheduler
from config import *

TATOL_PAGES = 2  # config the total pages
SALESCODE_PAGE_ID = 0
QRCODE_PAGE_ID = 1

SCHED_BACKGROUND_MSG = "background scheduler notify"


class ApiPage(object):
    def __init__(self, master=None):
        self.salesCodePage = None
        self.qrCodePage = None
        self.root = master
        self.status = 0
        self.newPage = PAGE_ID_API
        self.menubar = None
        self.p0 = None  # process for connection check

        # self.root.geometry('%dx%d' % (800, 600))

        # to create page default
        self.createPage()

        # start scheduler
        self.scheduler = BackgroundScheduler()
        self.jobTestPresent = self.scheduler.add_job(self.tick, trigger='interval', seconds=2)
        self.scheduler.start()

    def createPage(self):
        """ insert the pages in requirement """
        self.salesCodePage = Frame_SalesCode(self.root)
        self.qrCodePage = Frame_QrCode(self.root)

        self.salesCodePageActive()  # default page


        # add menubar
        self.menubar = Menu(self.root)
        self.menubar.add_command(label="sales code", command=self.salesCodePageActive)
        self.menubar.add_command(label="qr code", command=self.qrCodePageActive)

        self.root["menu"] = self.menubar  # set menu bar

    # to test the background scheduler
    def tick(self):
        print("%s , time now: %s" % (SCHED_BACKGROUND_MSG, datetime.now()))


    def pageActive(func):
        @functools.wraps(func)
        def deco(self, *args, **kwargs):
            # destroy pages as created

            ret = self.salesCodePage.pageDestroy()
            if ret != 0:
                showinfo("message", "命令没有执行完毕,无法切换页面")
                return
            ret = self.qrCodePage.pageDestroy()
            if ret != 0:
                showinfo("message", "命令没有执行完毕,无法切换页面")
                return
            func(self, *args, **kwargs)

        return deco

    @pageActive
    def salesCodePageActive(self):
        self.salesCodePage.createPage()

    @pageActive
    def qrCodePageActive(self):
        self.qrCodePage.createPage()


    @pageActive
    def page(self):
        self.cnt = 0
        self.scheduler.remove_all_jobs()  # remove current, prevent jump to next cycle
        self.menubar.destroy()  # destroy menu bar
        print("scheduler stop")
        abc = showinfo('Message', 'unexpected error happened')
        self.status = PAGE_STATUS_SWITCHPAGE
        self.newPage = PAGE_ID_HOME
        self.root.quit()
        print("quit root")

    def pagePack(self, frameId):
        self.last_frame_id = frameId


