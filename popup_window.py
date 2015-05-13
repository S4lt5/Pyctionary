__author__ = 'matthewgalligan'
from Tkinter import *
class InputDialog(object):
    def __init__(self,gui,callback):
        '''
        Default initialization
        :param gui: A reference to a TK root object
        :param callback: A callback function to perform, passing the address entered as the first parameter
        :return:
        '''
        top=Toplevel(gui)
        self.top = top
        self.callback = callback
        Label(top,text="Please input the destinatio server address").pack()
        self.input=Entry(top)
        self.input.pack()
        Button(top,text="OK",command=self.close).pack()
    def close(self):
        '''
        Get the value, call the callback and close the dialog
        :return:
        '''
        self.value = self.input.get()
        self.callback(self.value)
        self.top.destroy()