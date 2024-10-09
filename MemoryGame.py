import random

from customtkinter import CTk, CTkButton, CTkFont, CTkFrame, CTkLabel
from playsound import playsound


def LemonMilk(size: int):
    return CTkFont('LEMONMILK-Bold', size)


class Memory(CTk):
    def __init__(self):

        super().__init__()
        self.geometry('450x600')

        self.gameRegion = CTkFrame(self, corner_radius=0, fg_color='#1B1B1B')
        self.gameRegion.place(relx=0, rely=0.25, relwidth=1, relheight=0.75)
        self.scoreRegion = CTkFrame(self, corner_radius=0)
        self.scoreRegion.place(relx=0, rely=0, relwidth=1, relheight=0.25)

        self.combination = []
        self.dummyCombination = []

        self.incorrects = 0
        self.score = 0
        self.highScore = 0

        self.scoreLabel = CTkLabel(self.scoreRegion, text='0', font=LemonMilk(56))
        self.scoreLabel.place(relx=0.5, rely=0.5, anchor='center')

        self.buttons = dict()
        for i in range(25):
            self.buttons[i] = CTkButton(
                self.gameRegion,
                text=' ',
                fg_color='#00B7EB',
                command=lambda v=i: self.buttonClick(v)
                )
            self.buttons[i].place(
                relx=0.12 + ((i % 5) * 0.19),
                rely=0.12 + ((i // 5) * 0.19),
                relwidth=0.16,
                relheight=0.16,
                anchor='center'
                )

        self.addOrder()

    def buttonClick(self, val):

        if self.dummyCombination.pop(0) == val:
            self.score += 1
            playsound('Assets/Audio/user_click.mp3')
            if not self.dummyCombination:
                if self.highScore < self.score:
                    self.scoreLabel.configure(text=self.score)
                    self.highScore = self.score
                    self.update()

                    if self.highScore == 15:
                        playsound('Assets/Audio/success.mp3')
                        self.destroy()
                        return
                self.addOrder()
        else:
            self.combination.clear()
            self.dummyCombination.clear()

            self.incorrects += 1
            playsound('Assets/Audio/wrong.mp3')

            if self.incorrects >= 3:
                self.destroy()
                return

            self.addOrder()

    def addOrder(self):

        self.combination.append(int(random.random() * 25))
        self.dummyCombination = self.combination.copy()

        self.score = 0

        self.showOrder()

    def showOrder(self):

        len(self.combination)

        for c in self.combination:
            self.buttons[c].configure(fg_color='#fffff9')
            self.update()
            playsound('Assets/Audio/click.mp3')
            self.buttons[c].configure(fg_color='#00B7EB')
            self.update()

    def runApp(self):
        self.mainloop()

        return (self.highScore / 15) * 100
