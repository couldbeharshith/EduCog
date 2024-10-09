import random
from customtkinter import CTk, CTkFont, CTkButton, CTkLabel, CTkFrame


class ColorText(CTk):

    LemonMilk = lambda size: CTkFont('LEMONMILK-Bold', size)

    def __init__(self):
        super().__init__()
        self.geometry('800x500')

        self.colors = ['#FD4239','#88B04B','#6aa7ff','#FFE72B']
        self.texts = ['Red', 'Green', 'Blue', 'Yellow']

        self.scoreRegion = CTkFrame(self, corner_radius=0, fg_color='#242528')
        self.scoreRegion.place(relx=0, rely=0, relwidth=1, relheight=0.25)

        self.gameRegion = CTkFrame(self, corner_radius=0)
        self.gameRegion.place(relx=0, rely=0.25, relwidth=1, relheight=0.75)

        self.scoreLabel = CTkLabel(self.scoreRegion, font=ColorText.LemonMilk(50), text = 0)
        self.scoreLabel.place(relx = 0.5, rely = 0.5, anchor = 'center')

        self.compareText = CTkLabel(self.gameRegion, font=ColorText.LemonMilk(56))
        self.compareColor = CTkLabel(self.gameRegion, font=ColorText.LemonMilk(56))

        CTkLabel(self.gameRegion, font=ColorText.LemonMilk(12), text = 'Text').place(relx = 0.3, rely = 0.2, anchor = 'n')
        CTkLabel(self.gameRegion, font=ColorText.LemonMilk(12), text = '=').place(relx = 0.5, rely = 0.2, anchor = 'n')
        CTkLabel(self.gameRegion, font=ColorText.LemonMilk(12), text = 'Color').place(relx = 0.7, rely = 0.2, anchor = 'n')

        self.compareColor.place(relx=0.7, rely=0.1, relwidth=0.4, relheight=0.2, anchor='center')
        self.compareText.place(relx=0.3, rely=0.1, relwidth=0.4, relheight=0.2, anchor='center')

        CTkButton(self,
                  text = 'Match!',
                  font=ColorText.LemonMilk(25),
                  fg_color = '#32CD32',
                  text_color='Black',
                  command=lambda val=True: self.newInput(val)
                  ).place(relx = 0.3, rely = 0.8, relwidth = 0.3, relheight = 0.2, anchor = 'center')
        CTkButton(self,
                  text = 'Incorrect!',
                  font=ColorText.LemonMilk(25),
                  fg_color='#ec3434',
                  text_color='Black',
                  command=lambda val=False: self.newInput(val)
                  ).place(relx = 0.7, rely = 0.8, relwidth = 0.3, relheight = 0.2, anchor = 'center')

        self.points = 0
        self.attempts = 0

        self.colorIndex = None
        self.textIndex = None

        self.changeColor()

    def changeColor(self):

        self.textIndex = int(random.random() * len(self.texts))
        self.colorIndex = int(random.random() * len(self.colors))

        newText = self.texts[self.textIndex]
        newColor = self.colors[self.colorIndex]

        fakeText = [i for i in self.texts if i != newText][int(random.random() *(len(self.texts)-1))]
        fakeColor = [i for i in self.colors if i != newColor][int(random.random() * (len(self.colors)-1))]

        self.compareColor.configure(text=fakeText, text_color=newColor)
        self.compareText.configure(text=newText, text_color=fakeColor)

    def newInput(self, inp:bool):

        if inp == (self.colorIndex == self.textIndex):
            self.points += 1
            self.scoreLabel.configure(text = self.points, text_color='#32CD32')
        else:
            self.scoreLabel.configure(text_color='#ec3434')

        self.attempts += 1
        if self.attempts > 40:
            self.destroy()

        self.changeColor()
        self.update()

    def runApp(self):

        self.mainloop()

        return 100*(self.points/(self.attempts or 1))
