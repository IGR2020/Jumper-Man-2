import json
from objects import Block
from assets import *

def load_data(path):
    with open(path) as file:
        data = json.load(file)
        file.close()
    return data

def convert_blocks(data, sprite_sheet, air=32, y_offset=0):
    """
    air indicates which value to be interpreted as null
    """
    objects = []
    for x, collum in enumerate(data):
        for y, value in enumerate(collum):
            if value == air:
                continue
            objects.append(Block(x*block_size, y*block_size+y_offset, block_size, block_size, sprite_sheet, value))
    return objects

data = load_data("Level Data/Level 1.json")
theme = data["Theme"]
level_data = data["Data"]
level1 = convert_blocks(level_data, theme)
