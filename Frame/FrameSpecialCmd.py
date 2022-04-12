'''
    @Create time:   2022/3/1 9:57
    @Autohr:        Patrick.Yang
    @File:          FrameSpecialCmd.py
    @Software:      PyCharm
    -*- coding: utf-8 -*-
'''
import subprocess
import time
import tkinter.ttk
from tkinter.messagebox import showinfo
from tkinter import *
from tkinter.ttk import Combobox
import sys
from apscheduler.schedulers.background import BackgroundScheduler

INFO_WINDOW_WIDTH = 60
INFO_WINDOW_HEIGHT = 25

CMD_WINDOW_WIDTH = INFO_WINDOW_WIDTH
CMD_WINDOW_HEIGHT = 20

ADB_SHELL_LOGCAT_CMD2 = 'adb shell "/custapp/bin/logcat -v time -b main | grep Eth"'
ADB_SHELL_LOGCAT_CMD1 = "adb shell tail -f /custapp/mnt/log/ota/tbox-updateagent.log"

COMMAND_LOCK_PATTERN = 0xCC
COMMAND_UNLOCK_PATTERN = 0x00

COMMAND_TABLE = {
    '1': "get adb state",
    '2': "get ipconfig",
    '3': "push eth_app",
    '4': "cp & export",
    '5': "kill process"
}


def get_key2int(dct, value) -> int:
    return int([k for (k, v) in dct.items() if v == value][0], 10)


class CmdStatus:
    def __init__(self, master=None):
        self.cmd_executing = False
        self.cmd_lockPattern = COMMAND_UNLOCK_PATTERN


class Frame_SpecialCmd(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
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
        print("special ready")
        # command and result cheatbox
        self.cheatbox_frame_info = LabelFrame(self.root, text='command logging', width=60, labelanchor=N)
        self.cheatbox_frame_info.grid(row=0, column=0, rowspan=15, columnspan=8)

        # command logging window grouping with other widgets
        self.messages_frame_info = Frame(self.cheatbox_frame_info, bd=3, relief=SUNKEN, padx=5)
        self.messages_frame_info.grid(row=1, column=0, rowspan=15, sticky=W + E + N + S)

        # Horizontal Scrollbar
        self.xscrollbar_info = Scrollbar(self.messages_frame_info, orient=HORIZONTAL)
        self.xscrollbar_info.grid(row=18, columnspan=8, sticky=E + W)

        # Vertical Scrollbar
        self.yscrollbar_info = Scrollbar(self.messages_frame_info, orient=VERTICAL)
        self.yscrollbar_info.grid(row=0, column=8, rowspan=19, sticky=N + S + W)

        # list box to store the previous message **row2**
        self.message_list_info = Listbox(self.messages_frame_info, height=26, width=80, bd=0,
                                         yscrollcommand=self.yscrollbar_info.set,
                                         xscrollcommand=self.xscrollbar_info.set)
        self.message_list_info.grid(row=2, column=0, rowspan=16)
        self.xscrollbar_info.config(command=self.message_list_info.xview)
        self.yscrollbar_info.config(command=self.message_list_info.yview)

        self.strVar = StringVar()
        self.command_box = Combobox(self.root, textvariable=self.strVar)
        command_list = list(COMMAND_TABLE.values())
        self.command_box["values"] = command_list  # fill the command in combobox
        self.command_box.current(0)
        # self.command_box.bind("<<ComboboxSelected>>", self.getBox)
        self.command_box.grid(row=22, column=0, columnspan=5, sticky=W + E + N + S)

        self.get_button = Button(self.root, text="send cmd ", padx=10, pady=5,
                                 command=self.getBox)
        self.get_button.grid(row=22, column=5, columnspan=2, sticky=W + E + N + S)

        self.logcatEnable_button = Button(self.root, text="start logcat", padx=10, pady=5,
                                    command=self.startLogcat_TbxLog)
        self.logcatEnable_button.grid(row=23, column=0, columnspan=2, sticky=W + E + N + S)

        self.logcatDisable_button = Button(self.root, text="stop logcat", padx=10, pady=5,
                                    command=self.stopLogcat_TbxLog)
        self.logcatDisable_button.grid(row=23, column=5, columnspan=2, sticky=W + E + N + S)

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
        self.command_box.grid_remove()
        self.get_button.grid_remove()
        self.logcatEnable_button.grid_remove()
        self.logcatDisable_button.grid_remove()
        if self.scheduler is not None:
            self.scheduler.remove_all_jobs()
            self.scheduler.shutdown()
            self.scheduler = None
        return ret

    def startLogcat_TbxLog(self):
        if not self.logcatStatus.cmd_executing:
            self.idLogcat = "logcat"
            self.jobLogcat = self.scheduler.add_job(self.logcatRecv, trigger='interval', seconds=1, id=self.idLogcat)
        else:
            self.updateMessage("###job already started###")

    def stopLogcat_TbxLog(self):
        if self.logcatStatus.cmd_executing:
            self.logcatStatus.cmd_executing = False

            if self.logcatStatus.cmd_lockPattern == COMMAND_LOCK_PATTERN:
                cmd = "adb push E:\\temp\eth_app\eth_stop /data/userdata"
                self.r1 = subprocess
                print(self.r1.getoutput(cmd))
                cmd = "adb shell"
                self.r1 = subprocess.Popen(cmd, shell=True,
                                           stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                cmds = [
                    "cp -f /data/userdata/eth_stop /usr/share",
                    "cd /usr/share/",
                    "export LD_LIBRARY_PATH=/custapp/lib:${LD_LIBRARY_PATH}",
                    "echo $LD_LIBRARY_PATH",
                    "chmod 777 ./eth_stop",
                    "./eth_stop",
                    "exit",
                ]
                cmd_list = "\n".join(cmds) + "\n"
                debugMsg = ''
                output = self.r1.communicate(cmd_list.encode("utf-8"))
                for item in output:
                    debugMsg += item.decode("gbk").replace("\r\r", "")
                    print(debugMsg)
                print("remove")
        else:
            self.updateMessage("###no job scheduled###")

    def logcatRecv(self):
        self.jobLogcat.pause()
        self.logcatStatus.cmd_executing = True
        self.r0 = subprocess.Popen(ADB_SHELL_LOGCAT_CMD2, shell=True,
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        n = None
        while (n is None) and self.logcatStatus.cmd_executing:
            # get the lock pattern
            if self.logcatStatus.cmd_lockPattern == COMMAND_UNLOCK_PATTERN:
                self.logcatStatus.cmd_lockPattern = COMMAND_LOCK_PATTERN
                n = self.r0.poll()
                try:
                    message = self.r0.stdout.readline().decode("gbk").replace("\r", "")
                    self.updateMessage(message)
                except (IOError, BrokenPipeError):
                    pass
                self.logcatStatus.cmd_lockPattern = COMMAND_UNLOCK_PATTERN
            time.sleep(0.0001)  # 100 us
        self.r0.kill()  # kill process
        self.updateMessage("###logcat stopped###")
        if self.logcatStatus.cmd_executing:
            print("poll stopped by other interrupt")
            # still running next time
            self.jobLogcat.resume()
        else:
            # terminate via stop button
            self.scheduler.remove_job(self.idLogcat)

    def updateMessage(self, message):
        # new_msg = ''
        # new_msg = self.input_entry.get()
        # self.input_entry.delete(0, END)  # clear inupt message
        newlines = message.splitlines(keepends=TRUE)
        print(newlines)
        for line in newlines:
            self.message_list_info.insert(END, line)
        self.message_list_info.see(END)  # show last line when text overflow

    def getBox(self):
        cmd_str = self.command_box.get()
        # other way to get
        # print(self.strVar.get())
        cmd_number = get_key2int(COMMAND_TABLE, cmd_str)  # find command number
        self.executeCommand(cmd_number)

    def executeCommand(self, command):
        self.lock = True
        print("lock:{}".format(self.lock))
        cmd = ShellCommands()
        status, message = cmd.getCommand(command)
        self.last_status = status
        self.last_message = message
        print("status {}".format(status))
        if status == 0:
            self.updateMessage(message)
        self.lock = False


# shell commands definition
# add new command(s) with follow name "commands_x"
class ShellCommands(object):
    def commands_1(self):
        print("executing command1")
        ret_message = ''
        cmd = "adb get-state"
        ret_message = subprocess.getoutput(cmd)

        return 0, ret_message

    def commands_2(self):
        print("executing command2")
        ret_message = ''
        cmd = "ipconfig"

        ret_message = subprocess.getoutput(cmd)
        return 0, ret_message

    def commands_3(self):
        print("executing command4")
        ret_message = ''
        cmd = "adb push E:\\temp\eth_app\eth_app /data/userdata"

        ret_message = subprocess.getoutput(cmd)
        return 0, ret_message

    def commands_4(self):
        print("executing command4")
        ret_message = ''
        cmd = "adb shell"
        r0 = subprocess.Popen(cmd, shell=True,
                              stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        cmds = [
            "cp -f /data/userdata/eth_app /usr/share",
            "cd /usr/share/",
            "chmod 777 ./eth_app",
            # "export LD_LIBRARY_PATH=/custapp/lib:${LD_LIBRARY_PATH}",
            # "echo $LD_LIBRARY_PATH",
            "exit",
        ]
        cmd_list = "\n".join(cmds) + "\n"
        output = r0.communicate(cmd_list.encode("utf-8"))
        for item in output:
            ret_message += item.decode("gbk").replace("\r\r", "")
            print(ret_message)

        return 0, ret_message

    def commands_5(self):
        print("executing command5")
        ret_message = ''
        cmd = "adb shell"
        r0 = subprocess.Popen(cmd, shell=True,
                              stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        cmds = [
            "pkill -9 monitor_app",
            "pkill -9 eth_app",
            "exit",
        ]
        cmd_list = "\n".join(cmds) + "\n"
        output = r0.communicate(cmd_list.encode("utf-8"))
        for item in output:
            ret_message += item.decode("gbk").replace("\r\r", "")
            print(ret_message)

        return 0, ret_message

    def getCommand(self, no):
        name_of_method = "commands_" + str(no)
        method = getattr(self, name_of_method, lambda: -1)  # return -1 for invalid command
        return method()
