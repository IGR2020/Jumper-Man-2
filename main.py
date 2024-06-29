import pygame as pg

window_width, window_height = 900, 500
window = pg.display.set_mode((window_width, window_height))
pg.display.set_caption("Updated Platformer!")

from assets import assets
from objects import Block

run = True
fps = 60
clock = pg.time.Clock()

x_offset = 0
y_offset = 0

def display():
    window.fill((40, 50, 200))
    pg.display.update()


while run:

    clock.tick(fps)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    display()

pg.quit()
quit()