import random
import time
from tkinter import *
import pandas as pd

class loads:
    def __init__(self):
        global df
        #Get Data
        df = pd.read_csv("GameMainFrame.csv")
        self.row = 0
        #Make login window
        self.tk = Tk()
        self.tk.title("Login")
        self.tk.resizable(0,0)
        self.tk.wm_attributes("-topmost", 1)
        #Input box creation
        self.label = Label(self.tk, text="Enter Username")
        self.label.pack(pady=5)
        self.input_box = Entry(self.tk, width=50)
        self.input_box.pack(pady = 5)
        self.label1 = Label(self.tk, text="Enter password")
        self.label1.pack(pady=5)
        self.input_box1 = Entry(self.tk, width=50)
        self.input_box1.pack(pady=5)
        self.enter_button1 = Button(self.tk, text="Login", command=self.read_all)
        self.enter_button1.pack(pady=5)
        self.create_new_button = Button(self.tk, text="Create New Acount", command=self.create_new_account)
        self.create_new_button.pack(pady = 5)
        self.access_granted = False
        #Start main loop
        self.tk.mainloop()
    def read_all(self):
        global df
        self.answer = self.input_box.get()
        self.answer1 = self.input_box1.get()
        try:
            self.row = df[df["Username"] == self.answer].index[0]
            if self.answer1 == df.loc[self.row, 'Password']:
                self.tk.destroy()
                self.access_granted = True
        except Exception as e:
            self.fail = e
    def create_new_account(self):
        #Recreate Window
        self.tk.destroy()
        self.tk = Tk()
        self.tk.title("Create New Account")
        self.tk.resizable(0,0)
        self.tk.wm_attributes("-topmost", 1)
        #Input box creation
        self.label = Label(self.tk, text="Enter Username")
        self.label.pack(pady=5)
        self.input_box = Entry(self.tk, width=50)
        self.input_box.pack(pady = 5)
        self.label1 = Label(self.tk, text="Enter password")
        self.label1.pack(pady=5)
        self.input_box1 = Entry(self.tk, width=50)
        self.input_box1.pack(pady=5)
        self.button = Button(self.tk, text="Create", command=self.create_account)
        self.button.pack(pady = 5)
        #Main Loop
        self.tk.mainloop()
    def create_account(self):
        self.answer = self.input_box.get()
        self.answer1 = self.input_box1.get()
        try:
            if not df['Username'].eq(self.answer).any() == True:
                df.loc[len(df)] = [0.0, 0.0, 10, 1, 100, 1, 100, time.time(), 1, self.answer, self.answer1]
                self.row = len(df) - 1
                self.access_granted = True
                self.tk.destroy()
        except Exception as e:
            self.failure = e
    def load_game(self):
        global df
        stuff = []
        for i in range(9):
            stuff.append(df.iat[self.row,i])
        return stuff
    def save_game(self, gameclass):
        global df
        print("Saving...")
        df.iloc[self.row,0] = gameclass.cash
        df.iloc[self.row,1] = gameclass.cps
        df.iloc[self.row,2] = gameclass.cps_cost
        df.iloc[self.row,3] = gameclass.cm
        df.iloc[self.row,4] = gameclass.cm_cost
        df.iloc[self.row,5] = gameclass.cv
        df.iloc[self.row,6] = gameclass.cv_cost
        df.iloc[self.row,7] = time.time()
        df.iloc[self.row,8] = gameclass.luck
        with open("GameMainFrame.csv","w") as f:
            f.write("Saving...")
        df.to_csv('GameMainFrame.csv', index=False)
