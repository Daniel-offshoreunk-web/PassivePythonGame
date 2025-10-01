from tkinter import *
import time
import random
from LoadsClass import *
from ResetCSV import *
from Achivements import *

#Format Number Function
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

class Game:
    def __init__(self):
        global l
        #Main Frame and other
        self.tk = Tk()
        self.tk.title("Clicker Game")
        self.tk.resizable(0,0)
        self.tk.wm_attributes("-topmost", 1)
        self.last_click_time = time.time()
        self.cooldowntime = 0.5
        self.main_frame = Frame(self.tk)
        self.main_frame.pack(fill=BOTH, expand=1)
        self.luck_boost_used = False
        self.super_luck_boost_used = False
        self.bt_luck = 0
        self.sbt_luck = 0

        #Load game data on startup
        game_data = l.load_game()
        self.cash = game_data[0]
        self.cps = game_data[1]
        self.cps_cost = game_data[2]
        self.cm = game_data[3]
        self.cm_cost = game_data[4]
        self.cv = game_data[5]
        self.cv_cost = game_data[6]
        offlinetime = time.time() - game_data[7]
        offlinecash = offlinetime / 2
        self.cash += self.cps * offlinecash
        self.luck = game_data[8]
        string11 = str(game_data[9])
        self.bools = achivements.breaktobool(string11)
        self.prestiges = game_data[10]
        self.drawsingame = 0
        if offlinetime > 3600:
            self.bools[10] = True
        
        #Cash
        self.cash_var = StringVar()
        self.cash_var.set(f"Cash: ${format_number(self.cash)}")
        self.cash_text = Label(self.main_frame, textvariable=self.cash_var, \
                                 font=("Impact", 30, "bold"))
        self.cash_text.pack(side=TOP, fill=X)

        #Container
        self.canvas_container = Frame(self.main_frame)
        self.canvas_container.pack(fill=BOTH, expand=1)

        #Canvas
        self.canvas = Canvas(self.canvas_container, width=500, height=500, highlightthickness=0)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=1)

        #Button
        self.button_rect = self.canvas.create_rectangle(300, 400, 500, 500, \
                                                    fill="green", \
                                                    outline='black')
        self.button_text = self.canvas.create_text(400, 450, text="Draw",\
                                                   fill="black", \
                                                   font=("Impact", 55, "bold"))
        #Upgrade Cps
        self.upgrade_button_rect =  self.canvas.create_rectangle(250, 300, 500, 400, fill="cyan3", \
                                                                 outline="black")
        self.upgrade_button_text = self.canvas.create_text(375, 350, text='Upgrade CPS',\
                                                           fill="black", \
                                                           font=("Impact",25,"bold"))
        #Upgrade Cps%
        self.cm_upgrade_button_rect = self.canvas.create_rectangle(0, 300, 250, 400, fill="cyan3", \
                                                                   outline="black")
        self.cm_upgrade_button_text = self.canvas.create_text(125, 350, text="Upgrade CPS%",\
                                                           fill="black", font=("Impact",25,"bold"))
        #Upgrade Card Value & Luck
        self.cv_upgrade_button_rect = self.canvas.create_rectangle(0, 200, 250, 300, fill="green", \
                                                                   outline="black")
        self.cv_upgrade_button_text = self.canvas.create_text(125, 250, text="""Upgrade
Gambling""",\
                                                           fill="black", font=("Impact",25,"bold"))

        #Results Box
        self.carddrawn = ""
        self.result_rect = self.canvas.create_rectangle(0,400,300,500, \
                                                        fill="white", \
                                                        outline="black")
        self.result_text = self.canvas.create_text(150,450, text="", fill="black",\
                                                   font=("Impact",45, "bold"))

        #Cover for Output
        self.animate_rect = self.canvas.create_rectangle(0, 500, 300, 600, \
                                                         fill = "black", \
                                                         outline = "black")

        #Achivements Button
        self.a_button_rect = self.canvas.create_rectangle(250, 200, 500, 300, fill="yellow3", \
                                                          outline="black")
        self.a_button_text = self.canvas.create_text(375, 250, text="Achivements", fill="black",\
                                                     font=("Impact", 25, "bold"))

        #Info
        self.list_frame = Frame(self.canvas, background="#FFFFFF", width=10, height=20)
        self.canvas.create_window((0, 0), window=self.list_frame, anchor="nw")

        self.scrollbar = Scrollbar(self.list_frame)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        
        self.info_list = Text(self.list_frame, wrap="word", font=("Comic Sans MS", 12), height=8, width=10, yscrollcommand=self.scrollbar.set)
        self.info_list.pack(padx=5, pady=5, side=LEFT, fill="both", expand=True)

        self.scrollbar.config(command=self.info_list.yview)

        def on_canvas_configure(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.list_frame.bind("<Configure>", on_canvas_configure)

        #Bind Buttons
        self.canvas.tag_bind(self.button_rect, "<Button-1>", self.ondraw)
        self.canvas.tag_bind(self.button_text, "<Button-1>", self.ondraw)
        self.canvas.tag_bind(self.button_rect, "<Enter>", self.enter_draw)        
        self.canvas.tag_bind(self.button_rect, "<Leave>", self.leave_draw)
        self.canvas.tag_bind(self.button_text, "<Enter>", self.enter_draw)
        self.canvas.tag_bind(self.button_text, "<Leave>", self.leave_draw)
        self.canvas.tag_bind(self.upgrade_button_rect, "<Button-1>", self.cpsupgrade)
        self.canvas.tag_bind(self.upgrade_button_text, "<Button-1>", self.cpsupgrade)
        self.canvas.tag_bind(self.upgrade_button_rect, "<Enter>", self.enter_cps)
        self.canvas.tag_bind(self.upgrade_button_rect, "<Leave>", self.leave_cps)
        self.canvas.tag_bind(self.upgrade_button_text, "<Enter>", self.enter_cps)
        self.canvas.tag_bind(self.upgrade_button_text, "<Leave>", self.leave_cps)
        self.canvas.tag_bind(self.cm_upgrade_button_rect, "<Button-1>", self.cmupgrade)
        self.canvas.tag_bind(self.cm_upgrade_button_text, "<Button-1>", self.cmupgrade)
        self.canvas.tag_bind(self.cm_upgrade_button_rect, "<Enter>", self.cm_enter)
        self.canvas.tag_bind(self.cm_upgrade_button_rect, "<Leave>", self.cm_leave)
        self.canvas.tag_bind(self.cm_upgrade_button_text, "<Enter>", self.cm_enter)
        self.canvas.tag_bind(self.cm_upgrade_button_text, "<Leave>", self.cm_leave)
        self.canvas.tag_bind(self.cv_upgrade_button_rect, "<Button-1>", self.cvupgrade)
        self.canvas.tag_bind(self.cv_upgrade_button_text, "<Button-1>", self.cvupgrade)
        self.canvas.tag_bind(self.cv_upgrade_button_rect, "<Enter>", self.enter_cv)
        self.canvas.tag_bind(self.cv_upgrade_button_rect, "<Leave>", self.leave_cv)
        self.canvas.tag_bind(self.cv_upgrade_button_text, "<Enter>", self.enter_cv)
        self.canvas.tag_bind(self.cv_upgrade_button_text, "<Leave>", self.leave_cv)
        self.canvas.tag_bind(self.a_button_rect, "<Button-1>", self.achivements)
        self.canvas.tag_bind(self.a_button_text, "<Button-1>", self.achivements)
        self.canvas.tag_bind(self.a_button_rect, "<Enter>", self.enter_a)
        self.canvas.tag_bind(self.a_button_rect, "<Leave>", self.leave_a)
        self.canvas.tag_bind(self.a_button_text, "<Enter>", self.enter_a)
        self.canvas.tag_bind(self.a_button_text, "<Leave>", self.leave_a)
        

        #Save on Exit
        self.tk.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Start the cash update loop
        self.tk.after(1000, self.update_cash_display)

    def on_closing(self):
        global l
        l.save_game(self, achivements.fusetobool(self.bools))
        self.tk.destroy()

    def cooldown(self):
        if time.time() - self.last_click_time >= self.cooldowntime:
            self.last_click_time = time.time()
            return True
        else:
            return False
    def rarity(self, color, name, number, req, extra, reveal_color):
        if self.draw_chance > req:
            self.canvas.itemconfigure(self.result_rect, fill=color)
            self.canvas.itemconfigure(self.result_text, text=name, fill="black")
            self.canvas.itemconfigure(self.animate_rect, fill=reveal_color)
            self.cash += number * self.cv
            if not extra == '':
                exec(extra)
    def raritynew(self, color, name, number, req, extra, reveal_color):
        if self.draw_chance > req:
            self.canvas.itemconfigure(self.result_rect, fill=color)
            self.canvas.itemconfigure(self.result_text, text=name, fill="black")
            self.canvas.itemconfigure(self.animate_rect, fill=reveal_color)
            self.cash += number * self.cv
            if not extra == '':
                exec(extra)
    def reveal(self):
        if self.current_pos > 0:
            self.canvas.move(self.animate_rect, 0, 1)
            self.current_pos -= 1
            self.tk.after(2, self.reveal)
    def ondraw(self, event):
        self.bools[1] = True
        self.drawsingame += 1
        if self.drawsingame >= 100:
            self.bools[7] = True
        if self.drawsingame >= 1000:
            self.bools[8] = True
        if self.cooldown() == True:
            self.canvas.move(self.animate_rect, 0, -100)
            self.current_pos = 100
            self.reveal()
            top_chance = 0
            draws = 1
            if self.luck >= 1:
                draws = self.luck
            draws = round(draws)
            percentile = 100 / draws
            chance = random.random() * percentile
            maxedchance = 100 - percentile
            top_chance = maxedchance + chance
            self.draw_chance = top_chance
            self.rarity("grey", "Common", 1, 0,'', "black")
            self.rarity("Lightgreen", "Uncommon", 2, 50,'', "black")
            self.rarity("Lightblue", "Rare", 7, 75,'', "black")
            self.rarity("purple", "Epic", 40, 83.5,'', "black")
            self.rarity("red", "Mythic", 100, 92, '', "red")
            self.rarity("yellow", "Legendary", 150, 95,'', "red")
            self.rarity("black", "Unknown-", 700, 98,'self.canvas.itemconfigure(self.result_text, fill="white")', "red")
            self.rarity("black", "Unknown", 4000, 99.5, 'self.canvas.itemconfigure(self.result_text, fill="white")', "red")
            self.rarity("black", "Unknown+", 45000, 99.75, 'self.canvas.itemconfigure(self.result_text, fill="white")', "red")
            self.rarity("cyan", "Immortal-", 450000, 99.9, '', "yellow")
            self.rarity("cyan", "Immortal", 4500000, 99.925, 'self.bools[3] = True', "yellow")
            self.rarity("cyan", "Immortal+", 45000000, 99.99, '', "yellow")
            self.rarity("white", "Beyond-", 450000000, 99.999, '', "yellow")
            self.rarity("white", "Beyond", 4500000000, 99.99975, '', "yellow")
            self.rarity("white", "Beyond+", 45000000000, 99.99999, '', "yellow")
            self.rarity("red", "Infernal-", 450000000000, 99.9999975, '', "cyan")
            self.rarity("red", "Infernal", 4500000000000, 99.9999995, '', "cyan")
            self.rarity("red", "Infernal+", 45000000000000, 99.9999999, '', "cyan")
            self.rarity("yellow", "Celestial-", 450000000000000, 99.999999975, '', "cyan")
            self.rarity("yellow", "Celestial", 4500000000000000, 99.999999995, '', "cyan")
            self.rarity("yellow", "Celestial+", 4500000000000000, 99.999999999, 'self.bools[4] = True', "cyan")
            self.rarity("green", "DONE!", -5000000000000000, 99.9999999999, 'self.prestige_time()', "black")
            self.cash_var.set(f"Cash: ${format_number(self.cash)}")

    def cpsupgrade(self, event):
        self.bools[2] = True
        if self.cooldown() == True:
            cash_available = self.cash
            cost_of_next_upgrade = self.cps_cost
            upgrades_to_buy = 0
            total_cost = 0
            if not cash_available >= 1000 * cost_of_next_upgrade:
                while cash_available >= cost_of_next_upgrade:
                    cash_available -= cost_of_next_upgrade
                    total_cost += cost_of_next_upgrade
                    cost_of_next_upgrade += 5
                    upgrades_to_buy += 1
            elif not cash_available >= 1000000:
                while cash_available >= cost_of_next_upgrade * 100:
                    cash_available -= 100 * cost_of_next_upgrade
                    total_cost += 100 * cost_of_next_upgrade
                    cost_of_next_upgrade += 500
                    upgrades_to_buy += 100
                        
            else:
                while cash_available >= cost_of_next_upgrade * 100000:
                    cash_available -= 100000 * cost_of_next_upgrade
                    total_cost += 100000 * cost_of_next_upgrade
                    cost_of_next_upgrade += 500000
                    upgrades_to_buy += 100000
            if upgrades_to_buy > 0:
                ogcps = self.cps
                self.cash -= total_cost
                self.cash_var.set(f"Cash: ${format_number(self.cash)}")
                self.cps += upgrades_to_buy
                full_string = f"Cps upgraded from {format_number(ogcps)} to {format_number(self.cps)}."
                self.info_list.insert("0.0", full_string+'\n')
            else:
                full_string = f"You need ${format_number(self.cps_cost)} to upgrade this."
                self.info_list.insert("0.0", full_string+'\n')
                
    def cmupgrade(self, event):
        if self.cooldown() == True:   
            if self.cash>=self.cm_cost:
                self.cash -= self.cm_cost
                self.cm_cost = self.cm_cost * 2
                self.cash_var.set(f"Cash: ${format_number(self.cash)}")
                ogcm = self.cm
                self.cm += 1
                full_string = f"Cps% upgraded from {ogcm} to {self.cm}."
                self.info_list.insert("0.0", full_string+'\n')
            else:
                full_string = f"You need ${format_number(self.cm_cost)} to upgrade this."
                self.info_list.insert("0.0", full_string+'\n')

    def cvupgrade(self, event):
        self.bools[6] = True
        if self.cooldown() == True:
            if self.cash > self.cv_cost or self.cash == self.cv_cost:
                self.cash -= self.cv_cost
                self.cv_cost = self.cv_cost * 10
                self.cash_var.set(f"Cash: ${format_number(self.cash)}")
                ogcv = self.cv
                self.cv += 1
                self.luck *= 2
                full_string = f"Card value and luck upgraded from {ogcv} to {self.cv}."
                self.info_list.insert("0.0", full_string+'\n')
            else:
                full_string = f"You need ${format_number(self.cv_cost)} to upgrade this."
                self.info_list.insert("0.0", full_string+'\n')
    def achivements(self, event):
        self.a = achivements()
        self.a.check_all(self.bools)

    def luck_boost(self):
        self.luck *= 2
        self.bt_luck += 300
        self.luck_boost_used = True

    def super_luck_boost(self):
        self.luck *= 10
        self.sbt_luck += 300
        self.auper_luck_boost_used = True
        self.bools[5] = True
        
    def update_cash_display(self):
        #Also manages boosts and prestige
        self.cash += self.cps * self.cm
        self.cash_var.set(f"Cash: ${format_number(self.cash)}")
        
        if random.random() >= 0.998:
            self.info_list.insert("0.0","Luck boost is activate for five minutes!\n")
            self.luck_boost()
        if random.random() >= 0.9995:
            self.info_list.insert("0.0","Super luck boost is active for five minutes!\n")
            self.super_luck_boost()
        if self.bt_luck == 0 and self.luck_boost_used == True:
            self.luck /= 2
            self.luck_boost_used = False
        if self.sbt_luck == 0 and self.super_luck_boost_used == True:
            self.luck /= 10
            self.super_luck_boost_used = False
        if not self.bt_luck == 0:
            self.bt_luck -= 1
        if not self.sbt_luck == 0:
            self.sbt_luck -= 1
        if self.cash >= 1000000000000000000:
            self.prestige_time()
        
        # Schedule the next call to this function after 1000ms (1 second)
        self.tk.after(1000, self.update_cash_display)
    def prestige_time(self):
        self.button_rect = self.canvas.create_rectangle(300, 400, 500, 500, \
                                                    fill="white", \
                                                    outline='black')
        self.button_text = self.canvas.create_text(400, 450, text="PRESTIGE",\
                                                   fill="black", \
                                                   font=("Impact", 38, "bold"))
        self.canvas.tag_bind(self.button_rect, "<Button-1>", self.prestige)
        self.canvas.tag_bind(self.button_text, "<Button-1>", self.prestige)
        self.canvas.tag_bind(self.button_rect, "<Enter>", self.enter_p)        
        self.canvas.tag_bind(self.button_rect, "<Leave>", self.leave_p)
        self.canvas.tag_bind(self.button_text, "<Enter>", self.enter_p)
        self.canvas.tag_bind(self.button_text, "<Leave>", self.leave_p)
    def prestige(self, event):
        self.bools[9] = True
        self.prestiges += 1
        self.cash = 0
        self.cps = 0
        self.cps_cost = 10
        if self.prestiges == 3:
            self.info_list.insert("0.0", "You now gain cps boost from prestige!\n")
        if self.prestiges>= 3:
            from3 = self.prestiges - 2
            self.cm = from3 * 3
        else:
            self.cm = 1
        self.cm_cost = 100
        self.cv = 1
        self.cv_cost = 100
        if self.prestiges == 1:
            self.info_list.insert("0.0", "I wonder if you'll get more boost later...\n")
            self.info_list.insert("0.0", "You currently gain luck boost from prestige.\n")
        self.luck = self.prestiges
        self.button_rect = self.canvas.create_rectangle(300, 400, 500, 500, \
                                                    fill="green", \
                                                    outline='black')
        self.button_text = self.canvas.create_text(400, 450, text="Draw",\
                                                   fill="black", \
                                                   font=("Impact", 55, "bold"))
        self.canvas.tag_bind(self.button_rect, "<Button-1>", self.ondraw)
        self.canvas.tag_bind(self.button_text, "<Button-1>", self.ondraw)
        self.canvas.tag_bind(self.button_rect, "<Enter>", self.enter_draw)        
        self.canvas.tag_bind(self.button_rect, "<Leave>", self.leave_draw)
        self.canvas.tag_bind(self.button_text, "<Enter>", self.enter_draw)
        self.canvas.tag_bind(self.button_text, "<Leave>", self.leave_draw)
        
    def enter_draw(self, event):
        self.canvas.itemconfigure(self.button_rect, fill="green3")
    def leave_draw(self, event):
        self.canvas.itemconfigure(self.button_rect, fill="green")
    def enter_cps(self, event):
        self.canvas.itemconfigure(self.upgrade_button_rect, fill="cyan")
    def leave_cps(self, event):
        self.canvas.itemconfigure(self.upgrade_button_rect, fill="cyan3")
    def cm_enter(self, event):
        self.canvas.itemconfigure(self.cm_upgrade_button_rect, fill="cyan")
    def cm_leave(self, event):
        self.canvas.itemconfigure(self.cm_upgrade_button_rect, fill="cyan3")
    def enter_cv(self, event):
        self.canvas.itemconfigure(self.cv_upgrade_button_rect, fill="green3")
    def leave_cv(self, event):
        self.canvas.itemconfigure(self.cv_upgrade_button_rect, fill="green")
    def enter_a(self, event):
        self.canvas.itemconfigure(self.a_button_rect, fill="yellow")
    def leave_a(self, event):
        self.canvas.itemconfigure(self.a_button_rect, fill="yellow3")
    def enter_p(self, event):
        self.canvas.itemconfigure(self.button_rect, fill="black")
        self.canvas.itemconfigure(self.button_text, fill="white")
    def leave_p(self, event):
        self.canvas.itemconfigure(self.button_rect, fill="white")
        self.canvas.itemconfigure(self.button_text, fill="black")
        

try:
    with open("GameMainFrame.csv", "r") as f:
        f.close
except Exception as e:
    reset()
l = loads()
if l.access_granted == True:
    g = Game()
    g.tk.mainloop()
