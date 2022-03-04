'''
    @Create time:   2022/3/1 9:57
    @Autohr:        Patrick.Yang
    @File:          FrameSpecialCmd.py
    @Software:      PyCharm
    -*- coding: utf-8 -*-
'''
import subprocess
from tkinter.messagebox import showinfo
from tkinter import *

INFO_WINDOW_WIDTH = 60
INFO_WINDOW_HEIGHT = 25

CMD_WINDOW_WIDTH = INFO_WINDOW_WIDTH
CMD_WINDOW_HEIGHT = 20


class Frame_SpecialCmd(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.root = master
        self.creatPage()

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

        # list box to stroe the previous message **row2**
        self.message_list_info = Listbox(self.messages_frame_info, height=24, width=60, bd=0,
                                         yscrollcommand=self.yscrollbar_info.set,
                                         xscrollcommand=self.xscrollbar_info.set)
        self.message_list_info.grid(row=2, column=0, rowspan=16)
        self.xscrollbar_info.config(command=self.message_list_info.xview)
        self.yscrollbar_info.config(command=self.message_list_info.yview)

        # command label frames of tbox update **row20**
        # self.cmd_frame_dmclient = LabelFrame(self.root, text='dmclient commands', width=INFO_WINDOW_HEIGHT, labelanchor=N)
        # self.cmd_frame_dmclient.grid(row=45, column=0, rowspan=5, columnspan=8)
        #
        # # input label showed below **row21**
        # self.cmd_label_dmclient = Label(self.cmd_frame_dmclient, text='start/stop real-time output',
        #                                 width=CMD_WINDOW_WIDTH, padx=10, pady=5)
        # self.cmd_label_dmclient.config(fg="blue")
        # self.cmd_label_dmclient.grid(row=46, column=0, columnspan=8)
        #
        # # to send out the message **row22**
        # self.dmclient_start_button = Button(self.cmd_frame_dmclient, text="start updating result", padx=10, pady=5,
        #                                     command=self.startGetting_DmclientLog())
        # self.dmclient_start_button.grid(row=47, column=0, columnspan=8,
        #                                 sticky=W + E + N + S)
        #
        # # clear **row23**
        # self.dmclient_stop_button = Button(self.cmd_frame_dmclient, text="stop updating", padx=10, pady=5,
        #                                    command=self.startGetting_DmclientLog)
        # self.dmclient_stop_button.grid(row=48, column=0, columnspan=8,
        #                                sticky=W + E + N + S)

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

    def upadteMessage(self):
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


root = Tk()
root.title("SpecialCmd")

Frame_SpecialCmd(root)

root.mainloop()
