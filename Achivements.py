from tkinter import *
import time
import random

class achivements:
    def __init__(self):
        self.tk = Tk()
        self.tk.title("Achivements")
        self.tk.resizable(0,0)
        self.tk.wm_attributes("-topmost", 1)
        self.main_frame = Frame(self.tk)
        self.main_frame.pack(fill=BOTH, expand = 1)
        self.canvas_container = Frame(self.main_frame)
        self.canvas_container.pack(fill=BOTH, expand = 1)
        self.canvas = Canvas(self.canvas_container, width=300, height=400, \
                             highlightthickness = 0)
        self.canvas.pack(fill=BOTH, expand=1)
    def breaktobool(string11):
        boollist = []
        for char in string11:
            if char == '0':
                boollist.append(False)
            elif char == '1':
                boollist.append(True)
        return boollist
    def fusetobool(bools):
        string = ''
        for i in range(len(bools)):
            if bools[i] == True:
                string += "1"
            elif bools[i] == False:
                string += "0"
        return string
    def achive(self, name, backgroundcolor, color, x, y):
        rect = self.canvas.create_rectangle(x, y, x + 100, y + 100, \
                                            fill = backgroundcolor, outline = "black")
        circle = self.canvas.create_oval(x, y, x + 100, y + 100,outline = "black", \
                                         fill = color)
        text = self.canvas.create_text(x + 50, y + 50, text=name, fill="black",
                                      font=("Impact", 20, "bold"))
    def notachived(self, x, y):
        self.achive("???", "black", "white", x, y)
    def achive_check(self, tf, name, backgroundcolor, color, x, y):
        if tf == True:
            self.achive(name, backgroundcolor, color, x, y)
        elif tf == False:
            self.notachived(x, y)
    def check_all(self, bools):
        self.achive_check(bools[0], "PLAY", "blue", "red", 0, 0)
        self.achive_check(bools[1], """1ST
DRAW""", "purple", "green", 100, 0)
        self.achive_check(bools[2], """BUY
CPS""", "cyan", "orange", 200, 0)
        self.achive_check(bools[3], """RARE
DRAW""", "orange", "green", 0, 100)
        self.achive_check(bools[4], """BEST
DRAW""", "yellow", "white", 100, 100)
        self.achive_check(bools[5], """LUCKY
BOOST""", "cyan", "green", 200, 100)
        self.achive_check(bools[6], """LETS
GO...""", "red", "orange", 0, 200)
        self.achive_check(bools[7], """DRAW
A LOT""", "orange", "cyan", 100, 200)
        self.achive_check(bools[8], """ON THE
GRIND""", "red", "white", 200, 200)
        self.achive_check(bools[9], """DONE
HERE""", "pink", "purple", 0, 300)

##bools = [True, True, False, False, False, False, False, False, False, False, False, False]   
##a = achivements()
##a.check_all(bools)

