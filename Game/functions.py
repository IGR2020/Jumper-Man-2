from os import listdir
from os.path import join, isfile, isdir
import pygame as pg
import json
import pickle


def flip(surfaces):
    return [pg.transform.flip(surface, True, False) for surface in surfaces]

def load_sprite_sheets(path, width, height, direction=True, resize=None):
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pg.image.load(join(path, image))
        sprites = []

        for i in range(sprite_sheet.get_width() // width):
            for j in range(sprite_sheet.get_height() // height):
                surface = pg.Surface((width, height), pg.SRCALPHA, 32)
                rect = pg.Rect(i * width, j * height, width, height)
                surface.blit(sprite_sheet, (0, 0), rect)
                sprites.append(pg.transform.scale2x(surface))

        if resize is not None:
            sprites = [pg.transform.scale(surface, resize) for surface in sprites]

        if direction:
            all_sprites[image.replace(".png", "") + " Right"] = sprites
            all_sprites[image.replace(".png", "") + " Left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites

def load(path, size, scale):
    return pg.transform.scale_by(pg.transform.scale(pg.image.load(path), size), scale)

def load_sprite_sheet(path: str | pg.Surface, width, height, seperation=0, resize=None, direction=False):
    if not isinstance(path, pg.Surface):
        sprite_sheet = pg.image.load(path).convert_alpha()
    else:
        sprite_sheet = path
    sprites = []
    resize_sprites = []

    for i in range(sprite_sheet.get_width() // width):
        surface = pg.Surface((width, height), pg.SRCALPHA, 32)
        rect = pg.Rect(i * width + i*seperation, 0, width, height)
        surface.blit(sprite_sheet, (0, 0), rect)
        sprites.append(pg.transform.scale2x(surface))
        if direction:
            sprites.append(flip(pg.transform.scale2x(surface)))
    if resize is None:
        return sprites
    for sprite in sprites:
        resize_sprites.append(pg.transform.scale(sprite, resize))

    return resize_sprites

def blit_text(
    win,
    text,
    pos,
    colour=(0, 0, 0),
    size=30,
    font="arialblack",
    blit=True,
    centerx=False,
    centery=False,
    center=False,
):
    text = str(text)
    x, y = pos
    font_style = pg.font.SysFont(font, size)
    text_surface = font_style.render(text, True, colour)
    if center:
        x -= text_surface.get_width() // 2
        y -= text_surface.get_height() // 2
    else:
        if centerx:
            x -= text_surface.get_width() // 2
        if centery:
            y -= text_surface.get_height() // 2
    if blit:
        win.blit(text_surface, (x, y))
    return text_surface


def load_assets(path, size: int = None, scale: float = None, getSubDirsAsList=False, scaleifsize=None):
    sprites = {}
    for file in listdir(path):
        if getSubDirsAsList and isdir(join(path, file)):
            sprites[file.replace(".png", "")] = load_assets_list(
                join(path, file), size, scale
            )
            continue
        elif not isfile(join(path, file)):
            continue
        if size is None and scale is None:
            sprites[file.replace(".png", "")] = pg.image.load(join(path, file))
        elif scale is not None:
            image = pg.image.load(join(path, file))
            if scaleifsize and image.get_size() != scaleifsize:
                  sprites[file.replace(".png", "")] = image
                  continue
            sprites[file.replace(".png", "")] = pg.transform.scale_by(
                image, scale
            )
        else:
            sprites[file.replace(".png", "")] = pg.transform.scale(
                pg.image.load(join(path, file)), size
            )
    return sprites


def load_assets_list(path, size: int = None, scale: float = None):
    sprites = []
    for file in listdir(path):
        if not isfile(join(path, file)):
            continue
        if size is None and scale is None:
            sprites.append(pg.image.load(join(path, file)))
        elif scale is not None:
            sprites.append(
                pg.transform.scale_by(pg.image.load(join(path, file)), scale)
            )
        else:
            sprites.append(pg.transform.scale(pg.image.load(join(path, file)), size))
    return sprites


def loadJson(path):
    with open(path) as file:
        data = json.load(file)
        file.close()
    return data

def setAssetsToAlpha(assets) -> dict[str, pg.Surface]:
    for asset in assets:
        assets[asset] = assets[asset].convert_alpha()
    return assets

def saveData(data, path):
    with open(path) as file:
        pickle.dump(data, file)
        file.close()

def loadData(path):
    with open(path) as file:
        data = pickle.load(file)
        file.close()
    return data
