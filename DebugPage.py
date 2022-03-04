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





