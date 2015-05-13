__author__ = 'matthewgalligan'
from Tkinter import *


class GUI(object):
    '''
    The GUI Object contains a paintable canvas, a "get new words" button, and options to assist in connecting to other
    users
    '''
    def __init__(self):
        gui = Tk()
        gui.title("Pyctionary!")
        self.gui = gui
        self.last_pos = None
        canvas = Canvas(gui,width=500,height=500)
        canvas.pack()
        canvas.bind("<B1-Motion>", self.paint)
        canvas.bind("<Button-1>",self.paint)
        canvas.bind("<ButtonRelease-1>",self.unpaint)
        self.canvas = canvas
        mainloop()

    def unpaint(self,event):
        '''
        Stop painting. This tells the UI to not draw a line connecting the last point to the next drawn point.
        :param event: This contains the coordinates of the mouse release event. Not relevant to what we are doing
        :return: Nothing
        '''
        self.last_pos = None

    def paint(self,event):
        '''
        Continue painting. If painting a continuous line, draw a line from the last known point to fill
        any "holes"
        :param event: This contains the coordinates of the mouse event that triggered the paint event (and where we
         shoudl paint)
        :return: Nothing
        '''

        #http://www.python-course.eu/tkinter_canvas.php provided insight on using ovals to draw freely
        x1, y1,x2,y2 = ( event.x - 1 ), ( event.y - 1 ), ( event.x + 1 ), ( event.y + 1 )

        self.canvas.create_oval( x1, y1, x2, y2,fill="black")
        if self.last_pos:
            self.canvas.create_line(x1,y2,self.last_pos[0],self.last_pos[1])
        self.last_pos = (event.x,event.y)

