'''
    @Create time:   2022/3/1 9:37
    @Autohr:        Patrick.Yang
    @File:          FrameOtaLog.py.py
    @Software:      PyCharm
    -*- coding: utf-8 -*-
'''
import subprocess
from tkinter.messagebox import showinfo
from tkinter import *

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


class Frame_OtaLog(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.root = master
        self.createPage()

    def createPage(self):
        # window1 #
        # dmclient log chat box label frame
        self.cheatbox_frame_dmclient = LabelFrame(self.root, text='dmclient.log', width=WIDTH_FRAME_WIN_1, labelanchor=N)
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
        self.message_list_dmclient = Listbox(self.messages_frame_dmclient, height=WINDOW_HEIGHT, width=WIDTH_FRAME_WIN_1, bd=0,
                                             yscrollcommand=self.yscrollbar_dmclient.set,
                                             xscrollcommand=self.xscrollbar_dmclient.set)
        self.message_list_dmclient.grid(row=ROW_LISTBOX, column=0, rowspan=16)
        self.xscrollbar_dmclient.config(command=self.message_list_dmclient.xview)
        self.yscrollbar_dmclient.config(command=self.message_list_dmclient.yview)

        # command label frames of tbox update **row20**
        self.cmd_frame_dmclient = LabelFrame(self.root, text='dmclient commands', width=WIDTH_FRAME_WIN_1, labelanchor=N)
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
                                           command=self.startGetting_DmclientLog)
        self.dmclient_stop_button.grid(row=ROW_STOP_BUTTON, column=COLUMN_INSERT_WIN_1, columnspan=8,
                                       sticky=W + E + N + S)

        # window2 #
        # tboxUpdate log chat box label frame
        self.cheatbox_frame_tbxUpdate = LabelFrame(self.root, text='tbox-UpdateAgent', width=WIDTH_FRAME_WIN_2, labelanchor=N)
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
        self.message_list_tbxUpdate = Listbox(self.messages_frame_tbxUpdate, height=WINDOW_HEIGHT, width=WIDTH_FRAME_WIN_2, bd=0,
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


    def pageDestroy(self):
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

    def updateMessage(self):
        new_msg = ''
        new_msg = self.input_entry.get()
        self.input_entry.delete(0, END)  # clear inupt message

        self.message_list_tbxUpdate.insert(END, new_msg)
        self.message_list_tbxUpdate.see(END)  # show last line when text overflow

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


