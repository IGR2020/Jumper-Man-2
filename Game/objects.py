import pygame as pg
from Game.assets import *


class Object:

    def __init__(
        self,
        x: int,
        y: int,
        name: str,
        scale: int = 1,
        angle: int = 0,
        size: tuple[int, int] | list[int, int] = None,
        image: pg.Surface | None = None,
        type="Object",
    ) -> None:
        self.name = name
        try:
            self.rect: pg.Rect = assets[name].get_rect(topleft=(x, y))
            self.mask = pg.mask.from_surface(assets[name])
        except:
            self.rect = pg.Rect(x, y, 1, 1)
            self.update(image)
        self.scale = scale
        self.angle = angle
        if size is None:
            self.size = self.rect.width, self.rect.height
        else:
            self.size = size
        self.size = [self.size[0], self.size[1]]
        self.reload(image)
        self.type = type

    def resetSize(self) -> None:
        self.size = [assets[self.name].get_width(), assets[self.name].get_height()]

    def reload(self, image: pg.Surface | None) -> None:
        if image is None:
            self.morphedImage = pg.transform.scale(assets[self.name], self.size)
        else:
            self.morphedImage = pg.transform.scale(image, self.size)
        self.scaledImage = pg.transform.scale_by(self.morphedImage, self.scale)
        self.rotatedImage = pg.transform.rotate(self.scaledImage, self.angle)
        self.mask = pg.mask.from_surface(self.rotatedImage)
        self.rect = self.rotatedImage.get_rect(center=self.rect.center)

    def rotate(self) -> None:
        self.rotatedImage = pg.transform.rotate(self.scaledImage, self.angle)
        self.mask = pg.mask.from_surface(self.rotatedImage)
        self.rect = self.rotatedImage.get_rect(center=self.rect.center)

    def display(self, window: pg.Surface, x_offset: int = 0, y_offset: int = 0) -> None:
        window.blit(self.rotatedImage, (self.rect.x - x_offset, self.rect.y - y_offset))

    def update(self, image):
        self.rect = image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pg.mask.from_surface(image)

class AnimatedBlock(Object):
    animationSpeed = 3
    animationCount = 0
    sprite = pg.Surface((blockSize, blockSize))

    def display(self, window: pg.Surface, x_offset: int = 0, y_offset: int = 0) -> None:
        window.blit(self.sprite, (self.rect.x - x_offset, self.rect.y - y_offset))
        self.update_sprite()

    def __init__(self, x: int, y: int, name: str, sprites: str, scale: int = 1, angle: int = 0, size: tuple[int, int] | list[int] = None, image: pg.Surface | None = None, type="Object") -> None:
        super().__init__(x, y, name, scale, angle, size, image, type)
        self.sprite_sheet = "Idle"
        self.sprites = sprites

    def update_sprite(self):
        sprite_sheet_name = self.sprite_sheet
        sprites = self.sprites[sprite_sheet_name]
        sprite_index = (self.animationCount // self.animationSpeed) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animationSpeed += 1
        self.update(self.sprite)


class Fire(AnimatedBlock):
    def __init__(self, x: int, y: int, scale: int = 1, angle: int = 0, size: tuple[int, int] | list[int] = None) -> None:
        super().__init__(x, y, None, assets["Fire"], scale, angle, size, assets["Fire"]["Off"][0], "Trap")
        self.sprite_sheet = "On"

    def update_sprite(self):
        self.sprite_sheet = "On"
        super().update_sprite()

class Player:
    def __init__(self, x, y, sprites):
        self.sprites = sprites
        self.jump_count = 0
        self.animation_count = 0
        self.sprite = self.sprites["Idle Left"][0]
        self.rect = self.sprite.get_rect(topleft=(x, y))
        self.direction = "Left"
        self.x_vel = 0
        self.y_vel = 0
        self.hit = False
        self.hit_count = 0
        self.animate_speed = 3
        self.sprite_sheet = "Idle"
        self.gravity = 1
        self.fall_count = 0
        self.speed = 5
        self.mask = pg.mask.from_surface(self.sprite)
        self.bonusSpeed = 0
        self.acceleration = 0.5
        self.friction = 0.4
        self.onIce = False

    def display(self, screen, x_offset, y_offset):
        self.update_sprite()
        screen.blit(self.sprite, (self.rect.x - x_offset, self.rect.y - y_offset))
        return x_offset, y_offset

    def update_sprite(self):
        self.sprite_sheet = "Idle"
        if self.hit:
            self.sprite_sheet = "Hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                self.sprite_sheet = "Jump"
            elif self.jump_count == 2:
                self.sprite_sheet = "Double Jump"
        elif self.y_vel > self.gravity * 2:
            self.sprite_sheet = "Fall"
        elif self.x_vel != 0:
            self.sprite_sheet = "Run"
        sprite_sheet_name = self.sprite_sheet + " " + self.direction
        sprites = self.sprites[sprite_sheet_name]
        sprite_index = (self.animation_count // self.animate_speed) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pg.mask.from_surface(self.sprite)

    def landed(self, obj):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0
        self.rect.bottom = obj.rect.top
        if obj.name == "Ice Block":
            self.friction = 0.05
            self.speed = 25
            self.acceleration = 0.1
        else:
            self.acceleration = 0.5
            self.friction = 0.4
            self.speed = 5

    def hit_head(self, obj):
        self.y_vel = 0
        self.rect.top = obj.rect.bottom

    def is_hit(self):
        self.hit = True
        self.hit_count = 0
        self.jump_count = 0
        self.rect.x, self.rect.y = 100, 100

    def trapEffect(self, obj):
        if not pg.sprite.collide_mask(self, obj):
            return
        if obj.type == "Trap":
            self.is_hit()

    def move(self, objects):
        self.rect.y += self.y_vel
        for obj in objects:
            if self.rect.colliderect(obj.rect) and obj.type == "Object":
                if self.y_vel > 0:
                    self.landed(obj)
                else:
                    self.hit_head(obj)
            self.trapEffect(obj)
        self.rect.x += self.x_vel + self.bonusSpeed
        for obj in objects:
            if self.rect.colliderect(obj.rect) and obj.type == "Object":
                if self.x_vel + self.bonusSpeed > 0:
                    self.rect.right = obj.rect.left
                else:
                    self.rect.left = obj.rect.right
            self.trapEffect(obj)

    def move_left(self):
        self.x_vel += -self.acceleration
        if self.direction != "Left":
            self.direction = "Left"
            self.animation_count = 0

    def move_right(self):
        self.x_vel += self.acceleration
        if self.direction != "Right":
            self.direction = "Right"
            self.animation_count = 0

    def jump(self):
        self.speed = 1.5
        if self.jump_count < 2:
            self.y_vel = -self.gravity * 8
            self.jump_count += 1
            self.animation_count = 0
        if self.jump_count == 1:
            if abs(self.x_vel) > 0:
                self.bonusSpeed += max(abs(self.x_vel), 8.5) * (
                    self.x_vel / abs(self.x_vel)
                )
            self.fall_count = 0

    def controls(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_d]:
            self.move_right()
        elif keys[pg.K_a]:
            self.move_left()
        elif abs(self.x_vel) > 0:
            self.x_vel -= (self.x_vel / abs(self.x_vel)) * self.friction
            if abs(self.x_vel) < 0.6:
                self.x_vel = 0

    def event_controls(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                self.jump()
            if event.key == pg.K_r:
                self.is_hit()

    def script(self, fps, objects):
        if self.hit:
            self.hit_count += 1
        if self.hit_count >= fps // 2:
            self.hit = False

        self.y_vel += min(1, (self.fall_count / fps) * self.gravity)
        self.move(objects)
        if self.rect.y > 1000:
            self.is_hit()
        if abs(self.bonusSpeed) > 0:
            self.bonusSpeed -= (self.bonusSpeed / abs(self.bonusSpeed)) * 0.2
        self.fall_count += 1
        self.controls()
        self.x_vel = min(max(self.x_vel, -self.speed), self.speed)
