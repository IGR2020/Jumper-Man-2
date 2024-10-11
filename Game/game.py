import pygame as pg
from Game.level import loadLevel
from Game.objects import *


class CoreGame:
    "The Base Class For All Game Objects"

    def __init__(self, resolution: tuple[int, int], fps: int = 60) -> None:
        global assets

        # pygame window config
        self.width, self.height = resolution
        self.window = pg.display.set_mode(resolution, pg.RESIZABLE)

        self.run = True
        self.clock = pg.time.Clock()
        self.fps = fps

    def event(self, event):
        if event.type == pg.QUIT:
            self.run = False
        if event.type == pg.VIDEORESIZE:
            self.width, self.height = event.dict["size"]

    def tick(self):
        self.clock.tick(self.fps)

    def display(self): ...

    def start(self):
        while self.run:
            for event in pg.event.get():
                self.event(event)
            self.tick()
            self.display()


class Level(CoreGame):

    def __init__(self, resolution: tuple[int, int], level: str, fps: int = 60) -> None:
        super().__init__(resolution, fps)

        self.objects = loadLevel(level)
        self.player = Player(100, 100, assets["Virtual Guy"])

        self.x_offset, self.y_offset = 0, 0

    def display(self):
        self.window.fill((255, 255, 255))

        for obj in self.objects:
            obj.display(self.window, self.x_offset, self.y_offset)

        self.player.display(self.window, self.x_offset, self.y_offset)

        pg.display.update()

    def tick(self):
        super().tick()

        self.player.script(self.fps, self.objects)

        self.x_offset, self.y_offset = (
            self.player.rect.centerx - self.width / 2,
            self.player.rect.bottom - self.height / 2,
        )

    def event(self, event):
        super().event(event)

        self.player.event_controls(event)
