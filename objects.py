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
    def __init__(self, x, y, width, height, sprite_sheet, sprite_index, name=None):
        super().__init__(x, y, width, height)
        self.sprite_sheet = sprite_sheet
        self.sprite_index = sprite_index
        self.name = name

    def display(self, window: pg.Surface, x_offset: int, y_offset: int):
        window.blit(assets[self.sprite_sheet][self.sprite_index], (self.rect.x - x_offset, self.rect.y - y_offset))

import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, sprites):
        super().__init__()
        self.sprites = sprites
        self.jump_count = 0
        self.animation_count = 0
        self.sprite = self.sprites["Idle_left"][0]
        self.rect = self.sprite.get_rect(topleft=(x, y))
        self.direction = "left"
        self.x_vel = 0
        self.y_vel = 0
        self.hit = False
        self.hit_count = 0
        self.animate_speed = 6 # higher value lower speed
        self.sprite_sheet = "Idle"

        # movement
        self.fall_speed = 0.2
        self.speed = 0.5
        self.max_speed = 8
        self.jump_height = 8

    def display(self, screen, x_offset, y_offset):
        # getting current sprite sheet
        self.sprite_sheet = "Idle"
        if self.x_vel != 0:
            self.sprite_sheet = "Run"
        if self.x_vel > 0:
            self.direction = "right"
        if self.x_vel < 0:
            self.direction = "left"
        self.sprite_sheet = self.sprite_sheet + "_" + self.direction
        sprite_index = (self.animation_count // self.animate_speed) % len(self.sprites[self.sprite_sheet])
        self.sprite = self.sprites[self.sprite_sheet][sprite_index]
        self.animation_count += 1

        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
            
        screen.blit(self.sprite, (self.rect.x - x_offset, self.rect.y - y_offset))

    def landed(self, obj):
        self.y_vel = 0
        self.jump_count = 0
        self.rect.bottom = obj.rect.top

    def hit_head(self, obj):
        self.y_vel = 0
        self.rect.top = obj.rect.bottom

    def is_hit(self):
        self.hit = True
        self.hit_count = 0
        self.rect.x, self.rect.y = 100, 100

    def move(self, dx, dy, objects):
        self.rect.y += dy
        for obj in objects:
            if self.rect.colliderect(obj.rect):
                if dy > 0:
                    self.landed(obj)
                else:
                    self.hit_head(obj)
                break
        self.rect.x += dx
        for obj in objects:
            if self.rect.colliderect(obj.rect):
                if dx > 0:
                    self.rect.right = obj.rect.left
                else:
                    self.rect.left = obj.rect.right
                break

    def move_left(self):
        self.x_vel -= self.speed
        self.x_vel = max(min(self.x_vel, self.max_speed), -self.max_speed)

    def move_right(self):
        self.x_vel += self.speed
        self.x_vel = max(min(self.x_vel, self.max_speed), -self.max_speed)

    def jump(self):
        if self.jump_count < 1:
            self.y_vel -= self.jump_height
            self.jump_count += 1
            self.animation_count = 0
        self.animation_count = 0

    def controls(self):
        if self.jump_count != 0:
            self.max_speed = 5
        else:
            self.max_speed = 8
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.move_right()
        elif keys[pygame.K_a]:
            self.move_left()
        else:
            if abs(self.x_vel) < 1:
                self.x_vel = 0
            else:
                self.x_vel *= 0.2

    def event_controls(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.jump()

    def script(self, fps, objects):
        if self.hit:
            self.hit_count += 1
        if self.hit_count >= fps // 2:
            self.hit = False

        self.y_vel += self.fall_speed
        self.move(self.x_vel, self.y_vel, objects)
        if self.rect.y > 1000:
            self.is_hit()
        self.controls()

class Gumpa:
    def __init__(self, x, y, sprites) -> None:
        self.sprites = sprites
        self.jump_count = 0
        self.animation_count = 0
        self.sprite = self.sprites["Run"][0]
        self.rect = self.sprite.get_rect(topleft=(x, y))
        self.x_vel = -2
        self.y_vel = 0
        self.animate_speed = 6 # higher value lower speed
        self.sprite_sheet = "Run"
        self.fall_speed = 0.2

    def landed(self, obj):
        self.y_vel = 0
        self.rect.bottom = obj.rect.top
        
    def move(self, dx, dy, objects):
        self.rect.x += dy
        for obj in objects:
            if self.rect.colliderect(obj.rect):
                self.landed(obj)
                self.animation_count = 0
                break
        self.rect.x += dx
        for obj in objects:
            if self.rect.colliderect(obj.rect):
                if dx > 0:
                    self.rect.right = obj.rect.left
                    self.x_vel = -1
                else:
                    self.rect.left = obj.rect.right
                    self.x_vel = 1
                self.animation_count = 0
                break

    def script(self, objects):
        self.y_vel += self.fall_speed
        self.move(self.x_vel, self.y_vel, objects)

    def display(self, screen, x_offset, y_offset):
        # getting current sprite sheet
        self.sprite_sheet = "Run"
        self.sprite_sheet = self.sprite_sheet
        sprite_index = (self.animation_count // self.animate_speed) % len(self.sprites[self.sprite_sheet])
        self.sprite = self.sprites[self.sprite_sheet][sprite_index]
        self.animation_count += 1

        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
            
        screen.blit(self.sprite, (self.rect.x - x_offset, self.rect.y - y_offset))
