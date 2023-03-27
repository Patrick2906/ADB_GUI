'''
    @Create time:   2022/2/13 9:57
    @Autohr:        Patrick.Yang
    @File:          FrameSalesCode.py
    @Software:      PyCharm
    -*- coding: utf-8 -*-
'''

import json
import requests
import os, time
import subprocess
import tkinter.ttk
from tkinter.messagebox import showinfo
from tkinter import *
import sys
from apscheduler.schedulers.background import BackgroundScheduler
import qrcode

COMMAND_LOCK_PATTERN = 0xCC
COMMAND_UNLOCK_PATTERN = 0x00
url_getCarVin = "https://api-pre.jf-mall.com/car/activate/v1.0/car/getByVin"

params = {
    "vin": "QCTESTVIN00000191",
    "iccid": "898608071922D0196640"
}

class CmdStatus:
    def __init__(self, master=None):
        self.cmd_executing = False
        self.cmd_lockPattern = COMMAND_UNLOCK_PATTERN
        self.cmd_lastStr = ''


class Frame_QrCode(Frame):
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
        self.input_frame_info = LabelFrame(self.root, text='parameters', width=60, labelanchor=N)
        self.input_frame_info.grid(row=0, column=6, rowspan=15, columnspan=8)

        # command logging window grouping with other widgets
        self.param_frame_info = Frame(self.input_frame_info, bd=3, relief=SUNKEN, padx=5)
        self.param_frame_info.grid(row=1, column=6, rowspan=15, sticky=E + N + S)

        # vin lable + entry
        self.vinLabel = Label(self.input_frame_info, text='vinNo', padx=10, pady=5)
        self.vinLabel.grid(row=1, column=0, columnspan=2)

        self.vinStr = StringVar()
        self.vinStr.set('vin')
        self.vinStr_entry = Entry(self.input_frame_info, textvariable=self.vinStr, width=35, borderwidth=3)
        self.vinStr_entry.grid(row=1, column=2, columnspan=2, sticky=W)

        self.iccidLabel = Label(self.input_frame_info, text='ICCID', padx=10, pady=5)
        self.iccidLabel.grid(row=2, column=0, columnspan=2)

        self.iccidStr = StringVar()
        self.iccidStr.set('iccid')
        self.iccidStr_entry = Entry(self.input_frame_info, textvariable=self.iccidStr, width=35,
                                        borderwidth=3)
        self.iccidStr_entry.grid(row=2, column=2, columnspan=2, sticky=W)


        # command button
        self.cmd_frame_info = LabelFrame(self.root, text='QR code', width=30, labelanchor=N)
        self.cmd_frame_info.grid(row=23, column=0, rowspan=15, columnspan=8, sticky=W + E + N + S)

        self.generate_button = Button(self.cmd_frame_info, text="生成", padx=50, pady=5,
                                      command=self.generate_QrCode)
        self.generate_button.grid(row=25, column=0, columnspan=4, sticky=W + E + N + S)

        self.active_button = Button(self.cmd_frame_info, text="激活车辆", padx=30, pady=5,
                                      command=self.active_car)
        self.active_button.grid(row=25, column=6, columnspan=4, sticky=W + E + N + S)

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
        self.input_frame_info.grid_remove()
        self.param_frame_info.grid_remove()

        self.vinLabel.grid_remove()
        self.vinStr_entry.grid_remove()
        self.iccidLabel.grid_remove()
        self.iccidStr_entry.grid_remove()

        self.cmd_frame_info.grid_remove()
        self.generate_button.grid_remove()
        self.active_button.grid_remove()

        if self.scheduler is not None:
            self.scheduler.remove_all_jobs()
            self.scheduler.shutdown()
            self.scheduler = None
        return ret

    def generate_QrCode(self):
        # if not self.logcatStatus.cmd_executing:
        #     self.dLogcat = "logcat"
        #     self.jobLogcat = self.scheduler.add_job(self.logcatRecv, trigger='interval', seconds=1, id=self.idLogcat)
        #     # indicator = self.logcatInput_entry.get()
        #     # self.logcatStr.set(indicator)
        # else:
        #     self.updateMessage("###job already started###")
        self.logcatStatus.cmd_lockPattern == COMMAND_LOCK_PATTERN
        vin = self.vinStr_entry.get()
        iccid = self.iccidStr_entry.get()

        params["vin"] = vin
        params["iccid"] = iccid

        try:
            respond = requests.get(url=url_getCarVin, params=params)
            status = respond.status_code
            data = respond.json()
            print("respond:{}".format(data))
            if data["code"] == 1:
                if "data" in data:
                    # print(data["data"]["uid"])
                    print(respond.url)
                    showinfo('Message', data["message"])
                    qr_img = qrcode.QRCode(
                        version=None,
                        error_correction=qrcode.constants.ERROR_CORRECT_M,
                        box_size=15,
                        border=8
                    )
                    qr_img.add_data(respond.url)
                    img = qr_img.make_image(fill_color="blue", back_color="white")
                    img.show()
                else:
                    showinfo('Message', "车辆不存在或未激活")
            else:
                showinfo('Message', data["message"])
        except OSError as err:
            print(err, file=sys.stderr)
            showinfo('Message', err)

        self.logcatStatus.cmd_lockPattern == COMMAND_UNLOCK_PATTERN

    def active_car(self):
        self.logcatStatus.cmd_lockPattern == COMMAND_LOCK_PATTERN
        time.sleep(5)
        self.logcatStatus.cmd_lockPattern == COMMAND_UNLOCK_PATTERN



    # def stopLogcat_TbxLog(self):
        # if self.logcatStatus.cmd_executing:
        #     self.logcatStatus.cmd_executing = False
        #
        #     if self.logcatStatus.cmd_lockPattern == COMMAND_LOCK_PATTERN:
        #         self.sendLogcat_stopScript()
        # else:
        #     self.updateMessage("###no job scheduled###")
        # self.updateMessage("### stop ###")

