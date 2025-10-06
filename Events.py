from tkinter import *
import random
import time

def format_number(num):
    if abs(num) >= 1_000_000_000_000_000_000:
        return f"{num / 1_000_000_000_000_000_000:.2f}Qn"
    elif abs(num) >= 1_000_000_000_000_000:
        return f"{num / 1_000_000_000_000_000:.2f}Qd"
    elif abs(num) >= 1_000_000_000_000:
        return f"{num / 1_000_000_000_000:.2f}T"
    elif abs(num) >= 1_000_000_000:
        return f"{num / 1_000_000_000:.2f}B"
    elif abs(num) >= 1_000_000:
        return f"{num / 1_000_000:.2f}M"
    elif abs(num) >= 1_000:
        return f"{num / 1_000:.2f}K"
    else:
        return str(round(num))

class Event:
    def __init__(self, game):
        self.game = game
        self.tk = Toplevel(self.game.tk)
        self.tk.title("Event")
        self.tk.resizable(0,0)
        self.tk.wm_attributes("-topmost", 1)
        self.done = True
        self.main_frame = Frame(self.tk)
        self.main_frame.pack(fill=BOTH, expand=1)
        self.tk.config(bg="black")
        self.treats = self.game.treats
        self.treats_var = StringVar()
        self.treats_var.set(f"Treats: {format_number(self.treats)}")
        self.treats_text = Label(self.main_frame, textvariable=self.treats_var, \
                                 font=("Impact", 30, "bold"), bg="white")
        self.treats_text.pack(side=TOP, fill=X)
        self.cash_multi = self.game.luck_multi
        self.luck_multi = self.game.luck_multi
        #Canvas
        self.canvas_container = Frame(self.main_frame)
        self.canvas_container.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self.canvas_container, width=400, height=300, \
                             highlightthickness=0)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=1)
        self.canvas.config(bg="black")
        #Background
        self.mouth = self.canvas.create_oval(0, 100, 400, 300, outline="black", \
                                         fill = "yellow")
        bgprt1 = self.canvas.create_rectangle(0, 100, 400, 200, fill="black")
        bgprt2 = self.canvas.create_polygon(40, 200, 70, 240, 100, 200, width=2)
        bgprt3 = self.canvas.create_polygon(140, 200, 170, 225, 200, 200, width=2)
        bgprt4 = self.canvas.create_polygon(280, 200, 310, 260, 340, 200, width=2)
        self.eye_1 = self.canvas.create_polygon(50, 60, 30, 150, 170, 150, fill="yellow", width=2)
        self.eye_2 = self.canvas.create_polygon(350, 60, 370, 150, 230, 150, fill="yellow", width=2)
        #Increase multiplyer button
        self.buy_text = self.canvas.create_text(200,250, text = "FEED",font=("Impact", 50, "bold"),\
                                                        fill="orange")
        #Tag binds
        self.canvas.tag_bind(self.mouth, "<Enter>", self.enter_buy)
        self.canvas.tag_bind(self.mouth, "<Leave>", self.leave_buy)
        self.canvas.tag_bind(self.buy_text, "<Enter>", self.enter_buy)
        self.canvas.tag_bind(self.buy_text, "<Leave>", self.leave_buy)
        self.canvas.tag_bind(self.mouth, "<Button-1>", self.buy)
        self.canvas.tag_bind(self.buy_text, "<Button-1>", self.buy)

    def buy(self, event):
        if self.done == True:
            self.done = False
            self.canvas.itemconfig(self.mouth, fill="yellow")
            self.canvas.itemconfig(self.buy_text, fill="orange")
            if self.treats >= 1000000:
                self.treats-=1000000
                upgrades = 1000000 
            elif self.treats >= 100000:
                self.treats-=100000
                upgrades = 100000 
            elif self.treats >= 10000:
                self.treats-=10000
                upgrades = 10000 
            elif self.treats >= 1000:
                self.treats-=1000
                upgrades = 1000 
            elif self.treats >= 100:
                self. treats -= 100
                upgrades = 100
            elif self.treats >= 10:
                self.treats -= 10
                upgrades = 10
            elif self.treats >= 1:
                self.treats -= 1
                upgrades = 1
            else:
                upgrades = 0
            self.treats_var.set(f"Treats: {format_number(self.treats)}")
            percent = random.random()
            other_percent = 1 - random.random()
            cash_total = upgrades * percent
            luck_total = upgrades * other_percent
            self.cash_multi += cash_total * 0.01
            self.luck_multi += luck_total * 0.01
            self.game.cash_multi = self.cash_multi
            self.game.luck_multi = self.luck_multi
            self.done = True
    def enter_buy(self, event):
        if self.done == True:
            self.canvas.itemconfig(self.mouth, fill="orange")
            self.canvas.itemconfig(self.buy_text, fill="yellow")
    def leave_buy(self, event):
        self.canvas.itemconfig(self.mouth, fill="yellow")
        self.canvas.itemconfig(self.buy_text, fill="orange")
        

