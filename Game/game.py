import pygame as pg
from Game.level import loadLevel
from Game.objects import *
from Game.GUI import Text

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

        self.deltaTime = 0

    def event(self, event):
        if event.type == pg.QUIT:
            self.run = False
        if event.type == pg.VIDEORESIZE:
            self.width, self.height = event.dict["size"]

    def tick(self):
        self.deltaTime = self.clock.tick(self.fps) / 16

    def display(self): ...

    def start(self):
        while self.run:
            for event in pg.event.get():
                self.event(event)
            self.tick()
            self.display()


class Level(CoreGame):

    def __init__(self, resolution: tuple[int, int], level: str, fps: int = 60, background: str = "Blue") -> None:
        super().__init__(resolution, fps)
        pg.display.set_caption(f"Jumper Man 2 (Level {level.replace(".txt", "")}) ({version})")
        pg.display.set_icon(assets["Virtual Guy"]["Idle Right"][0])

        self.objects, self.levelSize = loadLevel(levelLocation + level)
        self.player = Player(100, 100, assets["Virtual Guy"])
        self.player.void = self.levelSize[1] + blockSize*2

        self.x_offset, self.y_offset = 0, 0

        self.background = background

        self.lowFPS = False

    def display(self):
        self.window.fill((255, 255, 255))

        if not self.lowFPS:
            for i in range((self.width//backgroundSize)+1):
                for j in range((self.height//backgroundSize)+1):
                    self.window.blit(assets["Background"][self.background], (i*backgroundSize, j*backgroundSize))

        for obj in self.objects:
            obj.display(self.window, self.x_offset, self.y_offset)

        self.player.display(self.window, self.x_offset, self.y_offset)

        pg.display.update()

    def tick(self):
        super().tick()

        if self.clock.get_fps() < 50 and self.clock.get_fps() > 1:
            print(f"[Warning] Low FPS {round(self.clock.get_fps())}")
            if not self.lowFPS:
                self.lowFPS = True
                print(f"[Graphics] Turning on optimized mode")

        self.player.script(self.fps, self.objects, self.deltaTime)

        self.x_offset, self.y_offset = (
            self.player.rect.centerx - self.width / 2,
            self.player.rect.bottom - self.height / 2,
        )

        if self.player.win:
            winMenu = Win((self.width, self.height), background=self.background)
            winMenu.start()
            self.run = False

    def event(self, event):
        super().event(event)

        self.player.event_controls(event)


class Win(CoreGame):
    def __init__(self, resolution: tuple[int, int], fps: int = 60, background: str = "Blue") -> None:
        super().__init__(resolution, fps)
        pg.display.set_caption("Victory")
        self.background = background
        self.text = Text("Victory", self.width/2, self.height/2, (0, 0, 0), 250, "Retro Font", center=True)

    def display(self):
        self.window.fill((255, 255, 255))
        for i in range((self.width//backgroundSize)+1):
            for j in range((self.height//backgroundSize)+1):
                self.window.blit(assets["Background"][self.background], (i*backgroundSize, j*backgroundSize))
        self.text.display(self.window)
        pg.display.update()