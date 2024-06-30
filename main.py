import pygame as pg

window_width, window_height = 900, 500
window = pg.display.set_mode((window_width, window_height))
pg.display.set_caption("Updated Platformer!")

from assets import *
from objects import Block, Player, Gumpa
from level import level1

run = True
fps = 60
clock = pg.time.Clock()

x_offset = 0
y_offset = 0

player = Player(100, 100, load_sprite_sheets("Assets/Player", 16, 16, 1, True, (player_size, player_size)))
gumpa = Gumpa(block_size*7, 6*block_size, load_sprite_sheets("Assets/Enemy/Gumpa", 16, 16, 1, False, (player_size, player_size)))
blocks = level1

def display():
    window.fill((100, 170, 200))
    for block in blocks:
        block.display(window, x_offset, y_offset)
    player.display(window, x_offset, y_offset)
    gumpa.display(window, x_offset, y_offset)
    pg.display.update()


while run:

    clock.tick(fps)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        player.event_controls(event)

    x_offset = player.rect.x
    x_offset = x_offset-window_width/2

    player.script(fps, blocks)
    gumpa.script(blocks)
    display()

pg.quit()
quit()