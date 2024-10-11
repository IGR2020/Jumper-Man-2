import pygame as pg
from Game.functions import *

blockSize = 96
playerSize = 64
assets = load_assets("Game/Assets/Terrain", (blockSize, blockSize))
assets["Virtual Guy"] = load_sprite_sheets(r"Game\Assets\Main Characters\Virtual Guy", 32, 32, resize=(playerSize, playerSize), direction=True)
assets["Spike"] = load(r"Game\Assets\Traps\Spikes\Idle.png", (blockSize, blockSize), 1)
assets["Fire"] = load_sprite_sheets(r"Game\Assets\Traps\Fire", 16, 32, False)