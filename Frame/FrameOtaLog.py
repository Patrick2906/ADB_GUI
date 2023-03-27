'''
    @Create time:   2022/3/1 9:37
    @Autohr:        Patrick.Yang
    @File:          FrameOtaLog.py.py
    @Software:      PyCharm
    -*- coding: utf-8 -*-
'''
import subprocess
from tkinter.messagebox import showinfo
from apscheduler.schedulers.background import BackgroundScheduler
from tkinter import *
import os
from config import *

ETH_STOP_PATH = os.getcwd() + "/ADB_WIN_LIB/eth_stop"

COMMAND_LOCK_PATTERN = 0xCC
COMMAND_UNLOCK_PATTERN = 0x00

ROW_LOGGING_FRAME = 0
ROW_LOGGING_LABEL = 1
ROW_LISTBOX = 2
ROW_XSCROLL = 18
ROW_CMD_FRAME = ROW_XSCROLL + 2
ROW_CMD_LABEL = ROW_XSCROLL + 3
ROW_START_BUTTON = ROW_XSCROLL + 4
ROW_STOP_BUTTON = ROW_XSCROLL + 5

WIDTH_FRAME_WIN_1 = 60
WIDTH_WIDGET_WIN_1 = 60
COLUMN_INSERT_WIN_1 = 0
WIDTH_FRAME_WIN_2 = 60
WIDTH_WIDGET_WIN_2 = 60
COLUMN_INSERT_WIN_2 = 60

WINDOW_HEIGHT = ROW_XSCROLL + 6
WIND_OFFSET_HORIZONTAL = COLUMN_INSERT_WIN_2 - COLUMN_INSERT_WIN_1

class CmdStatus:
    def __init__(self, master=None):
        self.cmd_executing = False
        self.cmd_lockPattern = COMMAND_UNLOCK_PATTERN
        self.cmd_lastStr = ''

class Frame_OtaLog(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.r0 = None
        self.idTbxLog = None
        self.scheduler = None
        self.root = master
        self.lock = False
        self.createPage()
        self.dmClientStatus = CmdStatus()
        self.tbxLogStatus = CmdStatus()
        self.lastStrTboxLog = None


    def createPage(self):
        """ window1 """
        # dmclient log chat box label frame
        self.cheatbox_frame_dmclient = LabelFrame(self.root, text='dmclient.log', width=WIDTH_FRAME_WIN_1,
                                                  labelanchor=N)
        self.cheatbox_frame_dmclient.grid(row=ROW_LOGGING_FRAME, column=0, rowspan=15, columnspan=8)

        # dmclient logging window grouping with other widgets
        self.messages_frame_dmclient = Frame(self.cheatbox_frame_dmclient, bd=3, relief=SUNKEN, padx=5)
        self.messages_frame_dmclient.grid(row=ROW_LOGGING_LABEL, column=0, rowspan=15, sticky=W + E + N + S)

        # Horizontal Scrollbar
        self.xscrollbar_dmclient = Scrollbar(self.messages_frame_dmclient, orient=HORIZONTAL)
        self.xscrollbar_dmclient.grid(row=ROW_XSCROLL, columnspan=8, sticky=E + W)

        # Vertical Scrollbar
        self.yscrollbar_dmclient = Scrollbar(self.messages_frame_dmclient, orient=VERTICAL)
        self.yscrollbar_dmclient.grid(row=0, column=8, rowspan=19, sticky=N + S + W)

        # list box to stroe the previous message **row2**
        self.message_list_dmclient = Listbox(self.messages_frame_dmclient, height=WINDOW_HEIGHT,
                                             width=WIDTH_FRAME_WIN_1, bd=0,
                                             yscrollcommand=self.yscrollbar_dmclient.set,
                                             xscrollcommand=self.xscrollbar_dmclient.set)
        self.message_list_dmclient.grid(row=ROW_LISTBOX, column=0, rowspan=16)
        self.xscrollbar_dmclient.config(command=self.message_list_dmclient.xview)
        self.yscrollbar_dmclient.config(command=self.message_list_dmclient.yview)

        # command label frames of tbox update **row20**
        self.cmd_frame_dmclient = LabelFrame(self.root, text='dmclient commands', width=WIDTH_FRAME_WIN_1,
                                             labelanchor=N)
        self.cmd_frame_dmclient.grid(row=ROW_CMD_FRAME, column=COLUMN_INSERT_WIN_1, rowspan=5, columnspan=8)

        # input label showed below **row21**
        self.cmd_label_dmclient = Label(self.cmd_frame_dmclient, text='start/stop real-time output',
                                        width=WIDTH_FRAME_WIN_1, padx=10, pady=5)
        self.cmd_label_dmclient.config(fg="blue")
        self.cmd_label_dmclient.grid(row=ROW_CMD_LABEL, column=COLUMN_INSERT_WIN_1, columnspan=8)

        # to send out the message **row22**
        self.dmclient_start_button = Button(self.cmd_frame_dmclient, text="start updating result", padx=10, pady=5,
                                            command=self.startGetting_DmclientLog)
        self.dmclient_start_button.grid(row=ROW_START_BUTTON, column=COLUMN_INSERT_WIN_1, columnspan=8,
                                        sticky=W + E + N + S)

        # clear **row23**
        self.dmclient_stop_button = Button(self.cmd_frame_dmclient, text="stop updating", padx=10, pady=5,
                                           command=self.stopGetting_DmclientLog)
        self.dmclient_stop_button.grid(row=ROW_STOP_BUTTON, column=COLUMN_INSERT_WIN_1, columnspan=8,
                                       sticky=W + E + N + S)

        """ window2 """
        # tboxUpdate log chat box label frame
        self.cheatbox_frame_tbxUpdate = LabelFrame(self.root, text='tbox-UpdateAgent', width=WIDTH_FRAME_WIN_2,
                                                   labelanchor=N)
        self.cheatbox_frame_tbxUpdate.grid(row=0, column=COLUMN_INSERT_WIN_2, rowspan=15, columnspan=8)

        # tboxUpdate logging window grouping with other widgets
        self.messages_frame_tbxUpdate = Frame(self.cheatbox_frame_tbxUpdate, bd=3, relief=SUNKEN, padx=5)
        self.messages_frame_tbxUpdate.grid(row=1, column=COLUMN_INSERT_WIN_2, rowspan=15, sticky=W + E + N + S)

        # Horizontal Scrollbar
        self.xscrollbar_tbxUpdate = Scrollbar(self.messages_frame_tbxUpdate, orient=HORIZONTAL)
        self.xscrollbar_tbxUpdate.grid(row=ROW_XSCROLL, columnspan=COLUMN_INSERT_WIN_2, sticky=E + W)

        # Vertical Scrollbar
        self.yscrollbar_tbxUpdate = Scrollbar(self.messages_frame_tbxUpdate, orient=VERTICAL)
        self.yscrollbar_tbxUpdate.grid(row=0, column=COLUMN_INSERT_WIN_2, rowspan=19, sticky=E + N + S)

        # list box to stroe the previous message **row2**
        self.message_list_tbxUpdate = Listbox(self.messages_frame_tbxUpdate, height=WINDOW_HEIGHT,
                                              width=WIDTH_FRAME_WIN_2, bd=0,
                                              yscrollcommand=self.yscrollbar_tbxUpdate.set,
                                              xscrollcommand=self.xscrollbar_tbxUpdate.set)
        self.message_list_tbxUpdate.grid(row=2, column=0, rowspan=16)
        self.xscrollbar_tbxUpdate.config(command=self.message_list_tbxUpdate.xview)
        self.yscrollbar_tbxUpdate.config(command=self.message_list_tbxUpdate.yview)

        # command label frames of tbox update **row20**
        self.cmd_frame_tbxUpdate = LabelFrame(self.root, text='tbx commands', width=WIDTH_FRAME_WIN_2, labelanchor=N)
        self.cmd_frame_tbxUpdate.grid(row=ROW_CMD_FRAME, column=COLUMN_INSERT_WIN_2, rowspan=5, columnspan=8)

        # input label showed below **row21**
        self.cmd_label_tbxUpdate = Label(self.cmd_frame_tbxUpdate, text='start/stop real-time output',
                                         width=WIDTH_FRAME_WIN_2, padx=10, pady=5)
        self.cmd_label_tbxUpdate.config(fg="blue")
        self.cmd_label_tbxUpdate.grid(row=ROW_CMD_LABEL, column=COLUMN_INSERT_WIN_2, columnspan=8)

        # to send out the message **row22**
        self.tbx_start_button = Button(self.cmd_frame_tbxUpdate, text="start tbox-UpdateAgent", padx=10, pady=5,
                                       command=self.startGetting_TbxLog)
        self.tbx_start_button.grid(row=ROW_START_BUTTON, column=COLUMN_INSERT_WIN_2, columnspan=8, sticky=W + E + N + S)

        # clear **row23**
        self.tbx_stop_button = Button(self.cmd_frame_tbxUpdate, text="stop tbox-UpdateAgent", padx=10, pady=5,
                                      command=self.stopGetting_TbxLog)
        self.tbx_stop_button.grid(row=ROW_STOP_BUTTON, column=COLUMN_INSERT_WIN_2, columnspan=8, sticky=W + E + N + S)

        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

    def pageDestroy(self):
        ret = 0
        # if self.tbxLogStatus.cmd_lockPattern == COMMAND_LOCK_PATTERN:

        self.cheatbox_frame_dmclient.grid_remove()
        self.messages_frame_dmclient.grid_remove()
        self.xscrollbar_dmclient.grid_remove()
        self.yscrollbar_dmclient.grid_remove()
        self.message_list_dmclient.grid_remove()
        self.cmd_frame_dmclient.grid_remove()
        self.cmd_label_dmclient.grid_remove()
        self.dmclient_start_button.grid_remove()
        self.dmclient_stop_button.grid_remove()
        self.cheatbox_frame_tbxUpdate.grid_remove()
        self.messages_frame_tbxUpdate.grid_remove()
        self.xscrollbar_tbxUpdate.grid_remove()
        self.yscrollbar_tbxUpdate.grid_remove()
        self.message_list_tbxUpdate.grid_remove()
        self.cmd_frame_tbxUpdate.grid_remove()
        self.cmd_label_tbxUpdate.grid_remove()
        self.tbx_start_button.grid_remove()
        self.tbx_stop_button.grid_remove()
        if self.scheduler is not None:
            self.scheduler.remove_all_jobs()
            self.scheduler.shutdown()
            self.scheduler = None

        return ret

    def load_TbxLog(self):
        #     n = p.poll()
        #     message = p.stdout.readline().decode("gbk")
        #     print(message)
        self.jobTbxLog.pause()

        r0 = subprocess.Popen("adb shell tail -f /custapp/mnt/log/ota/tbox-updateagent.log", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
        n = None
        while n is None:
            n = r0.poll()
            message = r0.stdout.readline().decode("gbk")
            if (message == ''):
                print("empty")
            else:
                print(message)
            self.updateMessage_tbox(message)
        self.jobTbxLog.resume()

    def load_Dmclient(self):
        self.jobDmclient.pause()
        print(self.jobDmclient)
        self.jobDmclient.resume()

    def startGetting_TbxLog(self):
        if not self.tbxLogStatus.cmd_executing:
            self.idTbxLog = "TBX_LOG"
            self.jobTbxLog = self.scheduler.add_job(self.load_TbxLog, trigger='interval', seconds=1, id=self.idTbxLog)
        else:
            self.updateMessage_tbox("###tbx job already started###")

    def stopGetting_TbxLog(self):
        if self.tbxLogStatus.cmd_executing:
            self.tbxLogStatus.cmd_executing = FALSE

            if self.tbxLogStatus.cmd_lockPattern == COMMAND_LOCK_PATTERN:
                self.sendLogcat_stopScript(self.tbxLogStatus.cmd_lastStr)

        self.jobTbxLog.pause()
        self.scheduler.remove_job(self.idTbxLog)

    def startGetting_DmclientLog(self):
        if not self.dmClientStatus.cmd_executing:
            self.idDmclient = "DM_CLIENT"
            self.jobDmclient = self.scheduler.add_job(self.load_Dmclient, trigger='interval', seconds=0.5,
                                                id=self.idDmclient)
        else:
            self.updateMessage_dm("###dmClient job already started###")

    def stopGetting_DmclientLog(self):

        self.jobDmclient.pause()
        self.scheduler.remove_job(self.idDmclient)
        print("")

    #tbox_updateagent.log
    def updateMessage_tbox(self, message):
        newlines = message.splitlines(keepends=TRUE)
        for line in newlines:
            self.message_list_tbxUpdate.insert(END, line)
        self.message_list_tbxUpdate.see(END)  # show last line when text overflow

    # dmclient.log
    def updateMessage_dm(self, message):
        newlines = message.splitlines(keepends=TRUE)
        for line in newlines:
            self.message_list_dmclient.insert(END, line)
        self.message_list_dmclient.see(END)

    def sendLogcat_stopScript(self, lastStr=""):
        cmd_stop = lastStr
        cmd_stop = "nohup ./eth_stop " + cmd_stop + " &"

        cmd = ADB_PUSH + ETH_STOP_PATH + " /data/userdata"  # "adb push E:\\temp\eth_app\eth_stop /data/userdata"
        self.r0 = subprocess
        print(self.r0.getoutput(cmd))
        cmd = "adb shell"
        self.r0 = subprocess.Popen(cmd, shell=True,
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        cmds = [
            "cp -f /data/userdata/eth_stop /usr/share",
            "rm -f /data/userdata/eth_stop",
            "cd /usr/share/",
            "export LD_LIBRARY_PATH=/custapp/lib:${LD_LIBRARY_PATH}",
            "echo $LD_LIBRARY_PATH",
            "chmod 777 ./eth_stop",
            cmd_stop,
            "exit",
        ]
        cmd_list = "\n".join(cmds) + "\n"
        debugMsg = ''
        output = self.r0.communicate(cmd_list.encode("utf-8"))
        for item in output:
            debugMsg += item.decode("gbk").replace("\r\r", "")
            print(debugMsg)

    def clearMessage(self):
        self.message_list_tbxUpdate.delete(0, END)
        self.message_list_dmclient.delete(0, END)