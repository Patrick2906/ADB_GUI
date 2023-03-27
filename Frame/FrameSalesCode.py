'''
    @Create time:   2022/2/13 9:57
    @Autohr:        Patrick.Yang
    @File:          FrameSalesCode.py
    @Software:      PyCharm
    -*- coding: utf-8 -*-
'''

import json
from Crypto.Cipher import AES
import os, time
import subprocess
import tkinter.ttk
from tkinter.messagebox import showinfo
from tkinter import *
from tkinter.ttk import Combobox
from TSP_Interface.TspIf import updateSalesCode
from apscheduler.schedulers.background import BackgroundScheduler


COMMAND_LOCK_PATTERN = 0xCC
COMMAND_UNLOCK_PATTERN = 0x00


class CmdStatus:
    def __init__(self, master=None):
        self.cmd_executing = False
        self.cmd_lockPattern = COMMAND_UNLOCK_PATTERN
        self.cmd_lastStr = ''


class Frame_SalesCode(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.lastStr = None
        self.idLogcat = ''
        self.last_status = None
        self.lock = False
        self.root = master
        self.createPage()
        self.logcatStatus = CmdStatus()
        self.jobLogcat = None
        self.infoIndex = 0
        self.scheduler = None
        self.r0 = None

    def createPage(self):
        # command and result cheatbox
        self.cheatbox_frame_info = LabelFrame(self.root, text='parameters', width=60, labelanchor=N)
        self.cheatbox_frame_info.grid(row=0, column=6, rowspan=15, columnspan=8)

        # command logging window grouping with other widgets
        self.messages_frame_info = Frame(self.cheatbox_frame_info, bd=3, relief=SUNKEN, padx=5)
        self.messages_frame_info.grid(row=1, column=6, rowspan=15, sticky=E + N + S)

        # Horizontal Scrollbar
        self.xscrollbar_info = Scrollbar(self.messages_frame_info, orient=HORIZONTAL)
        self.xscrollbar_info.grid(row=18, columnspan=8, sticky=E + W)

        # Vertical Scrollbar
        self.yscrollbar_info = Scrollbar(self.messages_frame_info, orient=VERTICAL)
        self.yscrollbar_info.grid(row=0, column=10, rowspan=19, sticky=N + S)

        # list box to store the previous message **row2**
        self.message_list_info = Listbox(self.messages_frame_info, height=26, width=80, bd=0,
                                         yscrollcommand=self.yscrollbar_info.set,
                                         xscrollcommand=self.xscrollbar_info.set)
        self.message_list_info.grid(row=2, column=6, rowspan=16)
        self.xscrollbar_info.config(command=self.message_list_info.xview)
        self.yscrollbar_info.config(command=self.message_list_info.yview)

        # vin lable + entry
        self.vinLabel = Label(self.cheatbox_frame_info, text='vinNo', padx=10, pady=5)
        self.vinLabel.grid(row=1, column=0, columnspan=2)

        self.vinStr = StringVar()
        self.vinStr.set('vin')
        self.vinStr_entry = Entry(self.cheatbox_frame_info, textvariable=self.vinStr, width=35, borderwidth=3)
        self.vinStr_entry.grid(row=1, column=2, columnspan=2, sticky=W)

        self.ownerNameLabel = Label(self.cheatbox_frame_info, text='车主名字', padx=10, pady=5)
        self.ownerNameLabel.grid(row=2, column=0, columnspan=2)

        self.ownerNameStr = StringVar()
        self.ownerNameStr.set('name')
        self.ownerNameStr_entry = Entry(self.cheatbox_frame_info, textvariable=self.ownerNameStr, width=35,
                                        borderwidth=3)
        self.ownerNameStr_entry.grid(row=2, column=2, columnspan=2, sticky=W)

        self.mobileLabel = Label(self.cheatbox_frame_info, text='车主手机', padx=10, pady=5)
        self.mobileLabel.grid(row=3, column=0, columnspan=2)

        self.mobileStr = StringVar()
        self.mobileStr.set('mobile')
        self.mobileStr_entry = Entry(self.cheatbox_frame_info, textvariable=self.mobileStr, width=35, borderwidth=3)
        self.mobileStr_entry.grid(row=3, column=2, columnspan=2, sticky=W)

        self.onwerIdLabel = Label(self.cheatbox_frame_info, text='身份证号码', padx=10, pady=5)
        self.onwerIdLabel.grid(row=4, column=0, columnspan=2)

        self.ownerIdStr = StringVar()
        self.ownerIdStr.set('id')
        self.ownerIdStr_entry = Entry(self.cheatbox_frame_info, textvariable=self.ownerIdStr, width=35, borderwidth=3)
        self.ownerIdStr_entry.grid(row=4, column=2, columnspan=2, sticky=W)

        self.salesCodeLabel = Label(self.cheatbox_frame_info, text='销售编码', padx=10, pady=5)
        self.salesCodeLabel.grid(row=5, column=0, columnspan=2)

        self.salesCodeStr = StringVar()
        self.salesCodeStr.set('code')
        self.salesCodeStr_entry = Entry(self.cheatbox_frame_info, textvariable=self.salesCodeStr, width=35,
                                        borderwidth=3)
        self.salesCodeStr_entry.grid(row=5, column=2, columnspan=2, sticky=W)

        # command button
        self.sendData_frame_info = LabelFrame(self.root, text='salesCode update', width=30, labelanchor=N)
        self.sendData_frame_info.grid(row=23, column=0, rowspan=15, columnspan=8, sticky=W + E + N + S)

        self.sendData_button = Button(self.sendData_frame_info, text="send", padx=50, pady=5,
                                      command=self.send_salesCode)
        self.sendData_button.grid(row=25, column=0, columnspan=4, sticky=W + E + N + S)

        self.clrMsg = Button(self.sendData_frame_info, text="clear window", padx=30, pady=5,
                             command=self.clearMessage)
        self.clrMsg.grid(row=25, column=6, columnspan=2, sticky=W + E + N + S)

        # start scheduler
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

    def pageDestroy(self):
        ret = 0
        if self.logcatStatus.cmd_lockPattern == COMMAND_LOCK_PATTERN:
            self.logcatStatus.cmd_executing = False
            ret = -1
            return ret
        while self.lock:
            time.sleep(1)
        self.cheatbox_frame_info.grid_remove()
        self.message_list_info.grid_remove()

        self.vinLabel.grid_remove()
        self.vinStr_entry.grid_remove()
        self.ownerNameStr_entry.grid_remove()
        self.mobileStr_entry.grid_remove()
        self.ownerIdStr_entry.grid_remove()
        self.salesCodeStr_entry.grid_remove()
        self.sendData_frame_info.grid_remove()
        self.sendData_button.grid_remove()

        if self.scheduler is not None:
            self.scheduler.remove_all_jobs()
            self.scheduler.shutdown()
            self.scheduler = None
        return ret

    def send_salesCode(self):
        # if not self.logcatStatus.cmd_executing:
        #     self.idLogcat = "logcat"
        #     self.jobLogcat = self.scheduler.add_job(self.logcatRecv, trigger='interval', seconds=1, id=self.idLogcat)
        #     # indicator = self.logcatInput_entry.get()
        #     # self.logcatStr.set(indicator)
        # else:
        #     self.updateMessage("###job already started###")
        self.logcatStatus.cmd_lockPattern == COMMAND_LOCK_PATTERN
        vin = self.vinStr_entry.get()
        name = self.ownerNameStr_entry.get()
        mobile = self.mobileStr_entry.get()
        identity = self.ownerIdStr_entry.get()
        salesCode = self.salesCodeStr_entry.get()

        error = 0
        length = 0
        if len(vin) != 17:
            self.updateMessage("### VIN 长度必须为17位 ###")
            error = -1
        for c in vin:
            if str.isalpha(c) or str.isdigit(c):
                # 多余操作
                length += 1
            else:
                self.updateMessage("### 输入vin包含无效字符 ###")
                error = -1
                break
        if name is None or name == "":
            self.updateMessage("### 输入姓名为空 ###")
            error = -1
        if mobile is None or mobile == "":
            self.updateMessage("### 输入手机为空 ###")
            error = -1
        if len(mobile) != 11:
            self.updateMessage("### 手机号码长度必须为11位 ###")
            error = -1
        if len(identity) != 18:
            self.updateMessage("### 身份证长度必须为18位 ###")
            error = -1
        if salesCode is None or salesCode == "":
            self.updateMessage("### 输入销售吗为空 ###")
            error = -1

        if error == 0:
            ret_status, ret_message = updateSalesCode(vin=vin, name=name, mobile=mobile, id=identity, code=salesCode)
            if ret_status == 0:
                self.updateMessage("###  操作成功 ###")
            else:
                self.updateMessage("###  操作失败 ###")
            self.updateMessage(ret_message)
        if error != 0:
            self.updateMessage("### 操作失败 ###")

        self.logcatStatus.cmd_lockPattern == COMMAND_UNLOCK_PATTERN
        return

    def stopLogcat_TbxLog(self):
        # if self.logcatStatus.cmd_executing:
        #     self.logcatStatus.cmd_executing = False
        #
        #     if self.logcatStatus.cmd_lockPattern == COMMAND_LOCK_PATTERN:
        #         self.sendLogcat_stopScript()
        # else:
        #     self.updateMessage("###no job scheduled###")
        self.updateMessage("### stop ###")

    def updateMessage(self, message):
        newlines = message.splitlines(keepends=TRUE)
        print(newlines)
        for line in newlines:
            self.message_list_info.insert(END, line)
        self.message_list_info.see(END)  # show last line when text overflow

    def clearMessage(self):
        self.message_list_info.delete(0, END)
        print("clear messages")
