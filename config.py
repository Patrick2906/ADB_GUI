'''
    @Create time:   2022/3/10 14:29
    @Autohr:        Patrick.Yang
    @File:          config.py.py
    @Software:      PyCharm
    -*- coding: utf-8 -*-
'''

# Symbolic for Page config
PAGE_STATUS_ERR = -1  # error status
PAGE_STATUS_INIT = 0  # initial state(normal state)
PAGE_STATUS_SWITCHPAGE = 1  # indicate to switch to other page

PAGE_ID_HOME = 1  # home page when start
PAGE_ID_DEBUG = 2  # debug page after connected
PAGE_ID_API = 3 # API page which enter directly

ADB_PUSH = "adb push " # reserve space

ADB_SHELL_LOGCAT_CMD2 = 'adb shell "/custapp/bin/logcat -v time -b main | grep '
ADB_SHELL_LOGCAT_CMD1 = "adb shell tail -f /custapp/mnt/log/ota/tbox-updateagent.log"
ADB_SHELL_LOGCAT_CMD3 = 'adb shell '