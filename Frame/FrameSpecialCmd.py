'''
    @Create time:   2022/3/1 9:57
    @Autohr:        Patrick.Yang
    @File:          FrameSpecialCmd.py
    @Software:      PyCharm
    -*- coding: utf-8 -*-
'''
import subprocess
import tkinter.ttk
from tkinter.messagebox import showinfo
from tkinter import *
from tkinter.ttk import Combobox
import sys

INFO_WINDOW_WIDTH = 60
INFO_WINDOW_HEIGHT = 25

CMD_WINDOW_WIDTH = INFO_WINDOW_WIDTH
CMD_WINDOW_HEIGHT = 20

COMMAND_TABLE = {
    '1': "find",
    '2': "get",
    '3': "clean"
}


class Frame_SpecialCmd(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.root = master
        self.creatPage()
        self.infoIndex = 0

    def creatPage(self):
        #
        self.cheatbox_frame_info = LabelFrame(self.root, text='L555', width=60, labelanchor=N)
        self.cheatbox_frame_info.grid(row=0, column=0, rowspan=15, columnspan=8)

        # dmclient logging window grouping with other widgets
        self.messages_frame_info = Frame(self.cheatbox_frame_info, bd=3, relief=SUNKEN, padx=5)
        self.messages_frame_info.grid(row=1, column=0, rowspan=15, sticky=W + E + N + S)

        # Horizontal Scrollbar
        self.xscrollbar_info = Scrollbar(self.messages_frame_info, orient=HORIZONTAL)
        self.xscrollbar_info.grid(row=18, columnspan=8, sticky=E + W)

        # Vertical Scrollbar
        self.yscrollbar_info = Scrollbar(self.messages_frame_info, orient=VERTICAL)
        self.yscrollbar_info.grid(row=0, column=8, rowspan=19, sticky=N + S + W)

        # list box to store the previous message **row2**
        self.message_list_info = Listbox(self.messages_frame_info, height=24, width=60, bd=0,
                                         yscrollcommand=self.yscrollbar_info.set,
                                         xscrollcommand=self.xscrollbar_info.set)
        self.message_list_info.grid(row=2, column=0, rowspan=16)
        self.xscrollbar_info.config(command=self.message_list_info.xview)
        self.yscrollbar_info.config(command=self.message_list_info.yview)

        self.strVar = StringVar()
        self.command_box = Combobox(self.root, textvariable=self.strVar)
        command_list = list(COMMAND_TABLE.values())
        self.command_box["values"] = command_list   # fill the command in combobox
        self.command_box.current(0)
        # self.command_box.bind("<<ComboboxSelected>>", self.getBox)
        self.command_box.grid(row=22, column=0, columnspan=5, sticky=W + E + N + S)

        self.get_button = Button(self.root, text="get Text ", padx=10, pady=5,
                                 command=self.getBox)
        self.get_button.grid(row=22, column=5, columnspan=2, sticky=W + E + N + S)

    '''
    send message sample
    '''

    # # input label showed below **row20**
    # self.input_label_tbxUpdate = Label(self.cheatbox_frame_tbxUpdate, text='Enter message', padx=10, pady=5)
    # self.input_label_tbxUpdate.grid(row=20, column=90, columnspan=8)
    #
    # # button for message test **row21**
    # self.input_entry = Entry(self.cheatbox_frame_tbxUpdate, width=50, borderwidth=5)
    # self.input_entry.grid(row=21, column=90, columnspan=8)
    # self.input_entry.bind("<Return>", self.upadteMessage)
    #
    # # to send out the message **row22**
    # self.send_button = Button(self.cheatbox_frame_tbxUpdate, text="Send Text ", padx=10, pady=5,
    #                           command=self.sendMessage)
    # self.send_button.grid(row=22, column=90, columnspan=6, sticky=W + E + N + S)
    #
    # # clear **row23**
    # self.clear_button = Button(self.cheatbox_frame_tbxUpdate, text="Clear Text ", padx=10, pady=5,
    #                            command=self.clearMessage)
    # self.clear_button.grid(row=23, column=90, columnspan=6, sticky=W + E + N + S)

    def startGetting_TbxLog(self):
        new_msg = ''

    def stopGetting_TbxLog(self):
        new_msg = ''

    def startGetting_DmclientLog(self):
        new_msg = ''
        print("")

    def stopGetting_DmclientLog(self):
        new_msg = ''
        print("")

    def get_key2int(self, dct, value) -> int:
        return int([k for (k, v) in dct.items() if v == value][0], 10)

    def updateMessage(self, message):
        # new_msg = ''
        # new_msg = self.input_entry.get()
        # self.input_entry.delete(0, END)  # clear inupt message

        self.message_list_info.insert(END, message)
        self.message_list_info.see(END)  # show last line when text overflow

    def sendMessage(self):
        newMsg = ''
        print("sent")
        self.count = self.count + 1

        newMsg = self.input_entry.get()
        self.input_entry.delete(0, END)  # clear input message

        self.message_list_tbxUpdate.insert(END, newMsg + str(self.count))
        self.message_list_tbxUpdate.see(END)  # show last line when text overflow

    def clearMessage(self):
        self.message_list_tbxUpdate.delete(0, END)

    def getBox(self):
        cmd_str = self.command_box.get()
        '''# other way to get'''
        # print(self.strVar.get())
        cmd_number = self.get_key2int(COMMAND_TABLE, cmd_str)
        self.executeCommand(cmd_number)

    def executeCommand(self, command):
        cmd = ShellCommands()
        status, message = cmd.getCommand(command)
        self.last_status = status
        self.last_message = message
        print("status {}".format(status))
        if status == 0:
            self.updateMessage(message)


class ShellCommands(object):
    def commands_1(self):
        print("executing command1")
        ret_message = ''
        cmd = "adb get state"

        try:
            r0 = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ret_message = r0.communicate()[0]  # [0] output message, [1] error message
        except OSError as err:
            print(err, file=sys.stderr)
            ret_message = err
        return 0, ret_message

    def commands_2(self):
        print("executing command2")
        ret_message = ''
        cmd = "ipconfig"
        try:
            r0 = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ret_message = r0.communicate()[0]  # [0] output message, [1] error message
        except OSError as err:
            print(err, file=sys.stderr)
            ret_message = err
        return 0, ret_message

    def commands_3(self):
        ret_message = ''
        print("executing command3")



        return 0, ret_message

    def getCommand(self, no):
        name_of_method = "commands_" + str(no)
        method = getattr(self, name_of_method, lambda: -1)
        return method()


root = Tk()
root.title("SpecialCmd")

Frame_SpecialCmd(root)

root.mainloop()
