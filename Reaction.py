import pygame as pg
from time import time, sleep
from random import randint


class Circle:
    allInstances = []

    def __init__(self, rad: int, pos) -> None:
        self.rad = rad
        self.pos = pos

        Circle.allInstances.append(self)

    def kill(self):
        Circle.allInstances.remove(self)
        del self

    # file = open('Apps\\Reaction Game\\Database\\user_stats.json', 'w')
    # from random import randint
    # for user in ('Harshith', 'Pragati', 'Tobit'):
    #     for game, _ in games:
    #         for key in data[user][game].keys():
    #             data[user][game][key] = randint(70,100)

    # json.dump(data, file, indent=2)
    # file.close()

    def increaseSize(self):
        self.rad += (10 / self.rad) * 0.7

        if self.rad > 45:
            self.kill()

    def draw(self, SCREEN, color):
        pg.draw.circle(SCREEN, color=color, radius=self.rad, center=self.pos)

    @staticmethod
    def checkClick(pos):
        for c in Circle.allInstances:
            if (c.pos - pos).magnitude() < c.rad:
                c.kill()

                return True

    @staticmethod
    def updateInstances(screen, color):
        for c in Circle.allInstances:
            c.increaseSize()
            c.draw(screen, color)


def runApp():
    pg.init()

    winWidth, winHeight = DIMS = (800, 600)
    SCREEN = pg.display.set_mode(DIMS)
    pg.display.set_caption("Reaction time testing game")
    SCORE_FONT = pg.font.Font('Assets/LEMONMILK-Bold.otf', 50)
    BGCOLOR = pg.color.Color(25, 25, 25)
    CLOCK = pg.time.Clock()

    def getPoint() -> tuple[int, int]: return randint(50, winWidth-50), randint(50, winHeight - 50)

    targetsCreated = 0
    targetsHit = 0

    startTime = time()
    delay = 1
    prevTime = startTime - delay

    def endGame():

        Circle.allInstances.clear()

        SCREEN.fill(BGCOLOR)

        gameOver = SCORE_FONT.render('Game Over', True, '#FD4239')
        SCREEN.blit(gameOver, (winWidth // 2 - gameOver.get_width() // 2, winHeight // 2 - gameOver.get_height() // 2))

        pg.display.flip()

        sleep(1)

        pg.quit()

    while True:
        SCREEN.fill(BGCOLOR)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                endGame()
                return (targetsHit / targetsCreated) * 100

            if event.type == pg.MOUSEBUTTONDOWN:
                if Circle.checkClick(pg.Vector2(pg.mouse.get_pos())):
                    targetsHit += 1

        currentTime = time()
        if currentTime - prevTime > delay:
            prevTime = currentTime
            Circle(10, pg.Vector2(getPoint()))
            targetsCreated += 1

        if time() - startTime > 40:
            endGame()
            return (targetsHit / targetsCreated) * 100

        Circle.updateInstances(SCREEN, (60, 60, 60))

        score = SCORE_FONT.render(str(targetsHit), True, (255, 255, 245))
        SCREEN.blit(score, (winWidth//2 - score.get_width()//2, 100 - score.get_height()//2))
        pg.display.update()
        CLOCK.tick(70)
