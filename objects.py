import pygame as pg
from assets import assets

class Object(pg.sprite.Sprite):
    
    def __init__(self, x, y, width, height):
        self.rect = pg.Rect(x, y, width, height)
        self.mask = None
    
    def set_mask(self, image):
        self.mask = pg.mask.from_surface(image)
    
    def display(): ...

class Block(Object):
    def __init__(self, x, y, width, height, sprite_sheet, sprite_index):
        super().__init__(x, y, width, height)
        self.sprite_sheet = sprite_sheet
        self.sprite_index = sprite_index

    def display(self, window: pg.Surface, x_offset: int, y_offset: int):
        window.blit(assets[self.sprite_sheet][self.sprite_index], (self.rect.x - x_offset, self.rect.y - y_offset))
