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
        self.tk.configure(bg='lightblue')
        #Input box creation
        self.label = Label(self.tk, text="Enter Username", bg='lightblue', font = ("Impact", 10, ""))
        self.label.pack(pady=5)
        self.input_box = Entry(self.tk, width=30)
        self.input_box.pack(pady = 5, padx = 10)
        self.label1 = Label(self.tk, text="Enter password", bg='lightblue', font = ("Impact", 10, ""))
        self.label1.pack(pady=5)
        self.input_box1 = Entry(self.tk, width=30)
        self.input_box1.pack(pady=5, padx=10)
        self.enter_button1 = Button(self.tk, text="Login", command=self.read_all, bg="green", font = ("Impact", 10, ""))
        self.enter_button1.pack(pady=5)
        self.enter_button1.bind("<Enter>", lambda event: self.buttoncolorchange(event, self.enter_button1, "green3"))
        self.enter_button1.bind("<Leave>", lambda event: self.buttoncolorchange(event, self.enter_button1, "green"))
        self.create_new_button = Button(self.tk, text="Create New Acount", command=self.create_new_account, bg="green", font = ("Impact", 10, ""))
        self.create_new_button.bind("<Enter>", lambda event: self.buttoncolorchange(event, self.create_new_button, "green3"))
        self.create_new_button.bind("<Leave>", lambda event: self.buttoncolorchange(event, self.create_new_button, "green"))
        self.create_new_button.pack(pady = 5)
        self.access_granted = False
        #Start main loop
        self.tk.mainloop()
    def buttoncolorchange(self, event, button, color):
        button.configure(bg = color)
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
        self.tk.configure(bg = "lightblue")
        #Input box creation
        self.label = Label(self.tk, text="Enter Username", bg="lightblue", font = ("Impact", 10, ""))
        self.label.pack(pady=5)
        self.input_box = Entry(self.tk, width=30)
        self.input_box.pack(pady = 5, padx=10)
        self.label1 = Label(self.tk, text="Enter password", bg="lightblue", font = ("Impact", 10, ""))
        self.label1.pack(pady=5)
        self.input_box1 = Entry(self.tk, width=30)
        self.input_box1.pack(pady=5, padx=10)
        self.enter_button1 = Button(self.tk, text="Create", command=self.create_account, bg="green", font = ("Impact", 10, ""))
        self.enter_button1.pack(pady=5)
        self.enter_button1.bind("<Enter>", lambda event: self.buttoncolorchange(event, self.enter_button1, "green3"))
        self.enter_button1.bind("<Leave>", lambda event: self.buttoncolorchange(event, self.enter_button1, "green"))
        #Main Loop
        self.tk.mainloop()
    def create_account(self):
        global df
        self.answer = self.input_box.get()
        self.answer1 = self.input_box1.get()
        try:
            if not df['Username'].eq(self.answer).any() == True:
                newdf = pd.DataFrame({
                    "Cash": [0.0],
                    "Cps": [0.0],
                    "Cps Cost": [10],
                    "Cm": [1],
                    "Cm Cost": [100],
                    "Cv": [1],
                    "Cv_Cost": [100],
                    "Last Online": [time.time()],
                    "Luck": [1],
                    "Username": [self.answer],
                    "Password": [self.answer1],
                    "Achivements": ["100000000000"],
                    "Prestiges": [0],
                    "Treats": [0],
                    "Cash Multi": [1.00],
                    "Luck Multi": [1.00]
                    })
                df = pd.concat([df, newdf], ignore_index=True)
                self.row = len(df.index) -1
                self.access_granted = True
                self.tk.destroy()
        except Exception as e:
            self.failure = e
    def load_game(self):
        global df
        stuff = []
        for i in range(9):
            stuff.append(df.iat[self.row,i])
        for i in range(5):
            stuff.append(df.iat[self.row, i + 11])
        return stuff
    def save_game(self, gameclass, string):
        global df
        df.iloc[self.row,0] = gameclass.cash
        df.iloc[self.row,1] = gameclass.cps
        df.iloc[self.row,2] = gameclass.cps_cost
        df.iloc[self.row,3] = gameclass.cm
        df.iloc[self.row,4] = gameclass.cm_cost
        df.iloc[self.row,5] = gameclass.cv
        df.iloc[self.row,6] = gameclass.cv_cost
        df.iloc[self.row,7] = time.time()
        df.iloc[self.row,8] = gameclass.luck
        df.iloc[self.row,11] = string
        df.iloc[self.row,12] = gameclass.prestiges
        df.iloc[self.row, 13] = gameclass.treats
        df.iloc[self.row, 14] = gameclass.cash_multi
        df.iloc[self.row, 15] = gameclass.luck_multi
        with open("GameMainFrame.csv","w") as f:
            f.write("Saving...")
        df.to_csv('GameMainFrame.csv', index=False)

