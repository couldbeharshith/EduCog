import customtkinter as ctk

from customtkinter import CTkFrame
from customtkinter import CTkLabel

import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as tkagg
import json

def stats(user: str):

    games = zip(('ReactionGame', 'SpatialGame', 'ColorGame', 'MemoryGame'), ('#f02521', 'red', '#fed724', '#74a6d7'))

    with open('Database\\user_stats.json', 'r') as file:
        data = json.loads(file.read())

    highScore = data[user]['HighScores']

    root = ctk.CTk()
    root.title('Statistics')
    root.geometry('1000x600')

    CTkLabel(root, text='Statistics', font=ctk.CTkFont(size=50), anchor='center').place(relx=0.4, rely=0.02)

    fScores = CTkFrame(root, fg_color='#4B4B4B')
    fScores.place(relx=0.36, rely=0.53, relwidth=0.65, relheight=0.8, anchor='center')

    fRight = CTkLabel(root, bg_color='transparent', text=f'User High-score\n{highScore}',
                      font=ctk.CTkFont('LEMONMILK-Bold', 25))
    fRight.place(relx=0.72, rely=0.129)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title("Peer Comparision")
    ax.set_xlabel("Time")
    ax.set_ylabel("Scores")
    currData = data[user]

    for game, color in games:
        gameData = currData[game]
        ax.plot([x for x in gameData], [y for y in gameData.values()], linewidth=2, color=color)

    canvas = tkagg.FigureCanvasTkAgg(fig, master=fScores)
    canvas.get_tk_widget().place(relx=0.5, rely=0.5, relheight=0.95, relwidth=0.95, anchor='center')

    root.mainloop()
