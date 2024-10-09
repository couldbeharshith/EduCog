import pygame as pg


class NineSliced:
    widthError = ValueError('width is too low')
    heightError = ValueError('length is too low')

    def __init__(self, baseImage: pg.surface.Surface, slices: tuple[int, int, int, int]):

        self.baseImage = baseImage
        self.left, self.right, self.top, self.bottom = self.slices = slices
        self.imageWidth, self.imageHeight = baseImage.get_width(), baseImage.get_height()
        self.centre = (self.left, self.top, self.imageWidth - self.right, self.imageHeight - self.bottom)
        self.parts = {}

        self.createParts()

    def createParts(self):

        horizontals = (0, self.centre[0], self.centre[2], self.imageWidth)
        verticals = (0, self.centre[1], self.centre[3], self.imageHeight)
        self.parts.clear()

        for v in range(len(verticals) - 1):
            for h in range(len(horizontals) - 1):
                surface = pg.surface.Surface((horizontals[h + 1] - horizontals[h], verticals[v + 1] - verticals[v]),
                                             pg.SRCALPHA)

                surface.blit(self.baseImage, (0, 0),
                             (horizontals[h], verticals[v], horizontals[h + 1], verticals[v + 1]))

                self.parts[len(self.parts)] = surface.copy()

    def createImage(self, width, height, scale=1) -> pg.surface.Surface:

        if width < self.imageWidth:
            raise self.widthError
        if height < self.imageHeight:
            raise self.heightError

        horizontalResize = width - (self.left + self.right) * scale
        verticalResize = height - (self.top + self.bottom) * scale

        horizontals = (0, self.left * scale, width - self.right * scale)
        verticals = (0, self.right * scale, height - self.bottom * scale)

        image = pg.surface.Surface((width, height), pg.SRCALPHA)
        part = 0

        for v in range(len(verticals)):
            for h in range(len(horizontals)):
                image.blit(pg.transform.scale(self.parts[part], (
                    horizontalResize if h % 2 else self.parts[part].get_width() * scale,
                    verticalResize if v % 2 else self.parts[part].get_height() * scale)), (horizontals[h], verticals[v]))
                part += 1

        return image


class Text:

    def __init__(self, text, color, position, size):
        self.font = pg.font.Font('Assets/LEMONMILK-Bold.otf', size)
        self.text = text
        self.color = color
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect()
        self.position = position

        self.rect.topLeft = position

    def draw(self, screen: pg.surface.Surface):
        screen.blit(self.image, self.rect)

    def updateText(self, text=None, color=None):
        self.text = text if text is not None else self.text
        self.color = color if color else self.color

        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = self.position


class Button:
    allInstances = []

    def __init__(self, position, size, plateActive, plateInactive, icon, function):

        self.plateActive = plateActive
        self.plateInactive = plateInactive

        self.imageActive = self.plateActive.createImage(*size, 2)
        self.imageInactive = self.plateInactive.createImage(*size, 2)

        self.image = self.imageInactive

        self.rect = self.imageActive.get_rect()

        self.position = position
        self.icon = icon
        self.iconRect = self.icon.get_rect()
        self.function = function

        self.iconRect.center = self.rect.center = self.position

        self.activated = False
        self.hidden = False

        Button.allInstances.append(self)

    def activate(self):
        self.activated = True
        self.image = self.imageActive

    def deactivate(self, *args):
        self.activated = False
        self.image = self.imageInactive
        self.function(*args)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.icon, self.iconRect)

    def setPosition(self, position):
        self.position = position
        self.iconRect.center = self.rect.center = self.position

    def kill(self):
        Button.allInstances.remove(self)
        del self

    @staticmethod
    def drawInstances(screen):
        for button in Button.allInstances:
            if not button.hidden:
                button.draw(screen)

    @staticmethod
    def checkInteraction():
        for button in Button.allInstances:
            if button.rect.collidepoint(pg.mouse.get_pos()) and not button.hidden:
                button.activate()
                return button
        return None


class KeyBind:
    def __init__(self):
        pass
