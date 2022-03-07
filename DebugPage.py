'''
    @Create time:   2022/2/28 14:53
    @Autohr:        Patrick.Yang
    @File:          DebugPage.py.py
    @Software:      PyCharm
    -*- coding: utf-8 -*-
'''

'''
    
    |------------|------------|------------|------------|------------| 
    |  info      |  OTA log   |  logcat    |  V-spy api |  hmconfig  |
    |------------|------------|------------|------------|------------| 
@info:
    information in the TBOX-> excelfore version, VIN ,APN, SW version
    
@OTA log:
    show result dmclient.log
    show ota status in tboxUpdageAgent.log
    
@logcat:
    logging of OTA status and pull out in windows system
    
@V-spy api:
    send diagnostic command(s) to fulfill TBOX update case
    
@hmconfig:
    find "hmconfi.ini" file
    create gho folder and copy "hmconfi.ini" file for TSP connect interval modify
    clean cache and to delete old certifications
    
'''

import subprocess
from tkinter.messagebox import showinfo
from tkinter import *
from apscheduler.schedulers.background import BlockingScheduler
from datetime import datetime
from Frame.FrameOtaLog import *
from Frame.FrameSpecialCmd import *
import functools

DEBUG_PAGES = 5  # config the total pages
OTALOG_PAGE_ID = 0
SPECIALCOMMAND_PAGE_ID = 1


class DebugPage(object):
    def __init__(self, master=None):
        self.root = master
        # self.root.geometry('%dx%d' % (800, 600))
        self.createPage()


    def createPage(self):
        self.otaLogPage = Frame_OtaLog(self.root)
        self.specialCmdPage = Frame_SpecialCmd(self.root)

        self.specCmdPageActive()  # default page
        menubar = Menu(self.root)
        menubar.add_command(label="special command", command=self.specCmdPageActive)
        menubar.add_command(label="ota log", command=self.otaLogPageActive)

        self.root["menu"] = menubar  # set menu bar

    def pageActive(func):
        @functools.wraps(func)
        def deco(self, *args, **kwargs):
            self.specialCmdPage.pageDestroy()
            self.otaLogPage.pageDestroy()
            func(self, *args, **kwargs)
        return deco

    @pageActive
    def otaLogPageActive(self):
        self.otaLogPage.createPage()

    @pageActive
    def specCmdPageActive(self):
        self.specialCmdPage.createPage()

    def pagePack(self, pageId):
        self.last_page_id = pageId



# root = Tk()
# root.title('debug page')
#
# DebugPage(root)
# root.mainloop()
