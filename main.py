import datetime
import json

import pyglet
from PIL import Image

import customtkinter as ctk
from customtkinter import CTkLabel, CTkButton, CTkImage, CTkFrame, CTkOptionMenu, CTkFont, StringVar, CTkInputDialog

from stats import stats
import Reaction
import SpatialGame
from MemoryGame import Memory
from TextColor import ColorText

pyglet.font.add_file('Assets\\LEMONMILK-Bold.otf')

class Home(ctk.CTk):
    LemonMilk = lambda size: CTkFont('LEMONMILK-Bold', size)
    PerfectIsland = lambda size: CTkFont('Perfect island', size)

    def __init__(self):
        super().__init__()
        self.geometry('800x600')

        self.USERS = list(json.load(open('Database/user_stats.json')).keys()) + ['+ Add User']
        self.CurrentUser = StringVar(value=self.USERS[0])

        self.tools = CTkFrame(self, fg_color='#222222')
        self.tools.place(relx=0, rely=0, relheight=0.2, relwidth=1)

        CTkButton(
            self.tools, fg_color='#BBBBBA', width=80, height=80, text='',
            image=CTkImage(Image.open("Assets/Icons/Stats.png"), size=(32, 32)),
            command=lambda: stats(self.CurrentUser.get())
        ).place(x=20, y=20)

        CTkLabel(self.tools, text_color='#fffffe', font=Home.PerfectIsland(80), text='The Brain').place(x=140, y=5)

        self.profileMenu = CTkOptionMenu(self.tools,
                                         fg_color='#333333',
                                         button_color='#555555',
                                         command=lambda user: self.changeUser(user),
                                         width=200, values=self.USERS,
                                         corner_radius=0,
                                         font=('Arial Bold', 15))
        self.profileMenu.pack(expand='y', anchor='e', padx=20)

        self.brain = CTkFrame(self)
        self.brain.place(relx=0, rely=0.2, relheight=0.8, relwidth=1)

        CTkLabel(self.brain, image=CTkImage(Image.open("Assets/BrainParts.png"), size=(500, 425)), text='').place(
            relx=0.5,
            rely=0.5,
            relwidth=1,
            relheight=1,
            anchor='center')

        CTkButton(self.brain, text='', image=CTkImage(Image.open("Assets/Icons/Cognition.png"), size=(60, 60)),
                  corner_radius=45, fg_color='#74a6d7', border_color='Black',
                  command=lambda: self.getScore('MemoryGame', Memory().runApp()), border_width=3).place(relx=0.9,
                                                                                                        rely=0.6,
                                                                                                        relheight=0.15,
                                                                                                        relwidth=0.15,
                                                                                                        anchor='center')
        CTkButton(self.brain, text='', image=CTkImage(Image.open("Assets/Icons/Reaction.png"), size=(60, 60)),
                  corner_radius=45, fg_color='#f02521', border_color='Black',
                  command=lambda: self.getScore('ReactionGame', Reaction.runApp()), border_width=3).place(relx=0.15,
                                                                                                          rely=0.3,
                                                                                                          relheight=0.15,
                                                                                                          relwidth=0.15,
                                                                                                          anchor='center')
        CTkButton(self.brain, text='', image=CTkImage(Image.open("Assets/Icons/Brain.png"), size=(60, 60)),
                  corner_radius=45,
                  fg_color='#ba5da3',
                  command=lambda: self.getScore('SpatialGame', SpatialGame.runApp()), border_width=3,
                  border_color='Black').place(relx=0.4, rely=0.75, relheight=0.15,
                                              relwidth=0.15,
                                              anchor='center')
        CTkButton(self.brain, text='', image=CTkImage(Image.open("Assets/Icons/Ear.png"), size=(60, 60)),
                  corner_radius=45,
                  fg_color='#fed724', border_width=3, border_color='Black',
                  command=lambda: self.getScore('ColorGame', ColorText().runApp())).place(relx=0.8, rely=0.2,
                                                                                          relheight=0.15, relwidth=0.15,
                                                                                          anchor='center')

    def changeUser(self, user):
        if user == '+ Add User':
            stats = json.load(open('Database/user_stats.json', 'r'))

            newUser = CTkInputDialog(text='New User\'s Name', title='ADD USER')

            self.CurrentUser.set(newUser.get_input())
            self.USERS.insert(-1, self.CurrentUser.get())

            self.profileMenu.configure(values=self.USERS)
            stats[self.CurrentUser.get()] = {g: dict() for g in
                                             ['ReactionGame', 'SpacialGame', 'ColorGame', 'MemoryGame']}

            json.dump(stats, open('Database/user_stats.json', 'w'), indent=4)

            self.update()

        self.CurrentUser.set(user)

    def getScore(self, game, value):

        stats = json.load(open('Database/user_stats.json', 'r'))

        oldVal = stats[self.CurrentUser.get()][game].get(str(datetime.date.today()))

        stats[self.CurrentUser.get()][game][str(datetime.date.today())] = max(value, oldVal) if oldVal else value

        json.dump(stats, open('Database/user_stats.json', 'w'), indent=4)


Home().mainloop()
