'''
    @Create time:   2022/2/26 16:06
    @Autohr:        Patrick.Yang
    @File:          run.py.py
    @Software:      PyCharm
    -*- coding: utf-8 -*-
'''
from DebugPage import *
from HomePage import *
from config import *


class APP(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.page = None
        self.pageID = 0  # initial

    def run(self, initialPage, id):
        self.page = initialPage(self)
        self.pageID = id
        while True:
            self.mainloop()
            if self.page.status == PAGE_STATUS_SWITCHPAGE:
                self.setPage()
            elif self.page.status == PAGE_STATUS_ERR:
                print("error condition occurred")
                break
            else:
                break

    def setPage(self):
        if self.pageID == PAGE_ID_HOME:
            self.page = DebugPage(self)
            self.pageID = PAGE_ID_DEBUG     # set new page id
        elif self.pageID == PAGE_ID_DEBUG:
            self.page = HomePage(self)
            self.pageID = PAGE_ID_HOME      # set new page id


_app = APP()

if __name__ == '__main__':
    _app.run(HomePage, PAGE_ID_HOME)
