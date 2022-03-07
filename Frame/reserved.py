'''
    @Create time:   2022/3/7 14:21
    @Autohr:        Patrick.Yang
    @File:          reserved.py.py
    @Software:      PyCharm
    -*- coding: utf-8 -*-
'''

'''
    ***** send message sample *****
     
    # input label showed below **row20**
    self.input_label_tbxUpdate = Label(self.cheatbox_frame_tbxUpdate, text='Enter message', padx=10, pady=5)
    self.input_label_tbxUpdate.grid(row=20, column=90, columnspan=8)
    
    # button for message test **row21**
    self.input_entry = Entry(self.cheatbox_frame_tbxUpdate, width=50, borderwidth=5)
    self.input_entry.grid(row=21, column=90, columnspan=8)
    self.input_entry.bind("<Return>", self.upadteMessage)
    
    # to send out the message **row22**
    self.send_button = Button(self.cheatbox_frame_tbxUpdate, text="Send Text ", padx=10, pady=5,
                              command=self.sendMessage)
    self.send_button.grid(row=22, column=90, columnspan=6, sticky=W + E + N + S)
    
    # clear **row23**
    self.clear_button = Button(self.cheatbox_frame_tbxUpdate, text="Clear Text ", padx=10, pady=5,
                               command=self.clearMessage)
    self.clear_button.grid(row=23, column=90, columnspan=6, sticky=W + E + N + S)
    
    
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

'''

'''
    ***** execute command and checkout the result *****

    def excCommand(self, cmd):
        try:
            r0 = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ret_message = r0.communicate()[0]  # [0] output message, [1] error message
        except OSError as err:
            print(err, file=sys.stderr)
            ret_message = err
        return 0, ret_message

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

'''

