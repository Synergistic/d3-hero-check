from Tkinter import Label, Listbox, Entry, Button, Frame, Tk, N, S, END
import tkMessageBox
from d3 import getChars, checkHeroes, checkGear
import csv
import shutil, time
import os, os.path

bnet_accounts = []
hero_list = []
stat_list = []
current_account = None
current_hero = None



class MainWindow(Frame):

    def __init__(self, master):
        bnetLabel = Label(text="Battle.net Accounts")
        bnetLabel.grid(row=1, column=1, sticky=S)
                       
        self.bnetBox = Listbox(master, height=5)
        self.bnetBox.grid(row=2, column=1, sticky=N)
        self.bnetBox.bind('<<ListboxSelect>>', self.get_heroes)                
        
        self.statBox = Listbox(master, width=25, height=6)
        self.statBox.grid(row=3, column=2, rowspan=4)

        heroLabel = Label(text="Heroes")
        heroLabel.grid(row=1, column=2, sticky=S)
        self.heroBox = Listbox(master, width=25, height=8)
        self.heroBox.grid(row=2, column=2, sticky=N)
        self.heroBox.bind('<<ListboxSelect>>', self.get_stats)

        self.new_bnet = Entry()
        self.new_bnet.grid(row=3, column=1, sticky=S)

        self.addButton = Button(text="Add Bnet Account", command=self.add_bnet).grid(row=4, column=1, sticky=N)
        self.addButton = Button(text="Remove Bnet Account", command=self.remove_bnet).grid(row=5, column=1, sticky=N)
        
        self.padding1 = Label(text="  ").grid(row=0,column=0)
        self.padding2 = Label(text="  ").grid(row=7,column=8)

    def get_stats(self, instance):
        global stat_list
        stat_list = []
        hero = str(self.heroBox.get(self.heroBox.curselection())).split(' ')[0]
        bonuses = checkGear(chars[hero])
        for skill in bonuses:
            if bonuses[skill] > 0:
                stat_list.append(' = '.join([skill, (str(bonuses[skill]) + '%')]))
        self.refresh_Box()
                
    def get_heroes(self, instance):
        global hero_list, chars, current_account
        hero_list = []
        bnet = str(self.bnetBox.get(self.bnetBox.curselection()))
        current_account = bnet
        self.bnet = bnet.replace('#', '-')
        chars = getChars(self.bnet, 'us')
        h = checkHeroes(chars)
        for hero in h:
            hero_list.append(' - '.join([hero, h[hero]]))
        self.refresh_Box()
            
    def refresh_Box(self):
        self.bnetBox.delete(0,END)
        self.heroBox.delete(0,END)
        self.statBox.delete(0,END)
        for account in bnet_accounts:
            self.bnetBox.insert(END, account)
        for hero in hero_list:
            self.heroBox.insert(END, hero)
        for stat in stat_list:
            self.statBox.insert(END, stat)

    def save_file(self):
        with open('inv.csv', 'w+') as bnet_accounts_write:
            writer = csv.writer(bnet_accounts_write, dialect='excel')
            for account in bnet_accounts:
                writer.writerow([account])        
                
    def add_bnet(self):
        bnet_accounts.append(str(self.new_bnet.get()))
        self.refresh_Box()
        self.save_file()
    
    def remove_bnet(self):
        bnet_accounts.remove(current_account)
        self.refresh_Box()
        self.save_file()
                
    def callback(self):
        #protocol for dealing with a quit.
        if tkMessageBox.askokcancel("Quit", "Really quit?"):
            root.destroy()


                                    
if __name__ == "__main__":
    #start this shit up
    root = Tk()
    root.title("SKILL DAMAGE BROS")
    bnet_accounts_Buddy = MainWindow(root)

    with open('inv.csv', 'r+') as bnet_accounts_file:
        reader = csv.reader(bnet_accounts_file)
        for row in reader:
            print row
            if len(row)>0:
                name = str(row[0])
                if name not in bnet_accounts:
                    bnet_accounts.append(name)
        bnet_accounts_Buddy.refresh_Box()
        
    root.protocol("WM_DELETE_WINDOW", bnet_accounts_Buddy.callback)   
    root.mainloop()






