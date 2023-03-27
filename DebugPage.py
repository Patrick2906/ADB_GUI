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
from datetime import datetime
from Frame.FrameOtaLog import *
from Frame.FrameSpecialCmd import *
import functools
import os
from apscheduler.schedulers.background import BackgroundScheduler
from config import *

DEBUG_PAGES = 5  # config the total pages
OTALOG_PAGE_ID = 0
SPECIALCOMMAND_PAGE_ID = 1

SCHED_BACKGROUND_MSG = "background scheduler notify"

class DebugPage(object):
    def __init__(self, master=None):
        self.root = master
        self.status = 0
        self.newPage = PAGE_ID_DEBUG
        self.menubar = None
        self.p0 = None  # process for connection check
        print("status: {}".format(self.status))
        # self.root.geometry('%dx%d' % (800, 600))

        # to create page default
        self.createPage()

        # start scheduler
        self.scheduler = BackgroundScheduler()
        self.jobTestPresent = self.scheduler.add_job(self.tick, trigger='interval', seconds=1)
        self.scheduler.start()


    def createPage(self):
        """ insert the pages in requirement """
        self.otaLogPage = Frame_OtaLog(self.root)
        self.specialCmdPage = Frame_SpecialCmd(self.root)

        self.specCmdPageActive()  # default page

        # add menubar
        self.menubar = Menu(self.root)
        self.menubar.add_command(label="special_command", command=self.specCmdPageActive)
        self.menubar.add_command(label="ota_log", command=self.otaLogPageActive)

        self.root["menu"] = self.menubar  # set menu bar

    # to test the background scheduler
    def tick(self):
        print("%s , time now: %s" % (SCHED_BACKGROUND_MSG, datetime.now()))
        self.jobTestPresent.pause()
        cmd = "adb get-state"
        output, error = subprocess.getstatusoutput(cmd)
        if output != 0:
            print("{}, going to disconnect".format(error))
            self.adbDisconnected()
        self.jobTestPresent.resume()

    def pageActive(func):
        @functools.wraps(func)
        def deco(self, *args, **kwargs):
            # destroy pages as created

            ret = self.specialCmdPage.pageDestroy()
            if ret != 0:
                showinfo("message", "specialCmdPage still running")
                return
            ret = self.otaLogPage.pageDestroy()
            if ret != 0:
                showinfo("message", "otaLogPage still running")
                return
            func(self, *args, **kwargs)

        return deco

    @pageActive
    def otaLogPageActive(self):
        self.otaLogPage.createPage()

    @pageActive
    def specCmdPageActive(self):
        self.specialCmdPage.createPage()

    @pageActive
    def adbDisconnected(self):
        self.cnt = 0
        self.scheduler.remove_all_jobs()    # remove current, prevent jump to next cycle
        self.menubar.destroy()  # destroy menu bar
        print("scheduler stop")
        abc = showinfo('Message', 'device disconnected')
        self.status = PAGE_STATUS_SWITCHPAGE
        self.newPage = PAGE_ID_HOME
        self.root.quit()
        print("quit root")

    def pagePack(self, frameId):
        self.last_frame_id = frameId

# root = Tk()
# root.title('adb test')
#
# HomePage(root)
# root.mainloop()
