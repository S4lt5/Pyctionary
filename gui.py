__author__ = 'matthewgalligan'
from Tkinter import *
from phrase_generator import PhraseGenerator
from communicator import Communicator
from popup_window import InputDialog
import tkMessageBox

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

        button = Button(gui,text="Generate Phrase",command=self.get_phrase)
        button.pack()
        #the drawing canvas that is the focus of our app
        self.canvas = canvas
        #This is the list of individual draw elements
        self.doodles = []

        self.generator = PhraseGenerator
        self.communicator = Communicator()
        menu = Menu(gui)
        file_menu = Menu(menu,tearoff=0)
        file_menu.add_command(label="Save",command=self.save)
        file_menu.add_command(label="Load",command=self.load)
        file_menu.add_command(label="Clear",command=self.clear)

        network_menu = Menu(menu,tearoff=0)
        network_menu.add_command(label="Host Session",command=self.host)
        network_menu.add_command(label="Connect to Session",command=self.query_server_address)
        menu.add_cascade(label="File",menu=file_menu)
        menu.add_cascade(label="Network",menu=network_menu)
        gui.config(menu=menu)
        mainloop()

    def host(self):
        '''
        Begin hosting a new session
        :return: nothing
        '''
        self.communicator.connect(host=True,remote_address="")

    def query_server_address(self):
        '''
        Attempt to connect to a remote server
        :return: nothing
        '''
        #pass callback to join server after getting IP
        InputDialog(self.gui,self.join_server)


    def join_server(self,address):
        print("Joining " + address)
        self.communicator.connect(host=False,remote_address=address)

    def get_phrase(self):
        phrase = self.generator.GetPhrase()
        tkMessageBox.showinfo("Your Phrase","Your Pyctionary Phrase is: " + phrase)


    def save(self):
        '''
        Save a drawing to file
        :return: nothing
        '''
        with open("doodles.txt","w") as f:
            for doodle in self.doodles:
                line = "%d,%d,%d" % (doodle.doodle_type,doodle.x,doodle.y)
                #if there is a destination point, also write this
                if doodle.x2 and doodle.y2:
                    line += ",%d,%d" % (doodle.x2,doodle.y2)
                f.write(line +"\n")
            f.close()
        print(self.doodles)

    def load(self):
        '''
        Load a drawing from file
        :return: Nothing
        '''
        with open("doodles.txt","r") as f:
            lines = f.readlines()
            for line in lines:

                args = line.strip().split(",")
                if(len(args) == 3):
                    args.append(None)
                    args.append(None)

                doodle = GUI.Doodle(args[0],args[1],args[2],args[3],args[4])
                self.draw(doodle)
                #print(args)

    def clear(self):
        clear_doodle = GUI.Doodle(GUI.Doodle.CLEAR,0,0,0,0)
        self.draw(clear_doodle)

    def unpaint(self,event):
        '''
        Stop painting. This tells the UI to not draw a line connecting the last point to the next drawn point.
        :param event: This contains the coordinates of the mouse release event. Not relevant to what we are doing
        :return: Nothing
        '''
        self.last_pos = None

    def draw(self,doodle,store_local=True):
        '''
        Draw the specified doodle on the canvas
        :param doodle: The event to draw
        :return: Nothing
        '''

        if doodle is None:
            raise ValueError("No doodle passed to draw()")

        if(doodle.doodle_type == doodle.OVAL):
            self.canvas.create_oval( doodle.x-1, doodle.y-1, doodle.x+1, doodle.y+1,fill="black")
        elif(doodle.doodle_type == doodle.LINE):
            self.canvas.create_line(doodle.x,doodle.y,doodle.x2,doodle.y2)
        elif(doodle.doodle_type == doodle.CLEAR):
            self.canvas.delete("all")
        else:
            raise ValueError("Unknown doodle type passed to draw()")

        #if we are drawing locally, store this on the list of user actions for saving/transmitting
        if store_local is True:
            self.doodles.append(doodle)


    def paint(self,event):
        '''
        Continue painting. If painting a continuous line, draw a line from the last known point to fill
        any "holes"
        :param event: This contains the coordinates of the mouse event that triggered the paint event (and where we
         should paint)
        :return: Nothing
        '''

        #http://www.python-course.eu/tkinter_canvas.php provided insight on using ovals to draw freely
        #the ovals(circles, really) are radius "1" from the point clicked.
        doodle = GUI.Doodle(GUI.Doodle.OVAL,event.x,event.y,None,None)
        self.draw(doodle)
        #draw a line between this position and the last to ensure we have a continuous drawing line
        if self.last_pos:
            line_doodle = GUI.Doodle(GUI.Doodle.LINE,event.x,event.y,self.last_pos[0],self.last_pos[1])
            self.draw(line_doodle)

        #store last position to draw a line between any 'gaps'
        self.last_pos = (event.x,event.y)

    class Doodle(object):
        '''
        A doodle represents a particular line or oval in a pyctionary drawing.

        These are stored and retrieved to reproduce a user-drawn image.

        '''
        #An oval is drawn with radius 1 at point x,y
        OVAL = 0
        #A line is drawn between points at x,y and x2,y2
        LINE = 1
        #A clear instruction erases the drawing area.
        CLEAR = 3



        def __init__(self,doodle_type,x,y,x2,y2):
            self.doodle_type = int(doodle_type)
            self.x = int(x)
            self.y = int(y)
            if x2:
                self.x2 = int(x2)
            else:
                self.x2 = None
            if y2:
                self.y2 = int(y2)
            else:
                self.y2 = None
