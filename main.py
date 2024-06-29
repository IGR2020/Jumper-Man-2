import pygame as pg

window_width, window_height = 900, 500
window = pg.display.set_mode((window_width, window_height))
pg.display.set_caption("Updated Platformer!")

from assets import *
from objects import Block, Player
from level import level1

run = True
fps = 60
clock = pg.time.Clock()

x_offset = 0
y_offset = 0

player = Player(100, 100, load_sprite_sheets("Assets/Player", 16, 16, 1, True, (32, 32)))
blocks = level1

def display():
    window.fill((100, 170, 200))
    for block in blocks:
        block.display(window, x_offset, y_offset)
    player.display(window, x_offset, y_offset)
    pg.display.update()


while run:

    clock.tick(fps)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        player.event_controls(event)

    player.script(fps, blocks)
    display()

pg.quit()
quit()